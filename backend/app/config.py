from pathlib import Path
import os

from dotenv import load_dotenv


# =====================================================
# Project root
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# =====================================================
# Settings
# =====================================================

class Settings:

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    PORT = int(os.getenv("PORT", "8000"))


settings = Settings()


# =====================================================
# Debug
# =====================================================

print(
    "GROQ_API_KEY:",
    "SET" if settings.GROQ_API_KEY else "NOT SET"
)

print(
    "PORT:",
    settings.PORT
)