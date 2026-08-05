# models/user.py

from datetime import datetime


class User:
    """
    User Model for GAICA
    """

    def __init__(
        self,
        fullname,
        email,
        username,
        password,
        role="user",
        status="active"
    ):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self):
        """
        Convert object to dictionary
        """
        return {
            "fullname": self.fullname,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"User({self.username})"