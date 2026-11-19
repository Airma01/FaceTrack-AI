"""
RecognitionLog entity – audit trail of face-recognition attempts.

Tracks both successful matches and unknown/failed attempts.
Does not store raw images or full embedding vectors.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.student import Student


class RecognitionStatus(str, enum.Enum):
    MATCHED = "MATCHED"
    UNKNOWN = "UNKNOWN"
    FAILED = "FAILED"


class RecognitionLog(Base):
    __tablename__ = "recognition_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Nullable – unknown faces have no linked student
    student_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Similarity score when a match is found (0.0–1.0)",
    )

    recognition_status: Mapped[RecognitionStatus] = mapped_column(
        Enum(RecognitionStatus, name="recognition_status", native_enum=False),
        nullable=False,
        index=True,
    )

    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="End-to-end recognition latency in milliseconds",
    )

    # Relationships
    student: Mapped[Optional["Student"]] = relationship(
        "Student",
        back_populates="recognition_logs",
    )

    __table_args__ = (
        Index("ix_recognition_logs_status_time", "recognition_status", "processed_at"),
        Index("ix_recognition_logs_student_time", "student_id", "processed_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<RecognitionLog id={self.id} status={self.recognition_status} "
            f"student_id={self.student_id} conf={self.confidence_score}>"
        )
