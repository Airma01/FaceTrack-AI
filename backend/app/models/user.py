"""
User entity – system administrators and operators.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.attendance import Attendance


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    full_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", native_enum=False),
        nullable=False,
        default=UserRole.OPERATOR,
        server_default=UserRole.OPERATOR.value,
    )
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
    recorded_attendances: Mapped[list["Attendance"]] = relationship(
        "Attendance",
        back_populates="recorder",
        foreign_keys="Attendance.recorded_by",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_users_role_active", "role", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role}>"
