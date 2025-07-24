import logging
import logging.handlers
import os
from app.core.config import get_settings

def setup_logging():
    settings = get_settings()
    
    # Create logger
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation (production only)
    if settings.ENVIRONMENT == "production":
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f"logs/{settings.LOG_FILE}",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger