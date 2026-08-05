# utils/helper.py

from datetime import datetime
import uuid


def get_current_time():
    """
    Return current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_id():
    """
    Generate unique ID.
    """
    return str(uuid.uuid4())


def success_response(message, data=None):
    """
    Return success response.
    """
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(message):
    """
    Return error response.
    """
    return {
        "status": "error",
        "message": message
    }


def format_text(text):
    """
    Remove extra spaces from text.
    """
    if not text:
        return ""

    return text.strip()


def capitalize_text(text):
    """
    Capitalize first letter.
    """
    if not text:
        return ""

    return text.title()


def get_timestamp():
    """
    Return Unix Timestamp.
    """
    return int(datetime.now().timestamp())


if __name__ == "__main__":

    print("Current Time :", get_current_time())
    print("Unique ID    :", generate_id())
    print("Timestamp    :", get_timestamp())

    print(success_response("Success"))
    print(error_response("Something went wrong"))