import os
import json
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(name)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

Define models

DEFAULT_MODEL = "google/gemini-2.0-flash-exp:free" MAX_DOTS_MODEL = "openrouter/cypher-alpha:free"

@app.route("/") def home(): return send_file("index.html")

@app.route("/chat", methods=["POST"]) def chat(): data = request.get_json() user_input = data.get("message", "") max_dots_mode = data.get("maxDots", False)

# Pick model
model = MAX_DOTS_MODEL if max_dots_mode else DEFAULT_MODEL

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

