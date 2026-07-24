"""
Application configuration loader.

Loads environment variables from the .env file and exposes them
through a Config class.
"""

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


class Config:
    """Application configuration."""

    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    USE_MOCK_DATA = (
        os.getenv("USE_MOCK_DATA", "true").strip().lower() == "true"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///scanner.db"
    )

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
