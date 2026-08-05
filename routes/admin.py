# routes/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from utils.decorators import login_required

admin = Blueprint("admin_panel", __name__)


def get_db():
    """Connect to MongoDB using URI from config.py"""
    mongo_uri = current_app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_database()


# -----------------------------
# READ - Admin Dashboard (list all users)
# -----------------------------
@admin.route("/admin")
@login_required
def admin_dashboard():
    db = get_db()
    users = list(db.users.find())

    # Convert ObjectId to string for template use
    for user in users:
        user["_id"] = str(user["_id"])

    return render_template("admin.html", users=users)


# -----------------------------
# CREATE - Add a new user manually
# -----------------------------
@admin.route("/admin/user/add", methods=["POST"])
@login_required
def add_user():
    try:
        db = get_db()
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")

        if not fullname or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("admin_panel.admin_dashboard"))

        existing_user = db.users.find_one({"email": email})
        if existing_user:
            flash("A user with this email already exists.", "danger")
            return redirect(url_for("admin_panel.admin_dashboard"))

        hashed_password = generate_password_hash(password)

        db.users.insert_one({
            "fullname": fullname,
            "email": email,
            "mobile": mobile,
            "password": hashed_password
        })

        flash("User added successfully.", "success")
        return redirect(url_for("admin_panel.admin_dashboard"))

    except Exception as e:
        flash(f"Error adding user: {str(e)}", "danger")
        return redirect(url_for("admin_panel.admin_dashboard"))


# -----------------------------
# UPDATE - Edit an existing user
# -----------------------------
@admin.route("/admin/user/edit/<user_id>", methods=["POST"])
@login_required
def edit_user(user_id):
    try:
        db = get_db()
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        mobile = request.form.get("mobile", "").strip()

        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "fullname": fullname,
                "email": email,
                "mobile": mobile
            }}
        )

        flash("User updated successfully.", "success")
        return redirect(url_for("admin_panel.admin_dashboard"))

    except Exception as e:
        flash(f"Error updating user: {str(e)}", "danger")
        return redirect(url_for("admin_panel.admin_dashboard"))


# -----------------------------
# DELETE - Remove a user
# -----------------------------
@admin.route("/admin/user/delete/<user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    try:
        db = get_db()
        db.users.delete_one({"_id": ObjectId(user_id)})
        flash("User deleted successfully.", "success")
        return redirect(url_for("admin_panel.admin_dashboard"))

    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")
        return redirect(url_for("admin_panel.admin_dashboard"))