
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the emotion detector interface."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """Analyze submitted text and display emotion scores."""
    text_to_analyze = request.values.get("textToAnalyze", "").strip()

    if not text_to_analyze:
        return "Please enter some text to analyze.", 400

    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return "Emotion analysis service is unavailable. Please try again.", 503

    scores = ", ".join(
        f"{emotion}: {result[emotion]}"
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )

    return (
        f"For the given statement, the system response is "
        f"{scores}. The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
