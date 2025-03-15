# Write your code here :-)
import tkinter as tk
from tkinter import messagebox
from deepface import DeepFace
import cv2
import webbrowser

# 對應情緒與 YouTube 音樂連結（簡單版本）
emotion_music_links = {
    "happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Happy
    "sad": "https://www.youtube.com/watch?v=ho9rZjlsyYY",     # Sad
    "angry": "https://www.youtube.com/watch?v=btPJPFnesV4",   # Angry
    "surprise": "https://www.youtube.com/watch?v=0KSOMA3QBU0",# Surprise
    "fear": "https://www.youtube.com/watch?v=VQ4qRCWcvL8",    # Fear
    "neutral": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"  # Neutral
}

# 進行情緒辨識的函式
def detect_emotion():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            # 偵測情緒
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            print(f"偵測到的情緒：{emotion}")

            messagebox.showinfo("辨識結果", f"您現在的情緒是：{emotion}")

            # 開啟對應的音樂
            link = emotion_music_links.get(emotion, None)
            if link:
                webbrowser.open(link)
            else:
                messagebox.showerror("錯誤", "找不到對應的音樂連結")

        else:
            messagebox.showerror("錯誤", "無法擷取相機影像")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))


# GUI 介面設定
def main():
    window = tk.Tk()
    window.title("情緒化音樂播放器")
    window.geometry("400x200")

    label = tk.Label(window, text="嘿，您今天心情如何？", font=("Arial", 16))
    label.pack(pady=20)

    start_button = tk.Button(window, text="開始使用", font=("Arial", 14), command=detect_emotion)
    start_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
