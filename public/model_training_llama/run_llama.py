from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "/Users/samuelzhang/Llama-3.2-3B-I" #DIRECTORY TO LOCAL INSTALL

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="auto"
)

prompt = "example prompt"
print("=======")
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
print("=======")
output = model.generate(**inputs, max_new_tokens=450)
print(tokenizer.decode(output[0], skip_special_tokens=True))
