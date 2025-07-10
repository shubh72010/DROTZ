import os
import json
import random
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Free rotating models
FREE_MODELS = [
    "deepseek/deepseek-r1-0528:free",
    "mistralai/mixtral-8x7b-instruct:free",
    "meta-llama/llama-3-70b-instruct:free",
    "anthropic/claude-3-haiku:free",
    "google/gemini-pro-1.5:free"
]

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    max_dots_mode = data.get("maxDots", False)

    # Pick model
    model = (
        "openrouter/cypher-alpha:free"
        if max_dots_mode
        else random.choice(FREE_MODELS)
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourapp.onrender.com",
        "X-Title": "FlayAI - Max Dots Chat"
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