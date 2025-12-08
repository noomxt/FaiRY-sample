"""
환경 설정 모듈
-------------
프로젝트 전체에서 사용하는 경로(Path), 감정 리스트, 
상수 값들을 한곳에서 관리하는 파일입니다.
"""
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

EMOTION_FILES = {
    "기쁨": os.path.join(DATA_DIR, 'data_joy.csv'),
    "슬픔": os.path.join(DATA_DIR, 'data_sad.csv'),
    "분노": os.path.join(DATA_DIR, 'data_anger.csv'),
    "무서움": os.path.join(DATA_DIR, 'data_fear.csv'),
    "평온": os.path.join(DATA_DIR, 'data_peace.csv')
}

EMOTIONS = list(EMOTION_FILES.keys())