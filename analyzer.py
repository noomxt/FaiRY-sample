import re
import csv
import os
import sys
import tkinter as tk 
from tkinter import messagebox
from config import EMOTION_FILES
import random
from difflib import SequenceMatcher

class TextEmotionAnalyzer:
    def __init__(self):
        print("감정 분석기 가동...")
        self.emotion_keywords = self._load_data()

    def _load_data(self):
        data = {}
        patch_data = {
            "분노": ["빡친다", "돌겟네", "개빡", "킹받네", "열받아", "뚜껑 열린다", "딥빡", "씨", "시발"],
            "슬픔": ["광광", "롬곡", "힝", "시무룩", "흑흑", "ㅠ", "ㅜ"],
            "기쁨": ["굳", "개꿀", "나이스", "쪼아", "아이조아", "굿"],
        }

        for emotion, file_path in EMOTION_FILES.items():
            loaded_keywords = []
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if not row: continue
                            if len(row) >= 3:
                                word = row[2].strip()
                                if word != "content": loaded_keywords.append(word)
                            elif len(row) >= 1:
                                word = row[0].strip()
                                if word != "content": loaded_keywords.append(word)
                except Exception:
                    pass 

            final_list = loaded_keywords + patch_data.get(emotion, [])
            data[emotion] = list(set(final_list)) 
            
        return data

    def preprocess_text(self, text):
        text = re.sub(r'(.)\1{2,}', r'\1\1', text) 
        return "".join(text.split())

    def _calculate_similarity(self, input_text, keyword):
        return SequenceMatcher(None, input_text, keyword).ratio()

    def _check_slang(self, text):
        slang_list = ["시발", "씨발", "개새", "ㅈㄴ", "존나", "미친", "ㅅㅂ","쌰갈","싸갈","사갈","씹","쓰발"]
        for slang in slang_list:
            if slang in text:
                return True
        return False

    def analyze_text(self, text):
        processed_text = self.preprocess_text(text)
        print(f"입력: {processed_text}")
        
        scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        
        if self._check_slang(processed_text):
            scores["분노"] += 20 
            print("욕설 감지: 분노 점수 +20 (가중치)")

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
        if "피곤함" in top_emotions: return "피곤함"
        
        return top_emotions[0]

    def get_matching_results(self, sentiment):
        recommendations = {
            "기쁨": [
                {"song": "NewJeans - Hype Boy", "todo": "친구들과 번개 모임 잡기"},
                {"song": "Pharrell Williams - Happy", "todo": "맛있는 디저트 사먹기"},
                {"song": "Bruno Mars - Uptown Funk", "todo": "거울 보고 춤 한번 추기"},
                {"song": "Day6 - 한 페이지가 될 수 있게", "todo": "오늘의 기분 일기 쓰기"},
                {"song": "Red Velvet - 빨간 맛", "todo": "시원한 음료수 마시며 산책"}
            ],
            "슬픔": [
                {"song": "IU - 밤편지", "todo": "따뜻한 차 한 잔 마시기"},
                {"song": "박효신 - 야생화", "todo": "슬픈 영화 보며 실컷 울기"},
                {"song": "폴킴 - 모든 날, 모든 순간", "todo": "포근한 이불 속에서 쉬기"},
                {"song": "이하이 - 한숨", "todo": "친구에게 전화해 하소연하기"},
                {"song": "김광석 - 서른 즈음에", "todo": "조용한 카페에서 생각 정리"}
            ],
            "분노": [
                {"song": "Imagine Dragons - Believer", "todo": "심호흡 크게 10번 하기"},
                {"song": "Eminem - Lose Yourself", "todo": "베개에 소리 지르기"},
                {"song": "Linkin Park - Faint", "todo": "땀 날 때까지 달리기"},
                {"song": "2NE1 - 내가 제일 잘 나가", "todo": "매운 떡볶이 먹기"},
                {"song": "G-Dragon - 삐딱하게", "todo": "이면지에 낙서하고 찢어버리기"}
            ],
            "피곤함": [
                {"song": "Jaurim - 스물다섯, 스물하나", "todo": "따뜻한 물로 반신욕"},
                {"song": "10cm - 스토커", "todo": "핸드폰 끄고 30분 낮잠"},
                {"song": "Zion.T - 꺼내 먹어요", "todo": "비타민/영양제 챙겨 먹기"},
                {"song": "백예린 - Square", "todo": "가벼운 스트레칭"},
                {"song": "성시경 - 두 사람", "todo": "눈 감고 10분 휴식"}
            ],
            "무서움": [
                {"song": "Gaho - 시작", "todo": "가족/친구 목소리 듣기"},
                {"song": "BTS - Dynamite", "todo": "무한도전 같은 예능 보기"},
                {"song": "Twice - Cheer Up", "todo": "따뜻한 우유 마시기"},
                {"song": "Disney OST", "todo": "귀여운 고양이 영상 보기"},
                {"song": "Bolbbalgan4 - 여행", "todo": "이불 꼭 덮고 안정 취하기"}
            ],
            "평온": [
                {"song": "Yiruma - River Flows In You", "todo": "읽다 만 책 읽기"},
                {"song": "Joe Hisaishi - Summer", "todo": "창문 열고 환기하기"},
                {"song": "Lofi Girl", "todo": "내일 할 일 정리하기"},
                {"song": "Depapepe - Start", "todo": "책상 정리하기"},
                {"song": "Maroon 5 - Sunday Morning", "todo": "향긋한 커피 마시기"}
            ]
        }
        target_list = recommendations.get(sentiment, recommendations["평온"])
        return random.choice(target_list)

def run_gui():
    try:
        analyzer = TextEmotionAnalyzer()
        window = tk.Tk()
        window.title("FaiRY - 감정 분석기")
        window.geometry("400x500")

        lbl_title = tk.Label(window, text="오늘의 기분을 적어주세요!", font=("맑은 고딕", 14, "bold"))
        lbl_title.pack(pady=20)

        entry_text = tk.Entry(window, width=30, font=("맑은 고딕", 12))
        entry_text.pack(pady=10)

        lbl_result = tk.Label(window, text="결과가 여기 나타납니다.", font=("맑은 고딕", 11), justify="center")
        lbl_result.pack(pady=20)

        def on_click():
            user_input = entry_text.get()
            if not user_input.strip(): return
            
            sentiment = analyzer.analyze_text(user_input)
            recommendation = analyzer.get_matching_results(sentiment)
            
            result_text = f"분석된 감정: [{sentiment}]\n\n추천 노래: {recommendation['song']}\n추천 할 일: {recommendation['todo']}"
            lbl_result.config(text=result_text, fg="blue")

        btn_analyze = tk.Button(window, text="분석하기", command=on_click, bg="lightblue")
        btn_analyze.pack(pady=10)
        
        window.mainloop()
    except Exception as e:
        print(f"에러: {e}")

if __name__ == "__main__":
    run_gui()