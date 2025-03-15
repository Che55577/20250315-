from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import cv2
import yt_dlp
import os
import googletrans
from textblob import TextBlob
import numpy as np

app = Flask(__name__)

# 設定 YouTube 播放對應的情緒與音樂
emotion_music = {
    "angry": "https://www.youtube.com/watch?v=8jzDnsjYv9A",
    "annoyed": "https://www.youtube.com/watch?v=LRP8d7hhpoQ",
    "sad": "https://www.youtube.com/watch?v=hoNb6HuNmU0",
    "happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
    "ecstatic": "https://www.youtube.com/watch?v=3GwjfUFyY6M"
}

def analyze_emotion():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 嘗試開啟攝影機
    if not cap.isOpened():
        return None, "攝影機開啟失敗，可能被佔用或無權限"
    
    ret, frame = cap.read()
    cap.release()  # 釋放攝影機
    
    if not ret:
        return None, "無法讀取影像"
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換格式
    
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion'], None
    except Exception as e:
        return None, str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect_face')  # ✅ 確保這個路由名稱正確
def detect_face():
    emotion, error = analyze_emotion()
    if error:
        return jsonify({"error": error})
    return jsonify({"emotion": emotion})

@app.route('/get_music')
def get_music():
    emotion = request.args.get('emotion')
    if emotion in emotion_music:
        return jsonify({"emotion": emotion, "music": emotion_music[emotion]})
    return jsonify({"emotion": "unknown", "music": None})

@app.route('/voice_emotion')
def voice_emotion():
    text = request.args.get('text')
    translator = googletrans.Translator()
    translated_text = translator.translate(text, dest='en').text  # 翻譯成英文分析
    sentiment = TextBlob(translated_text).sentiment.polarity
    
    if sentiment < -0.3:
        emotion = "sad"
    elif -0.3 <= sentiment < 0.1:
        emotion = "annoyed"
    elif 0.1 <= sentiment < 0.5:
        emotion = "happy"
    else:
        emotion = "ecstatic"
    
    return jsonify({"emotion": emotion, "music": emotion_music[emotion]})

if __name__ == "__main__":
    app.run(debug=True)
