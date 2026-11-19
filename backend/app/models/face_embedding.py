"""
FaceEmbedding entity – biometric face feature vectors from InsightFace.

Security notes:
- Never expose the raw embedding vector through ordinary student/list APIs.
- Prefer dedicated, authenticated internal endpoints for recognition services.
- Do not store raw facial images in this table.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.student import Student


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Store InsightFace embedding as binary (float32 array bytes).
    # Typical dimension for buffalo_l / antelopev2 is 512.
    embedding: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
        comment="Serialized float32 embedding vector (e.g. 512-dim)",
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="buffalo_l",
        server_default="buffalo_l",
    )
    model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    embedding_dimension: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=512,
        server_default="512",
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

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="face_embeddings",
    )

    __table_args__ = (
        Index("ix_face_embeddings_student_active", "student_id", "is_active"),
        Index("ix_face_embeddings_model", "model_name"),
    )

    def __repr__(self) -> str:
        return (
            f"<FaceEmbedding id={self.id} student_id={self.student_id} "
            f"dim={self.embedding_dimension} model={self.model_name!r}>"
        )
