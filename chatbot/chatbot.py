from chatbot.intent import detect_intent
from chatbot.response import get_response

def local_reply(user_message):
    """
    Local (offline) chatbot reply using keyword-based intent detection.
    Optimized for standalone usage without external dependencies.
    """
    if not user_message or not user_message.strip():
        return "Please enter a valid message."

    # Detect user intent based on keywords
    intent = detect_intent(user_message)
    
    # Get the appropriate response for the detected intent
    return get_response(intent)


def chatbot_reply(user_message):
    """
    Main chatbot entry point. Google Gemini API has been completely removed.
    It now routes all queries directly to the stable offline local response system.
    """
    try:
        # Directly use the local offline chatbot system to avoid any network or quota errors
        return local_reply(user_message)

    except Exception as e:
        # Catch any unexpected internal errors safely
        print(f"Chatbot processing error: {str(e)}")
        return "An internal server error occurred. Please try again."