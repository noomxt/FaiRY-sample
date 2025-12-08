from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import recommend  # 미현이 데이터 모듈 연동


class ImageEmotionAnalyzer:
    def __init__(self):
        print("AI 모델(ViT) 로딩 중... (시간이 좀 걸릴 수 있습니다)")
        # 모델은 클래스 생성 시 한 번만 로딩 (속도 최적화)
        self.model = ViTForImageClassification.from_pretrained("trpakov/vit-face-expression")
        self.processor = ViTImageProcessor.from_pretrained("trpakov/vit-face-expression")

        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        # 우리 프로젝트(미현 데이터)에 맞는 한글 키워드로 매핑
        self.emotion_map = {
            'Angry': '분노',
            'Disgust': '분노',  # 혐오 -> 분노로 통합
            'Fear': '무서움',
            'Happy': '기쁨',
            'Sad': '슬픔',
            'Surprise': '기쁨',  # 놀람 -> 기쁨으로 통합
            'Neutral': '평온'
        }

    def analyze(self, image_path):
        """
        이미지 경로를 받아서 -> 감정 분석 -> 추천 결과까지 반환
        """
        try:
            # 1. 이미지 열기
            image = Image.open(image_path).convert("RGB")

            # 2. 전처리 및 추론
            inputs = self.processor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class = logits.argmax(-1).item()

            # 3. 결과 변환 (영어 -> 한글)
            emotion_eng = self.emotion_labels[predicted_class]
            emotion_kor = self.emotion_map.get(emotion_eng, '평온')

            # 4. 미현이 모듈에서 추천 데이터 가져오기
            reco_data = recommend.get_recommendation(emotion_kor)

            return {
                "emotion_eng": emotion_eng,
                "emotion": emotion_kor,
                "recommendation": reco_data
            }

        except Exception as e:
            print(f"이미지 분석 실패: {e}")
            return {"emotion": "에러", "recommendation": "분석 실패"}


# 테스트용 코드 (이 파일 직접 실행할 때만 작동)
if __name__ == "__main__":
    analyzer = ImageEmotionAnalyzer()
    # 테스트할 때는 경로를 직접 넣어서 확인
    result = analyzer.analyze("test_image.jpg")
    print(result)

