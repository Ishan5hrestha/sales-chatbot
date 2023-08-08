from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from views.openai_view import openai_bp
from views.trends import serpapi_bp


app = Flask(__name__)
CORS(app)  # Enable CORS for all origins. Replace with specific origins if needed.

app.register_blueprint(openai_bp)
app.register_blueprint(serpapi_bp)

@app.route("/")
def read_root():
    return jsonify({"Backend": "Online!!!"})

# @app.route("/trends", methods=["POST"])
# def get_trends():
#     result = keyword_trend('volcano')
#     return jsonify({"keyword": 'volcano', "response": result})

if __name__ == "__main__":
    app.run()
