from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key)
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in the .env file.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins. Replace with specific origins if needed.

@app.route("/")
def read_root():
    return jsonify({"Backend": "Online!!!"})

class Item:
    def __init__(self, prompt: str):
        self.prompt = prompt

@app.route("/chat", methods=["POST"])
def read_chat():
    request_data = request.get_json()
    prompt = request_data.get("prompt", "")
    engine = request_data.get("engine", "text-davinci-003")

    response = get_openai_response(engine, prompt)
    return jsonify({"prompt": prompt, "response": response})

ENGINE = "text-curie-001"
# ENGINE = "text-davinci-003"
def get_openai_response(engine: str, prompt: str) -> str:
    try:
        response = openai.Completion.create(engine=ENGINE, prompt=prompt, max_tokens=100, temperature=0.7, n=1, stop=None)
        return response.choices[0].text.strip()
    except Exception as e:
        return "Error calling OpenAI API", 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
