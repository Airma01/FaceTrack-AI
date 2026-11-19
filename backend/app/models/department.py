"""
Department entity – academic departments.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.student import Student


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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

    # Relationships
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="department",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_departments_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<Department id={self.id} code={self.code!r} name={self.name!r}>"
