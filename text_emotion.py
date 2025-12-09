import re
import csv
import os
import random
from difflib import SequenceMatcher
from config import EMOTION_FILES

class TextEmotionAnalyzer:
    def __init__(self):
        print(f"\n[System] 현재 실행 위치: {os.getcwd()}")
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

        for emotion, original_path in EMOTION_FILES.items():
            final_path = original_path
            
            if not os.path.exists(original_path):
                filename = os.path.basename(original_path) 
                candidates = [
                    os.path.join('data', filename),              
                    os.path.join('..', 'data', filename),        
                    os.path.join('.', 'fairy', 'data', filename)
                ]
                
                found = False
                for path in candidates:
                    if os.path.exists(path):
                        final_path = path
                        found = True
                        print(f"경로 자동 보정 성공: {original_path} -> {final_path}")
                        break
                
                if not found:
                    print(f"실패: '{filename}'을 찾을 수 없습니다. (패치 데이터 사용)")
                    self.emotion_keywords[emotion] = patch_data.get(emotion, [])
                    continue

            success = False
            for enc in ['utf-8-sig', 'cp949']:
                try:
                    with open(final_path, 'r', encoding=enc) as f:
                        reader = csv.reader(f)
                        count = 0
                        for row in reader:
                            if not row: continue
                            
                            if len(row) >= 3:
                                category = row[1].strip()
                                content = row[2].strip()
                                if category == "comment":
                                    self.emotion_keywords[emotion].append(content)
                                elif category == "song":
                                    self.recommendations[emotion]["song"].append(content)
                                elif category == "act":
                                    self.recommendations[emotion]["act"].append(content)
                                count += 1
                            elif len(row) >= 1:
                                self.emotion_keywords[emotion].append(row[0].strip())
                                count += 1
                        
                        combined = self.emotion_keywords[emotion] + patch_data.get(emotion, [])
                        self.emotion_keywords[emotion] = list(set(combined))
                        
                        print(f"[{emotion}] 로드 완료 ({count}개)")
                        success = True
                        break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    pass
            
            if not success:
                print(f"읽기 실패: {final_path}")
                self.emotion_keywords[emotion] = patch_data.get(emotion, [])

    def preprocess_text(self, text):
        text = re.sub(r'(.)\1{2,}', r'\1\1', text) 
        return "".join(text.split())

    def _check_slang(self, text):
        slang_list = ["시발", "씨발", "개새", "ㅈㄴ", "존나", "미친", "ㅅㅂ", "쌰갈", "씹"]
        for slang in slang_list:
            if slang in text: return True
        return False

    def _calculate_similarity(self, input_text, keyword):
        return SequenceMatcher(None, input_text, keyword).ratio()

    def analyze(self, text):
        processed_text = self.preprocess_text(text)
        scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        
        if self._check_slang(processed_text):
            if "분노" in scores: scores["분노"] += 20 

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
        if max_score == 0: return "평온"
        
        top_emotions = [k for k, v in scores.items() if v == max_score]
        if "슬픔" in top_emotions: return "슬픔"
        if "공포" in top_emotions: return "공포"
        return top_emotions[0]

    def get_recommendation(self, sentiment):
        rec_data = self.recommendations.get(sentiment, self.recommendations.get("평온"))
        song = "추천 노래 없음"
        act = "휴식하기"
        if rec_data:
            if rec_data.get("song"): song = random.choice(rec_data["song"])
            if rec_data.get("act"): act = random.choice(rec_data["act"])
        return {"song": song, "todo": act}

if __name__ == "__main__":
    print("\n---테스트 실행 ---")
    analyzer = TextEmotionAnalyzer()
    
    test_inputs = ["진짜 빡친다", "너무 행복해", "아무 생각이 없다"]
    for text in test_inputs:
        result = analyzer.analyze(text)
        rec = analyzer.get_recommendation(result)
        print(f"\n입력: {text}")
        print(f"감정: [{result}]")
        print(f"추천: {rec['song']} / {rec['todo']}")

    
    
    



    

