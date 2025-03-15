from deepface import DeepFace
import cv2
import os
import yt_dlp
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 設定 YouTube 播放對應的情緒與音樂
emotion_music = {
    "happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Pharrell Williams - Happy
    "sad": "https://www.youtube.com/watch?v=hoNb6HuNmU0",  # Adele - Someone Like You
    "angry": "https://www.youtube.com/watch?v=8jzDnsjYv9A",  # Linkin Park - Numb
    "surprise": "https://www.youtube.com/watch?v=Q-GLuydiMe4"  # Owl City - Fireflies
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
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect')
def detect():
    emotion = detect_emotion()
    if emotion in emotion_music:
        return jsonify({"emotion": emotion, "music": emotion_music[emotion]})
    return jsonify({"emotion": "unknown", "music": None})

if __name__ == "__main__":
    app.run(debug=True)
