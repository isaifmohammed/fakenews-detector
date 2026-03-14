from flask import Flask, render_template, request, jsonify
from src.detector import analyze_text
from src.scraper import get_text_from_input
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news")
def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=12&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_input = data.get("text", "")

    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    article = get_text_from_input(user_input)

    if not article["success"]:
        return jsonify({"error": article["error"]}), 400

    result = analyze_text(article["text"])

    return jsonify({
        "title": article["title"],
        "source": article["source"],
        "authors": article["authors"],
        "publish_date": article["publish_date"],
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "label": result["label"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))