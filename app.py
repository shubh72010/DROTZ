import os
import json
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MAX_DOTS_MODEL = "openrouter/cypher-alpha:free"
DEFAULT_MODEL = "deepseek/deepseek-r1:free"

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/settings.html")
def settings():
    return send_file("settings.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    max_dots_mode = data.get("maxDots", False)
    selected_model = data.get("defaultModel", DEFAULT_MODEL)
    model = MAX_DOTS_MODEL if max_dots_mode else selected_model

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://drotz.onrender.com",
        "X-Title": "DORTZ"
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        result = response.json()
        result["used_model"] = model
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500