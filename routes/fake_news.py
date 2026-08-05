# routes/fake_news.py

from flask import Blueprint, render_template, request, jsonify, current_app, session
from google import genai
from pymongo import MongoClient
from datetime import datetime
from utils.decorators import login_required

fake_news = Blueprint("fake_news", __name__)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# Local (offline) keyword-based fake news detector
# Used as fallback when Gemini API is unavailable
# -----------------------------
FAKE_NEWS_KEYWORDS = [
    "forward this message", "share before it is deleted", "government hiding",
    "doctors don't want you to know", "miracle cure", "breaking: shocking truth",
    "you won't believe", "click to know shocking", "this will be deleted soon",
    "urgent share", "must forward", "whatsapp forward", "unverified sources say",
    "secret the media won't tell you", "100% true no fake", "share to all groups"
]

RELIABLE_INDICATORS = [
    "according to reuters", "according to pti", "official statement",
    "government press release", "verified by", "as reported by",
    "ministry of", "official website"
]


def local_fake_news_analysis(news_text):
    """
    Simple offline fake news analysis using keyword matching.
    Returns a markdown-formatted string similar to what the AI would return.
    """
    text = news_text.lower()

    matched_fake = [kw for kw in FAKE_NEWS_KEYWORDS if kw in text]
    matched_reliable = [kw for kw in RELIABLE_INDICATORS if kw in text]

    if len(matched_fake) >= 2 and not matched_reliable:
        credibility = "Likely Fake / Misleading"
    elif matched_fake and not matched_reliable:
        credibility = "Suspicious"
    elif matched_reliable and not matched_fake:
        credibility = "Likely Reliable"
    else:
        credibility = "Uncertain - Needs Manual Verification"

    if matched_fake:
        keyword_list = ", ".join(matched_fake)
        analysis = (
            f"The content contains common misinformation patterns such as: **{keyword_list}**. "
            f"Messages urging urgent forwarding, claiming hidden secrets, or lacking any official "
            f"source citation are frequently associated with fake or misleading news."
        )
    elif matched_reliable:
        analysis = (
            "The content references official sources or established news agencies, which is a "
            "positive sign of credibility. However, always cross-check with multiple trusted outlets."
        )
    else:
        analysis = (
            "No strong fake-news or reliability indicators were detected. This does not confirm "
            "the news is true or false — please verify manually from trusted sources before sharing."
        )

    safety_points = (
        "- Cross-check the news on official government or reputed news websites.\n"
        "- Check the source and publishing date before sharing.\n"
        "- Avoid forwarding messages that ask for urgent, unverified sharing.\n"
        "- Use fact-checking sites like PIB Fact Check for Indian news."
    )

    result = (
        f"**CREDIBILITY:** {credibility}\n\n"
        f"**ANALYSIS:**\n{analysis}\n\n"
        f"**RECOMMENDATIONS:**\n{safety_points}"
    )

    return result, credibility


# -----------------------------
# Render the Fake News Detection page
# -----------------------------
@fake_news.route("/fake-news", methods=["GET"])
@login_required
def fake_news_page():
    return render_template("fake_news.html")


# -----------------------------
# AI Fake News Analysis API
# -----------------------------
@fake_news.route("/fake-news", methods=["POST"])
@login_required
def analyze_fake_news():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No data received."
            }), 400

        news_text = data.get("news_text", "").strip()

        if not news_text:
            return jsonify({
                "status": "error",
                "message": "Please provide news content to analyze."
            }), 400

        api_key = current_app.config.get("GEMINI_API_KEY")
        credibility = "Unknown"

        # If API key missing/default, use local analysis directly
        if not api_key or "YOUR_ACTUAL_KEY" in api_key or "यहाँ" in api_key or "your" in api_key:
            ai_analysis, credibility = local_fake_news_analysis(news_text)
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = (
                    f"Analyze the following news/content for authenticity:\n\n"
                    f"Content: {news_text}\n\n"
                    f"Provide your evaluation strictly in English with three sections:\n"
                    f"1. CREDIBILITY: (Likely Reliable, Suspicious, or Likely Fake/Misleading)\n"
                    f"2. ANALYSIS: Explain clearly why this content appears reliable or suspicious.\n"
                    f"3. RECOMMENDATIONS: Give 3 quick, clear actionable bullet points on how the user should verify this."
                )

                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config={
                        'temperature': 0.3
                    }
                )

                ai_analysis = response.text

            except Exception as api_error:
                print(f"Gemini API error (falling back to local analysis): {str(api_error)}")
                ai_analysis, credibility = local_fake_news_analysis(news_text)

        # Save the report data and AI analysis into MongoDB
        try:
            db = get_db()
            db.fake_news_reports.insert_one({
                "user_email": session.get("email", "guest"),
                "news_text": news_text,
                "credibility": credibility,
                "ai_analysis": ai_analysis,
                "timestamp": datetime.utcnow()
            })
        except Exception as db_error:
            print(f"Fake news report save error: {str(db_error)}")

        return jsonify({
            "status": "success",
            "message": "News analyzed successfully.",
            "ai_analysis": ai_analysis
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred during analysis: {str(e)}"
        }), 500