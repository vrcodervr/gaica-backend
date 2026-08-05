from flask import Flask, render_template
from config import Config
from utils.decorators import login_required
from pymongo import MongoClient
from flask import session

# Import Blueprints
from routes.auth import auth
from routes.chatbot import chatbot
from routes.scam import scam
from routes.fake_news import fake_news
from routes.emergency import emergency
from routes.admin import admin

# Create Flask App
app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)

# Secret Key
app.secret_key = app.config["SECRET_KEY"]

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(chatbot)
app.register_blueprint(scam)
app.register_blueprint(fake_news)
app.register_blueprint(emergency)
app.register_blueprint(admin)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# Dashboard (with stats)
# -----------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    try:
        db = get_db()
        user_email = session.get("email", "guest")

        stats = {
            "total_chats": db.chat_history.count_documents({"user_email": user_email}),
            "total_scams": db.scam_reports.count_documents({"user_email": user_email}),
            "total_fake_news": db.fake_news_reports.count_documents({"user_email": user_email}),
            "total_emergencies": db.emergency_reports.count_documents({"user_email": user_email})
        }
    except Exception as e:
        print(f"Dashboard stats error: {str(e)}")
        stats = {
            "total_chats": 0,
            "total_scams": 0,
            "total_fake_news": 0,
            "total_emergencies": 0
        }

    return render_template("dashboard.html", stats=stats)


# -----------------------------
# 404 Error Handler
# -----------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# -----------------------------
# 500 Error Handler
# -----------------------------
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)