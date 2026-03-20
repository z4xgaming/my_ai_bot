import os, requests
from flask import Flask, request
import google.generativeai as genai
from gtts import gTTS

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "" # <--- Apna Telegram Token yahan dalo
genai.configure(api_key="AIzaSyAfUdfj6FDJwwGLdoXn_wE-jFfvORIKQnE")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if data and "message" in data:
                chat_id = data["message"]["chat"]["id"]
                user_msg = data.get("message", {}).get("text", "")

                if user_msg:
                    # 1. Jiya Meena ka Dimag (Duplicate of Gemini)
                    prompt = f"You are Jiya Meena, an AI. Reply to this as a voice message: {user_msg}"
                    response = model.generate_content(prompt)
                    reply_text = response.text

                    # 2. Direct Voice (MP3) Generation
                    tts = gTTS(text=reply_text, lang='hi') 
                    audio_path = "/tmp/jiya_voice.mp3"
                    tts.save(audio_path)

                    # 3. Direct Audio Message bhejna (Caption ke saath)
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
                    files = {'audio': open(audio_path, 'rb')}
                    data_payload = {
                        'chat_id': chat_id,
                        'caption': f"🌸 **JIYA MEENA**\n\n{reply_text[:100]}...", # Short preview
                        'parse_mode': 'Markdown'
                    }
                    requests.post(url, data=data_payload, files=files)
                    
                    # Cleanup
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
        except Exception as e:
            print(f"Error: {e}")
        return "ok", 200
    
    return "<h1>🎙️ Jiya Meena: Direct Voice is Online!</h1>"
