# routes/chatbot.py

from flask import Blueprint, render_template, request, jsonify, session, current_app
from chatbot.chatbot import chatbot_reply
from pymongo import MongoClient
from datetime import datetime
from utils.decorators import login_required

# Create Blueprint
chatbot = Blueprint("chatbot", __name__)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# Chat Page (GET) - Yahan par chatbot.html dikhega
# -----------------------------
@chatbot.route("/chatbot", methods=["GET"])
@login_required
def chatbot_page():
    return render_template("chatbot.html")


# -----------------------------
# Chat API (POST) - JS yahan message bhejega
# -----------------------------
@chatbot.route("/chat", methods=["POST"])
@login_required
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"status": "error", "reply": "Please enter a valid message."})

        reply = chatbot_reply(user_message)

        # Save chat history to MongoDB
        try:
            db = get_db()
            db.chat_history.insert_one({
                "user_email": session.get("email", "guest"),
                "message": user_message,
                "reply": reply,
                "timestamp": datetime.utcnow()
            })
        except Exception as db_error:
            print(f"Chat history save error: {str(db_error)}")

        return jsonify({"status": "success", "reply": reply})

    except Exception as e:
        return jsonify({"status": "error", "reply": "Something went wrong: " + str(e)})