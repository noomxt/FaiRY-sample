from flask import Flask, render_template, request
from analyzer import TextEmotionAnalyzer
from image_analyzer import ImageEmotionAnalyzer
import os
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = "static/uploads"

text_analyzer = TextEmotionAnalyzer()
image_analyzer = ImageEmotionAnalyzer()

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    song = ""
    todo = ""
    img_result = ""

    if request.method == "POST":
        if "user_input" in request.form:
            text = request.form["user_input"]
            sentiment = text_analyzer.analyze_text(text)
            recommendation = text_analyzer.get_matching_results(sentiment)

            result = sentiment
            song = recommendation["song"]
            todo = recommendation["todo"]

        elif "image" in request.files:
            image_file = request.files["image"]
            filepath = f"static/uploads/{image_file.filename}"
            image_file.save(filepath)

            img_result = image_analyzer.predict_image(filepath)

    return render_template("index.html", 
                           result=result, song=song, todo=todo,
                           img_result=img_result)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')