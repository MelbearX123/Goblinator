from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)
llm = Llama(model_path="./models/llama-2-7b.Q4_K_M.gguf")

@app.route("/api/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt", "")
    output = llm(prompt, max_tokens=100, stop=["\n\n"])
    return jsonify({"response": output["choices"][0]["text"]})

if __name__ == "__main__":
    app.run(port=5000)