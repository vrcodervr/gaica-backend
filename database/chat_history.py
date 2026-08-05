from datetime import datetime
from pymongo import MongoClient

# Initialize MongoDB Connection securely using local server
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["gaica_db"]
    chats_collection = db["chats"]
except Exception as conn_error:
    print(f"MongoDB Connection initialization error: {str(conn_error)}")


def save_chat_message(user_id, prompt, response):
    """
    Saves the user's message and chatbot's response to the MongoDB database.
    """
    try:
        chat_document = {
            "user_id": user_id,
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.now(),
        }

        # Force write document into collection
        result = chats_collection.insert_one(chat_document)
        print(f"Chat saved successfully with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Error saving chat to database: {str(e)}")
        return None


def get_chat_history(user_id, limit=20):
    """
    Fetches the recent chat history for a specific user, sorted by timestamp.
    """
    try:
        history_cursor = (
            chats_collection.find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(limit)
        )

        history = []
        for chat in history_cursor:
            history.append(
                {
                    "prompt": chat["prompt"],
                    "response": chat["response"],
                    "timestamp": chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return history[::-1]
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return []