"""
Student entity – registered students.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.attendance import Attendance
    from app.models.department import Department
    from app.models.face_embedding import FaceEmbedding
    from app.models.recognition_log import RecognitionLog


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="University student identifier (unique)",
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    gender: Mapped[Optional[Gender]] = mapped_column(
        Enum(Gender, name="gender", native_enum=False),
        nullable=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    enrollment_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="students",
    )
    face_embeddings: Mapped[list["FaceEmbedding"]] = relationship(
        "FaceEmbedding",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    attendances: Mapped[list["Attendance"]] = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recognition_logs: Mapped[list["RecognitionLog"]] = relationship(
        "RecognitionLog",
        back_populates="student",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_students_department_active", "department_id", "is_active"),
        Index("ix_students_name", "last_name", "first_name"),
        UniqueConstraint("student_id", name="uq_students_student_id"),
    )

    @property
    def full_name(self) -> str:
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)

    def __repr__(self) -> str:
        return (
            f"<Student id={self.id} student_id={self.student_id!r} "
            f"name={self.full_name!r}>"
        )
