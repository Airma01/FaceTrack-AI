"""
SQLAlchemy ORM models package.

Importing this package registers all models with the shared Base metadata,
which is required for Alembic autogenerate and for Base.metadata.create_all().
"""

from app.models.attendance import Attendance, AttendanceStatus
from app.models.department import Department
from app.models.face_embedding import FaceEmbedding
from app.models.recognition_log import RecognitionLog, RecognitionStatus
from app.models.student import Gender, Student
from app.models.user import User, UserRole

__all__ = [
    "User",
    "UserRole",
    "Department",
    "Student",
    "Gender",
    "FaceEmbedding",
    "Attendance",
    "AttendanceStatus",
    "RecognitionLog",
    "RecognitionStatus",
]
