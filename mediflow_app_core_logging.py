"""
app/core/logging.py - Logging configuration
"""

import logging
import logging.handlers
from app.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure application logging"""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/mediflow.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (FileNotFoundError, PermissionError):
        # If we can't write to logs directory, just use console
        pass

    return logger


# Get logger instance
logger = logging.getLogger(__name__)
