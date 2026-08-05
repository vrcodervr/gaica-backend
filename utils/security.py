# utils/security.py

from werkzeug.security import generate_password_hash, check_password_hash
import secrets


def hash_password(password):
    """
    Generate a secure hashed password.
    """
    return generate_password_hash(password)


def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    """
    return check_password_hash(hashed_password, password)


def generate_secret_key(length=32):
    """
    Generate a secure random secret key.
    """
    return secrets.token_hex(length)


def generate_token(length=16):
    """
    Generate a random security token.
    """
    return secrets.token_urlsafe(length)


if __name__ == "__main__":

    password = "admin123"

    hashed = hash_password(password)

    print("Original Password :", password)
    print("Hashed Password   :", hashed)

    print("Password Match    :", verify_password(password, hashed))

    print("Secret Key        :", generate_secret_key())

    print("Random Token      :", generate_token())