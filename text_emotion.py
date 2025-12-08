import re
import csv
import os
import random
from difflib import SequenceMatcher
from config import EMOTION_FILES

class TextEmotionAnalyzer:
    def __init__(self):
        self.emotion_keywords = {} 
        self.recommendations = {}
        
        self._load_all_data()

    def _load_all_data(self):
        patch_data = {
            "분노": ["빡친다", "돌겟네", "개빡", "킹받네", "열받아", "뚜껑 열린다", "딥빡", "씨", "시발", "짜증"],
            "슬픔": ["광광", "롬곡", "힝", "시무룩", "흑흑", "ㅠ", "ㅜ", "우울", "눈물"],
            "기쁨": ["굳", "개꿀", "나이스", "쪼아", "아이조아", "굿", "행복", "신나", "럭키비키"],
            "공포": ["무서워", "오싹", "ㄷㄷ", "소름", "후덜덜"],
            "평온": ["평온", "쏘쏘", "보통", "휴식", "멍"]
        }

        for emotion in EMOTION_FILES.keys():
            self.emotion_keywords[emotion] = []
            self.recommendations[emotion] = {"song": [], "act": []}

        for emotion, file_path in EMOTION_FILES.items():
            loaded_keywords = []
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if not row: continue
                            
                            if len(row) >= 3:
                                category = row[1].strip() 
                                content = row[2].strip()
                                
                                if category == "comment":
                                    loaded_keywords.append(content)
                                elif category == "song":
                                    self.recommendations[emotion]["song"].append(content)
                                elif category == "act":
                                    self.recommendations[emotion]["act"].append(content)
                                    
                except Exception as e:
                    print(f"[System] {emotion} 파일 로딩 중 오류 발생: {e}")

            final_keywords = loaded_keywords + patch_data.get(emotion, [])
            self.emotion_keywords[emotion] = list(set(final_keywords))

    def preprocess_text(self, text):
        text = re.sub(r'(.)\1{2,}', r'\1\1', text) 
        return "".join(text.split())

    def _check_slang(self, text):
        slang_list = ["시발", "씨발", "개새", "ㅈㄴ", "존나", "미친", "ㅅㅂ", "쌰갈", "씹","싸갈","사갈"]
        for slang in slang_list:
            if slang in text:
                return True
        return False

    def _calculate_similarity(self, input_text, keyword):
        return SequenceMatcher(None, input_text, keyword).ratio()

    def analyze(self, text):
        processed_text = self.preprocess_text(text)
        
        scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        
        if self._check_slang(processed_text):
            if "분노" in scores:
                scores["분노"] += 20 

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                clean_keyword = "".join(keyword.split())
                
                if clean_keyword in processed_text:
                    scores[emotion] += 100
                else:
                    similarity = self._calculate_similarity(processed_text, clean_keyword)
                    if similarity >= 0.6:
                        scores[emotion] += int(similarity * 50)

        max_score = max(scores.values())
        if max_score == 0: 
            return "평온"
        
        top_emotions = [k for k, v in scores.items() if v == max_score]
        
        if "슬픔" in top_emotions: return "슬픔"
        if "공포" in top_emotions: return "공포"
        
        return top_emotions[0]

    def get_recommendation(self, sentiment):
        rec_data = self.recommendations.get(sentiment, self.recommendations.get("평온"))
        
        song = "추천 노래 없음"
        act = "휴식하기"

        if rec_data:
            if rec_data["song"]:
                song = random.choice(rec_data["song"])
            if rec_data["act"]:
                act = random.choice(rec_data["act"])
        
        return {"song": song, "todo": act}