import os
import openai
from dotenv import load_dotenv
from flask import request, jsonify, Blueprint

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in the .env file.")

pass_phrase = os.getenv("PASSWORD")
all_engines = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]

openai_bp = Blueprint('openai', __name__)
@openai_bp.route('/openai')
def profile():
    return jsonify({"status": "active"})


@openai_bp.route("/chat", methods=["POST"])
def get_result():
    request_data = request.get_json()
    prompt = request_data.get("prompt", "")
    engine = request_data.get("engine", "text-davinci-003")
    
    # So that garbage from frontend doesn't pass ahead
    if engine not in all_engines:
        engine = "text-davinci-003"

    password = request_data.get("password","")
    if password != pass_phrase: 
        return jsonify({"Error":"Incorrect Key"})

    response = get_openai_response(engine, prompt)
    return jsonify({"prompt": prompt, "response": response})

def get_openai_response(engine: str, prompt: str) -> str:
    try:
        response = openai.Completion.create(engine=engine, prompt=prompt, max_tokens=2049, temperature=0.7, n=1, stop=None)
        return response.choices[0].text.strip()
    except Exception as e:
        return "Error calling OpenAI API", 500
