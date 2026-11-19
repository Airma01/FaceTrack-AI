"""
Attendance entity – daily attendance records.

Unique constraint on (student_id, attendance_date) prevents duplicate
check-ins for the same calendar day. Extend later with session/period
support if multi-period attendance is required.
"""

from __future__ import annotations

import enum
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.user import User


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    LATE = "LATE"
    ABSENT = "ABSENT"


class Attendance(Base):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    check_in_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    check_out_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)

    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus, name="attendance_status", native_enum=False),
        nullable=False,
        default=AttendanceStatus.PRESENT,
        server_default=AttendanceStatus.PRESENT.value,
    )

    recognition_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Similarity / confidence score from face matcher (0.0–1.0)",
    )

    recorded_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="attendances",
    )
    recorder: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="recorded_attendances",
        foreign_keys=[recorded_by],
    )

    __table_args__ = (
        # One attendance record per student per calendar day
        UniqueConstraint(
            "student_id",
            "attendance_date",
            name="uq_attendance_student_date",
        ),
        Index("ix_attendances_date_status", "attendance_date", "status"),
        Index("ix_attendances_student_date", "student_id", "attendance_date"),
    )

    def __repr__(self) -> str:
        return (
            f"<Attendance id={self.id} student_id={self.student_id} "
            f"date={self.attendance_date} status={self.status}>"
        )
