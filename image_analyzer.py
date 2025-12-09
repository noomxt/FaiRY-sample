from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import tkinter as tk
from tkinter import filedialog
import config   # 추천과 CSV 매핑이 들어있는 파일

# 감정 라벨 (FER2013 기준)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# 한국어 매핑
emotion_korean = {
    'Angry': '분노',
    'Disgust': '분노',
    'Fear': '공포',
    'Happy': '기쁨',
    'Sad': '슬픔',
    'Surprise': '기쁨',
    'Neutral': '평온'
}

class EmotionAnalyzer:
    def __init__(self):
        self.model = ViTForImageClassification.from_pretrained("trpakov/vit-face-expression")
        self.processor = ViTImageProcessor.from_pretrained("trpakov/vit-face-expression")

    def predict(self, img_path):
        image = Image.open(img_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = logits.argmax(-1).item()

        emotion_eng = emotion_labels[predicted_class]
        emotion_kor = emotion_korean[emotion_eng]

        return {
            "emotion_eng": emotion_eng,
            "emotion_kor": emotion_kor,
            "logits": logits[0].tolist()
        }

def main():
    # 파일 탐색기 열기
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="분석할 이미지를 선택하세요",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        print("이미지를 선택하지 않았습니다.")
        return

    analyzer = EmotionAnalyzer()
    result = analyzer.predict(file_path)

    print("\n=== 감정 분석 결과 ===")
    for i, label in enumerate(emotion_labels):
        print(f"{emotion_korean[label]}: {result['logits'][i]:.2f}")
    print(f"\n최종 감정: {result['emotion_kor']}")

    # config.py에서 추천 가져오기
    rec = config.get_recommendations(result['emotion_kor'])
    print("\n=== 추천 활동 & 노래 ===")
    print(f"추천 활동(act): {rec['act']}")
    print(f"추천 노래(song): {rec['song']}")

if __name__ == "__main__":
    main()
