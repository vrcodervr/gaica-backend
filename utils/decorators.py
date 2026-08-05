# utils/decorators.py

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Decorator to protect routes that require login.
    Redirects to login page if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            flash("Please login to access this page.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function