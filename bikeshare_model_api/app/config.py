"""Configuration for the bike sharing API."""

import logging
import sys
from typing import List

from loguru import logger
try:
    # For Pydantic v2.x
    from pydantic_settings import BaseSettings
except ImportError:
    # For Pydantic v1.x
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the API."""

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Bike Sharing Prediction API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Logging configuration - use string for the level
    LOGGING_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic config class."""

        case_sensitive = True


# Application settings instance
settings = Settings()

# Configure logging
class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging."""

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_app_logging(config: Settings) -> None:
    """Configure app logging."""
    
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    
    # Convert string log level to int if needed
    log_level = config.LOGGING_LEVEL
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=numeric_level)]

    logger.configure(
        handlers=[{"sink": sys.stderr, "level": log_level}]
    )