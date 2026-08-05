# models/report.py

from datetime import datetime


class Report:
    """
    Report Model for GAICA
    """

    def __init__(
        self,
        report_type,
        title,
        description,
        location,
        reported_by,
        status="Pending"
    ):
        self.report_type = report_type
        self.title = title
        self.description = description
        self.location = location
        self.reported_by = reported_by
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self):
        """
        Convert Report object to Dictionary
        """
        return {
            "report_type": self.report_type,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "reported_by": self.reported_by,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"Report({self.report_type}, {self.status})"