# KAN-465: Implement Sistema de Logging y Monitoreo de Consultas
import logging
import sys
from src.config import config

def setup_logging():
    """
    Configures a centralized logging system for the application.
    """
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    # Suppress verbose logs from libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance for a given module name.
    """
    return logging.getLogger(name)
