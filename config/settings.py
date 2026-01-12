"""Configuration management for ApplyMate."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "ApplyMate"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATABASE_PATH: str = "data/database/applymate.db"
    PROFILES_DIR: str = "data/profiles"
    UPLOADS_DIR: str = "data/uploads"
    LOG_FILE: str = "data/logs/applymate.log"
    
    # Browser
    BROWSER_HEADLESS: bool = False
    BROWSER_TIMEOUT: int = 30000  # milliseconds
    BROWSER_VIEWPORT_WIDTH: int = 1280
    BROWSER_VIEWPORT_HEIGHT: int = 720
    
    # NLP
    SPACY_MODEL: str = "en_core_web_sm"
    MIN_FIELD_MATCH_SCORE: float = 0.6
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Future: Authentication
    SECRET_KEY: Optional[str] = None
    SESSION_TIMEOUT: int = 3600
    
    # Current user (for single-user mode, will be replaced with auth)
    CURRENT_USER_ID: int = 1
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    def get_database_path(self) -> Path:
        """Get absolute database path."""
        return self.BASE_DIR / self.DATABASE_PATH
    
    def get_profiles_dir(self) -> Path:
        """Get absolute profiles directory path."""
        return self.BASE_DIR / self.PROFILES_DIR
    
    def get_uploads_dir(self) -> Path:
        """Get absolute uploads directory path."""
        return self.BASE_DIR / self.UPLOADS_DIR
    
    def get_log_file(self) -> Path:
        """Get absolute log file path."""
        return self.BASE_DIR / self.LOG_FILE
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.get_database_path().parent,
            self.get_profiles_dir(),
            self.get_uploads_dir(),
            self.get_log_file().parent
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

