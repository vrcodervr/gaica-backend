# config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    GAICA Configuration File
    """

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "gaica_secret_key_2026")

    # Gemini API Key
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    DEBUG = True
    TESTING = False

    # MongoDB Configuration
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/gaica_db")

    # Upload Configuration
    UPLOAD_FOLDER = "static/uploads"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "pdf",
        "docx",
        "txt"
    }

    # Session Configuration
    SESSION_PERMANENT = False

    # Chatbot Configuration
    CHATBOT_NAME = "GAICA AI"
    CHATBOT_VERSION = "1.0"
    CHATBOT_LANGUAGE = "English"

    # Security
    PASSWORD_MIN_LENGTH = 8

    # Fake News Module
    FAKE_NEWS_ENABLED = True

    # Scam Detection Module
    SCAM_DETECTION_ENABLED = True

    # Emergency Module
    EMERGENCY_ENABLED = True

    # Application Information
    APP_NAME = "GAICA"
    APP_VERSION = "1.0"

    # Time Zone
    TIMEZONE = "Asia/Kolkata"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True