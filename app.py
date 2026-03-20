import os, requests
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)
BOT_TOKEN = "8480955083:AAFVIXXvXmbt7irxXTUte3ppItRDwn_0CXA"
genai.configure(api_key="AIzaSyAfUdfj6FDJwwGLdoXn_wE-jFfvORIKQnE")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_msg = data["message"].get("text", "")
            try:
                response = model.generate_content(f"Act as Termux & App King. User: {user_msg}")
                reply = response.text
            except:
                reply = "⚠️ API Limit ya Connection Error!"
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          json={"chat_id": chat_id, "text": f"💀 **MASTER AI**\n\n{reply}", "parse_mode": "Markdown"})
        return "ok", 200
    return "Bot is Running!"
