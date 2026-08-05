# routes/scam.py

from flask import Blueprint, render_template, request, jsonify, current_app, session
from google import genai
from pymongo import MongoClient
from datetime import datetime
from utils.decorators import login_required

scam = Blueprint("scam", __name__)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# Local (offline) keyword-based scam detector
# Used as a fallback when Gemini API is unavailable
# -----------------------------
SCAM_KEYWORDS = [
    "otp", "one time password", "urgent", "click this link", "click here",
    "verify your account", "bank account block", "lottery", "prize",
    "you have won", "congratulations you", "free gift", "limited time offer",
    "kyc update", "kyc expire", "refund", "tax refund", "electricity bill due",
    "account suspended", "confirm your details", "password expired",
    "share your pin", "share your card number", "cvv", "act now",
    "immediate action required", "government scheme", "investment double money",
    "job offer without interview", "work from home earn", "crypto guaranteed return"
]


def local_scam_analysis(scam_type, description, location):
    """
    Simple offline scam analysis using keyword matching.
    Returns a markdown-formatted string similar to what the AI would return.
    """
    text = description.lower()
    matched_keywords = [kw for kw in SCAM_KEYWORDS if kw in text]

    if len(matched_keywords) >= 2:
        risk_level = "High"
    elif len(matched_keywords) == 1:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if matched_keywords:
        keyword_list = ", ".join(matched_keywords)
        analysis = (
            f"The message contains common scam-related patterns such as: **{keyword_list}**. "
            f"Messages that ask you to click unknown links, share OTP/PIN/CVV, or claim urgent "
            f"account action are frequently used in phishing and fraud attempts."
        )
    else:
        analysis = (
            "No well-known scam keywords were detected in the message. However, always stay "
            "cautious with unexpected messages, unknown senders, or requests for personal/financial information."
        )

    safety_points = (
        "- Never share your OTP, PIN, CVV, or password with anyone.\n"
        "- Do not click on unknown or suspicious links.\n"
        "- Verify directly with the official bank/company using contact details from their official website.\n"
        "- If money has already been deducted, contact your bank and report to cybercrime.gov.in immediately."
    )

    result = (
        f"**RISK LEVEL:** {risk_level}\n\n"
        f"**ANALYSIS:**\n{analysis}\n\n"
        f"**SAFETY INSTRUCTIONS:**\n{safety_points}"
    )

    return result, risk_level


# -----------------------------
# Render the Scam Detection page
# -----------------------------
@scam.route("/scam")
@login_required
def scam_page():
    return render_template("scam.html")


# -----------------------------
# AI Scam Analysis and Reporting API
# -----------------------------
@scam.route("/report-scam", methods=["POST"])
@login_required
def report_scam():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No data received."
            }), 400

        scam_type = data.get("type", "").strip()
        description = data.get("description", "").strip()
        location = data.get("location", "").strip()

        if not description:
            return jsonify({
                "status": "error",
                "message": "Please provide a description or message to analyze."
            }), 400

        # Fetch the Gemini API key from configuration
        api_key = current_app.config.get("GEMINI_API_KEY")
        risk_level = "Unknown"

        # If API key is missing/default, use local analysis directly
        if not api_key or "YOUR_ACTUAL_KEY" in api_key or "यहाँ" in api_key or "your" in api_key:
            ai_analysis, risk_level = local_scam_analysis(scam_type, description, location)
        else:
            try:
                # Initialize the Google GenAI Client
                client = genai.Client(api_key=api_key)

                # Prompt engineering to evaluate the potential fraud
                prompt = (
                    f"Analyze the following potential scam attempt:\n"
                    f"Reported Type: {scam_type}\n"
                    f"Details/Message content: {description}\n"
                    f"Location: {location}\n\n"
                    f"Provide your evaluation strictly in English with three sections:\n"
                    f"1. RISK LEVEL: (High, Medium, or Low)\n"
                    f"2. ANALYSIS: Explain clearly why this is likely a scam or fraud attempt.\n"
                    f"3. SAFETY INSTRUCTIONS: Give 3 quick, clear actionable bullet points on what the user should do next."
                )

                # Generate response using the standard gemini-2.0-flash model
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
                ai_analysis, risk_level = local_scam_analysis(scam_type, description, location)

        # Save the report data and AI analysis into MongoDB
        try:
            db = get_db()
            db.scam_reports.insert_one({
                "user_email": session.get("email", "guest"),
                "type": scam_type,
                "description": description,
                "location": location,
                "risk_level": risk_level,
                "ai_analysis": ai_analysis,
                "timestamp": datetime.utcnow()
            })
        except Exception as db_error:
            print(f"Scam report save error: {str(db_error)}")

        return jsonify({
            "status": "success",
            "message": "Scam analyzed successfully.",
            "ai_analysis": ai_analysis,
            "data": {
                "type": scam_type,
                "description": description,
                "location": location
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred during analysis: {str(e)}"
        }), 500