import os
from pathlib import Path

# Load .env if present (development convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Configuration for the Flask app.

    Uses environment variables when available, with sane defaults for
    local development (sqlite file and a non-secret development key).
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret'
    