# chatbot/intent.py

def detect_intent(message):
    """
    Detect the user's intent based on keywords.
    """

    message = message.lower().strip()

    intents = {

        "greeting": [
            "hello", "hi", "hey", "namaste", "good morning",
            "good afternoon", "good evening"
        ],

        "scam": [
            "scam", "fraud", "otp", "bank", "upi",
            "phishing", "fake call", "cyber crime", "hack"
        ],

        "fake_news": [
            "fake news", "rumour", "rumor",
            "viral message", "news", "misinformation"
        ],

        "emergency": [
            "help", "emergency", "ambulance",
            "police", "fire", "hospital", "accident"
        ],

        "goodbye": [
            "bye", "goodbye", "see you", "exit"
        ]
    }

    # Check every intent
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in message:
                return intent

    return "unknown"