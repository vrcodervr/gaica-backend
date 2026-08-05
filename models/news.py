# models/news.py

from datetime import datetime


class News:
    """
    News Model for GAICA
    """

    def __init__(
        self,
        title,
        content,
        source,
        submitted_by,
        status="Pending"
    ):
        self.title = title
        self.content = content
        self.source = source
        self.submitted_by = submitted_by
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self):
        """
        Convert News object to Dictionary
        """
        return {
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "submitted_by": self.submitted_by,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"News({self.title}, {self.status})"