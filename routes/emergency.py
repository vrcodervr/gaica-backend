# routes/emergency.py

from flask import Blueprint, render_template, request, jsonify, current_app, session
from google import genai
from pymongo import MongoClient
from datetime import datetime
from utils.decorators import login_required

emergency = Blueprint("emergency", __name__)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# Local (offline) emergency guidance
# Used as fallback when Gemini API is unavailable
# -----------------------------
EMERGENCY_GUIDANCE = {
    "Flood": (
        "- Move to higher ground immediately, avoid walking or driving through flood water.\n"
        "- Switch off electricity and gas supply at the main switch if water is rising.\n"
        "- Keep emergency contacts, ID proof, and essential medicines ready in a waterproof bag.\n"
        "- Call Disaster Management helpline **1078** for rescue assistance."
    ),
    "Earthquake": (
        "- Drop, Cover, and Hold On — get under a sturdy table and protect your head/neck.\n"
        "- Stay away from windows, mirrors, and heavy furniture that could fall.\n"
        "- If outdoors, move to an open area away from buildings and power lines.\n"
        "- After shaking stops, check for injuries and be prepared for aftershocks."
    ),
    "Fire": (
        "- Alert everyone nearby and evacuate the building immediately, do not use elevators.\n"
        "- Stay low to the ground to avoid smoke inhalation.\n"
        "- If trapped, close doors between you and the fire, and signal for help from a window.\n"
        "- Call Fire Brigade **101** immediately."
    ),
    "Cyclone": (
        "- Stay indoors, away from windows and glass doors.\n"
        "- Keep a battery-powered radio, flashlight, and emergency supplies ready.\n"
        "- Avoid using the phone except for emergencies.\n"
        "- Follow official evacuation orders from local authorities without delay."
    ),
    "Landslide": (
        "- Move away from the slide path immediately, do not return to collect belongings.\n"
        "- Watch for unusual sounds like trees cracking or rocks knocking together.\n"
        "- If escape is not possible, curl into a tight ball and protect your head.\n"
        "- Report the incident to Disaster Management helpline **1078**."
    ),
    "Health Emergency": (
        "- Call Ambulance **108** immediately for medical assistance.\n"
        "- Keep the person calm, comfortable, and avoid moving them unnecessarily.\n"
        "- If trained, provide first aid or CPR as needed until help arrives.\n"
        "- Keep medical history and current medications handy for paramedics."
    ),
    "Cyber Attack": (
        "- Disconnect the affected device from the internet immediately.\n"
        "- Change passwords for affected accounts from a different secure device.\n"
        "- Do not pay any ransom demands; report to cybercrime.gov.in immediately.\n"
        "- Inform your bank if any financial accounts may be compromised."
    ),
    "Road Accident": (
        "- Call Ambulance **108** and Police **112** immediately.\n"
        "- Do not move injured persons unless there is immediate danger (fire, traffic).\n"
        "- Turn on hazard lights and place warning triangles to alert other vehicles.\n"
        "- Provide basic first aid only if trained, and keep the injured person calm."
    ),
    "Other": (
        "- Stay calm and assess the situation carefully.\n"
        "- Contact the nearest relevant emergency helpline (Police 112, Ambulance 108, Fire 101).\n"
        "- Share your exact location with emergency responders or trusted contacts.\n"
        "- Move to a safe location if there is any immediate danger."
    )
}


def local_emergency_guidance(emergency_type, message):
    """
    Simple offline emergency guidance based on emergency type.
    Returns a markdown-formatted string similar to what the AI would return.
    """
    guidance = EMERGENCY_GUIDANCE.get(emergency_type, EMERGENCY_GUIDANCE["Other"])

    result = (
        f"**EMERGENCY TYPE:** {emergency_type}\n\n"
        f"**IMMEDIATE ACTIONS:**\n{guidance}\n\n"
        f"**IMPORTANT:** If this is a life-threatening emergency, call Police (112), "
        f"Ambulance (108), or Fire Brigade (101) immediately. Do not rely solely on this guidance."
    )

    return result


# -----------------------------
# Render the Emergency page
# -----------------------------
@emergency.route("/emergency", methods=["GET"])
@login_required
def emergency_page():
    return render_template("emergency.html")


# -----------------------------
# AI Emergency Guidance API
# -----------------------------
@emergency.route("/emergency", methods=["POST"])
@login_required
def get_emergency_guidance():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No data received."
            }), 400

        emergency_type = data.get("emergency_type", "").strip()
        message = data.get("message", "").strip()

        if not emergency_type or not message:
            return jsonify({
                "status": "error",
                "message": "Please select an emergency type and describe your situation."
            }), 400

        api_key = current_app.config.get("GEMINI_API_KEY")

        # If API key missing/default, use local guidance directly
        if not api_key or "YOUR_ACTUAL_KEY" in api_key or "यहाँ" in api_key or "your" in api_key:
            ai_analysis = local_emergency_guidance(emergency_type, message)
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = (
                    f"A user is reporting an emergency situation:\n"
                    f"Emergency Type: {emergency_type}\n"
                    f"Details: {message}\n\n"
                    f"Provide clear, calm, and actionable emergency guidance strictly in English with:\n"
                    f"1. IMMEDIATE ACTIONS: 3-5 clear bullet points on what to do right now.\n"
                    f"2. SAFETY TIPS: 2-3 additional safety precautions.\n"
                    f"Keep the tone calm, direct, and reassuring since the user may be in distress."
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
                print(f"Gemini API error (falling back to local guidance): {str(api_error)}")
                ai_analysis = local_emergency_guidance(emergency_type, message)

        # Save the emergency report into MongoDB
        try:
            db = get_db()
            db.emergency_reports.insert_one({
                "user_email": session.get("email", "guest"),
                "emergency_type": emergency_type,
                "message": message,
                "ai_analysis": ai_analysis,
                "timestamp": datetime.utcnow()
            })
        except Exception as db_error:
            print(f"Emergency report save error: {str(db_error)}")

        return jsonify({
            "status": "success",
            "message": "Emergency guidance generated successfully.",
            "ai_analysis": ai_analysis
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500