"""
Application Configuration

This module loads environment variables from the project .env file
and provides them throughout the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file from the project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application configuration settings."""

    SQL_SERVER: str = os.getenv("DB_SERVER", "")
    SQL_DATABASE: str = os.getenv("DB_DATABASE", "")
    SQL_DRIVER: str = os.getenv("DB_DRIVER", "")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


print(Settings.SQL_SERVER)
print(Settings.SQL_DATABASE)
print(Settings.SQL_DRIVER)
print(Settings.POSTGRES_HOST)
print(Settings.POSTGRES_PORT)
print(Settings.POSTGRES_DATABASE)
print(Settings.POSTGRES_USER)


