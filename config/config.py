import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    DATABASE_URL = "sqlite:///scanner.db"
