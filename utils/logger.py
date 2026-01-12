"""Logging configuration for ApplyMate."""

import sys
from pathlib import Path
from loguru import logger

from config import settings


def setup_logging():
    """Configure loguru logger."""
    # Remove default handler
    logger.remove()
    
    # Console handler with colorized output
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # File handler
    log_file = settings.get_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="1 week",
        compression="zip"
    )
    
    logger.info("Logging initialized")


# Initialize logging when module is imported
setup_logging()
