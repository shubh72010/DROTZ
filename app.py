import os
import requests
import json
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Get OpenRouter key from Render environment
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return send_file("index.html")  # Serve index.html from root

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    payload = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site-url.com",  # optional
        "X-Title": "FlayAI",                          # optional
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500