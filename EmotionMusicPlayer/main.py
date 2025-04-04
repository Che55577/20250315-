from flask import Flask, render_template, request, jsonify
from deepface import DeepFace

import cv2
import yt_dlp
import os
import googletrans
from textblob import TextBlob

app = Flask(__name__)

# 設定 YouTube 播放對應的情緒與音樂
emotion_music = {
    "angry": "https://www.youtube.com/watch?v=8jzDnsjYv9A",  # Linkin Park - Numb
    "annoyed": "https://www.youtube.com/watch?v=LRP8d7hhpoQ",  # Billie Eilish - Bad Guy
    "sad": "https://www.youtube.com/watch?v=hoNb6HuNmU0",  # Adele - Someone Like You
    "happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Pharrell Williams - Happy
    "depressed": "https://www.youtube.com/watch?v=4N3N1MlvVc4"  # Gary Jules - Mad World (厭世)
}

def detect_emotion():
    cap = cv2.VideoCapture(0)  # 開啟鏡頭
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None
    
    try:
        result = DeepFace.analyze(frame, actions=['emotion'])
        return result[0]['dominant_emotion']
    except Exception as e:
        print("DeepFace 錯誤:", e)
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect')
def detect():
    emotion = detect_emotion()
    if emotion and emotion in emotion_music:
        return jsonify({"emotion": emotion, "music": emotion_music[emotion]})
    return jsonify({"emotion": "unknown", "music": None})

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
    
    if sentiment < -0.5:
        emotion = "depressed"  # 極度負面 -> 厭世
    elif -0.5 <= sentiment < -0.2:
        emotion = "sad"  # 負面 -> 憂鬱
    elif -0.2 <= sentiment < 0.2:
        emotion = "annoyed"  # 中性偏負面 -> 煩躁
    elif 0.2 <= sentiment < 0.5:
        emotion = "happy"  # 正面 -> 開心
    else:
        emotion = "angry"  # 超高分數 -> 憤怒 (因為極端正向語氣可能帶有諷刺)

    return jsonify({"emotion": emotion, "music": emotion_music[emotion]})

if __name__ == "__main__":
    app.run(debug=True)
