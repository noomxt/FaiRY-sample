
=======
# 🧚 FaiRY Sample: Web Service Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Type](https://img.shields.io/badge/Type-Sample_Usage-green)
![Library](https://img.shields.io/badge/Library-FaiRY-orange)

> **"FaiRY 라이브러리를 활용한 감정 케어 웹 서비스 예제입니다."**
>
> 이 리포지토리는 [FaiRY Library](https://github.com/noomxt/FaiRY)를 **Import**하여 실제로 어떻게 활용할 수 있는지 보여주는 **Sample Usage Project**입니다.

---

## 📂 프로젝트 소개 (Introduction)

이 프로젝트는 **FaiRY (Face and text Analysis & Intelligent Recommendation for You)** 라이브러리의 핵심 모듈을 사용하여 구축된 웹 애플리케이션입니다.

**FaiRY 라이브러리**의 `image_emotion` 및 `text_emotion` 모듈을 가져와(Import), 사용자의 웹캠 이미지와 일기 텍스트를 분석하고 결과를 화면에 출력하는 **Full-stack 예제**를 구현했습니다.

## 💻 코드 예시 (Code Example)

FaiRY 라이브러리를 사용하여 감정을 분석하는 핵심 코드입니다.

```python
# app.py (Sample Code)

from fairy.image_emotion import FaceAnalyzer
from fairy.text_emotion import TextAnalyzer
from fairy.recommendation import Recommender

# 1. 얼굴 표정 분석 (Face Analysis)
face_result = FaceAnalyzer.predict(image_file)

# 2. 텍스트 감정 분석 (Text Analysis)
text_result = TextAnalyzer.analyze(user_diary_text)

# 3. 맞춤형 활동 및 음악 추천 (Recommendation)
final_recommendation = Recommender.get_suggestion(face_result, text_result)

print(f"Detected Emotion: {face_result}")
print(f"Recommended Song: {final_recommendation['song']}")