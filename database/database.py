"""
Database connection module.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.config import Config

# SQLAlchemy engine
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Returns a database session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
