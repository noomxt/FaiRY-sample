from flask import Flask, render_template, request
from image_analyzer import EmotionAnalyzer
from text_emotion import TextEmotionAnalyzer
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 객체 생성
image_analyzer = EmotionAnalyzer()
text_emotion = TextEmotionAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------
# 이미지 감정 분석 엔드포인트
# -------------------------
@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    file = request.files["file"]
    if file.filename == "":
        return "파일이 업로드되지 않았습니다."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    try:
        from PIL import Image, UnidentifiedImageError
        img = Image.open(filepath).convert("RGB")

        # JPG로 자동 변환
        converted_path = filepath.rsplit(".", 1)[0] + ".jpg"
        img.save(converted_path, "JPEG")

        # 저장된 이미지 표시용 경로 변환
        image_display_path = converted_path.replace("static/", "")
        image_display_path = "/static/" + image_display_path.split("static/")[-1]

    except UnidentifiedImageError:
        return render_template(
            "result.html",
            sentiment="",
            rec="",
            message="이미지 파일만 분석할 수 있어요! (JPG/PNG 권장)"
        )

    # ===== 이미지 감정 분석 결과 =====
    result = image_analyzer.analyze(converted_path)

    return render_template(
        "result.html",
        sentiment=result["emotion"],
        rec=result.get("recommendation", {}),
        message=""
    )

# -------------------------
# 텍스트 감정 분석 엔드포인트
# -------------------------
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    text = request.form['text']

    sentiment = text_emotion.analyze(text)               # 감정 분석
    rec = text_emotion.get_recommendation(sentiment)    # 추천 컨텐츠

    return render_template(
        "result.html",
        sentiment=sentiment,
        rec=rec,
        message=""
    )

# 파일 저장 폴더 설정
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(debug=True)
