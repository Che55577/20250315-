from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from deepface import DeepFace
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)  # 允許前端存取 API

YOUTUBE_API_KEY = "你的 YouTube API 金鑰"

def search_youtube_music(emotion):
    query_map = {
        "happy": "開心音樂 playlist",
        "sad": "悲傷音樂 playlist",
        "angry": "放鬆音樂 playlist",
        "surprise": "快樂音樂 playlist",
        "neutral": "輕音樂 playlist"
    }
    query = query_map.get(emotion, "輕音樂 playlist")
    
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query, part="snippet", maxResults=1, type="video"
    ).execute()
    
    if search_response["items"]:
        return search_response["items"][0]["id"]["videoId"]
    return None

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["image"]
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
    emotion = result[0]["dominant_emotion"]
    
    return jsonify({"emotion": emotion})

@app.route("/search_music", methods=["GET"])
def search_music():
    emotion = request.args.get("emotion")
    video_id = search_youtube_music(emotion)
    
    return jsonify({"videoId": video_id})

if __name__ == "__main__":
    app.run(debug=True)
