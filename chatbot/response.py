# chatbot/response.py

RESPONSES = {

    "greeting": (
        "👋 Hello! Welcome to GAICA.\n"
        "I am your AI Crisis Assistant.\n"
        "How can I help you today?"
    ),

    "scam": (
        "⚠️ Scam Alert!\n"
        "- Never share your OTP or password.\n"
        "- Do not click on unknown links.\n"
        "- Verify the caller before making any payment.\n"
        "- Contact your bank immediately if money has been deducted."
    ),

    "fake_news": (
        "📰 Fake News Alert!\n"
        "- Verify information from trusted sources.\n"
        "- Do not forward unverified messages.\n"
        "- Check official government or news websites."
    ),

    "emergency": (
        "🚨 Emergency Detected!\n"
        "If this is a real emergency:\n"
        "- Call the nearest Police Station.\n"
        "- Contact Ambulance Services.\n"
        "- Stay calm and share your live location with trusted people."
    ),

    "goodbye": (
        "👋 Thank you for using GAICA.\n"
        "Stay Safe! Have a great day."
    ),

    "unknown": (
        "❓ Sorry, I couldn't understand your request.\n"
        "Please try asking in another way.\n\n"
        "Example:\n"
        "- Scam\n"
        "- Fake News\n"
        "- Emergency\n"
        "- Help"
    )
}


def get_response(intent):
    """
    Return chatbot response according to detected intent.
    """
    return RESPONSES.get(intent, RESPONSES["unknown"])