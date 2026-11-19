"""
Database connection and session management for FaceTrack-AI.

Uses SQLAlchemy 2.0 style with a shared declarative Base.
All models must import Base from this module.
"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""

    pass


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session and
    ensures it is closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for dependency injection
DbSession = Annotated[Session, Depends(get_db)]
