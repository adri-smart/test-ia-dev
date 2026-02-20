# KAN-464, KAN-466, KAN-467: Configuration Management
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to hold all settings from environment variables.
    """
    # General Config
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Database Config (KAN-467)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "customer_db")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_SSL_MODE = os.getenv("DB_SSL_MODE", "prefer") # Ensures encrypted communication
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if DB_SSL_MODE:
        DATABASE_URL += f"?sslmode={DB_SSL_MODE}"

    # Gemini Enterprise API Config (KAN-466)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

    # Logging Config (KAN-465)
    QUERY_LOG_SLOW_THRESHOLD_SEC = int(os.getenv("QUERY_LOG_SLOW_THRESHOLD_SEC", 2))

    # Analysis Config
    DATA_INTEGRITY_THRESHOLD = float(os.getenv("DATA_INTEGRITY_THRESHOLD", 0.95))
    CLV_PROCESS_TIME_LIMIT_MIN = int(os.getenv("CLV_PROCESS_TIME_LIMIT_MIN", 2))
    SEGMENTATION_TIME_LIMIT_SEC = int(os.getenv("SEGMENTATION_TIME_LIMIT_SEC", 5))
    DRILL_DOWN_TIME_LIMIT_SEC = int(os.getenv("DRILL_DOWN_TIME_LIMIT_SEC", 2))

config = Config()
