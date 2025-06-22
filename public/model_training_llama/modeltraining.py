import torch
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
from transformers import TrainerCallback, TrainerState, TrainerControl
from transformers.integrations import TensorBoardCallback
import os

# allow unsupported ops to fall back to CPU
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

##functions
def tokenize(data):
    return tokenizer(data["text"], truncation=True, padding="max_length", max_length=512)

####

#initialize modelID
model_id = "/Users/samuelzhang/Llama-3.2-3B-I" #PUT IN DIRECTORY HERE

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float16,  # or torch.float32 for CPU fallback
    max_memory={                        # tune these if you hit CPU OOM
      "cpu": "52GB",                    # spill almost everything
      "mps": "4GB"                      
    },
)
#PEFT Training config
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    task_type=TaskType.CAUSAL_LM,
    lora_dropout=0.05,
    bias="none"
)
model = get_peft_model(model, peft_config)

#Training Content
training_args = TrainingArguments(
    output_dir="./llama-1b-brainrot",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    dataloader_num_workers=4,
    optim="adamw_torch",
    warmup_steps=50,
    num_train_epochs=3,
    save_steps=100,
    save_total_limit=2,
    logging_dir='./logs',
    fp16=True,
    bf16=False,
    gradient_checkpointing=True,
    torch_compile=False,
    max_grad_norm=1.0
    )

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
train_dataset = load_dataset("json", data_files="brainrot_data.json")["train"]
tokenized_dataset = train_dataset.map(tokenize, batched=True)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,    
    tokenizer=tokenizer,
    data_collator=data_collator,
    callbacks=[TensorBoardCallback()]
)


if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id
if model.config.pad_token_id is None:
    model.config.pad_token_id = model.config.eos_token_id

trainer.train()

model.save_pretrained("./llama-3b-brainrot-adapter")
tokenizer.save_pretrained("./llama-3b-brainrot-adapter")