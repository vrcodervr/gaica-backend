# utils/validation.py

import re


def is_valid_email(email):
    """
    Validate email address.
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_username(username):
    """
    Username must be 3-20 characters.
    """
    pattern = r'^[A-Za-z0-9_]{3,20}$'
    return re.match(pattern, username) is not None


def is_valid_password(password):
    """
    Password must contain:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    pattern = (
        r'^(?=.*[a-z])'
        r'(?=.*[A-Z])'
        r'(?=.*\d)'
        r'.{8,}$'
    )
    return re.match(pattern, password) is not None


def is_empty(value):
    """
    Check if value is empty.
    """
    return value is None or value.strip() == ""


def is_valid_phone(phone):
    """
    Validate 10-digit phone number.
    """
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_required_fields(data, fields):
    """
    Check required fields in a dictionary.
    """
    missing = []

    for field in fields:
        if field not in data or is_empty(str(data[field])):
            missing.append(field)

    return missing


if __name__ == "__main__":

    print("Email:", is_valid_email("test@gmail.com"))
    print("Username:", is_valid_username("virendra123"))
    print("Password:", is_valid_password("Admin123"))
    print("Phone:", is_valid_phone("9876543210"))

    sample = {
        "name": "Virendra",
        "email": "test@gmail.com"
    }

    print(validate_required_fields(
        sample,
        ["name", "email", "password"]
    ))