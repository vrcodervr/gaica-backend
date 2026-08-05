# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

auth = Blueprint("auth", __name__)


def get_db():
    """
    Connect to MongoDB using URI from config.py
    Returns the gaica_db database object.
    """
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client.get_database()
    return db


# ----------------------------
# Login
# ----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html")

        try:
            db = get_db()
            users = db.users

            user = users.find_one({"email": email})

            if user and check_password_hash(user["password"], password):
                session["user"] = user["fullname"]
                session["email"] = user["email"]

                # Set admin flag for the specific admin email
                if user["email"] == "virendrasingh376d@gmail.com":
                    session["is_admin"] = True
                else:
                    session["is_admin"] = False

                flash("Login Successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid Email or Password", "danger")

        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")

    return render_template("login.html")


# ----------------------------
# Register
# ----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not fullname or not email or not mobile or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "danger")
            return render_template("register.html")

        if len(password) < current_app.config.get("PASSWORD_MIN_LENGTH", 8):
            flash(f"Password must be at least {current_app.config.get('PASSWORD_MIN_LENGTH', 8)} characters long.", "danger")
            return render_template("register.html")

        try:
            db = get_db()
            users = db.users

            # Check if email already exists
            existing_user = users.find_one({"email": email})
            if existing_user:
                flash("Email already registered. Please login.", "danger")
                return render_template("register.html")

            # Hash password before saving (never store plain text)
            hashed_password = generate_password_hash(password)

            # Save new user to MongoDB
            users.insert_one({
                "fullname": fullname,
                "email": email,
                "mobile": mobile,
                "password": hashed_password
            })

            flash("Registration Successful! Please Login.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")
            return render_template("register.html")

    return render_template("register.html")


# ----------------------------
# Logout
# ----------------------------
@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "info")

    return redirect(url_for("index"))