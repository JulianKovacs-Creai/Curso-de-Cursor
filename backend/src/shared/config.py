"""
Configuration Management - Clean Architecture compatible.

This module provides configuration management with proper validation.
"""

import os
from typing import List, Optional


class Settings:
    """
    Application settings with validation and environment variable support.
    """
    
    def __init__(self):
        # Database settings
        self.database_path = os.getenv("DATABASE_PATH", "ecommerce_clean.db")
        self.database_url = os.getenv("DATABASE_URL")
        
        # API settings
        self.api_title = os.getenv("API_TITLE", "E-commerce Clean Architecture API")
        self.api_description = os.getenv("API_DESCRIPTION", "Clean Architecture e-commerce API")
        self.api_version = os.getenv("API_VERSION", "1.0.0")
        
        # Server settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.reload = os.getenv("RELOAD", "false").lower() == "true"
        
        # Security settings
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.jwt_refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        
        # CORS settings
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003")
        self.cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
        self.cors_allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
        
        cors_methods_str = os.getenv("CORS_ALLOW_METHODS", "*")
        self.cors_allow_methods = [method.strip() for method in cors_methods_str.split(",")]
        
        cors_headers_str = os.getenv("CORS_ALLOW_HEADERS", "*")
        self.cors_allow_headers = [header.strip() for header in cors_headers_str.split(",")]
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # File upload settings
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10MB
        self.upload_directory = os.getenv("UPLOAD_DIRECTORY", "uploads/")
        
        # Environment
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings (singleton pattern).
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_database_path() -> str:
    """
    Get database path from settings.
    
    Returns:
        Database file path
    """
    settings = get_settings()
    return settings.database_path


def is_development() -> bool:
    """Check if running in development mode"""
    return get_settings().environment == "development"


def is_production() -> bool:
    """Check if running in production mode"""
    return get_settings().environment == "production"


def is_debug_mode() -> bool:
    """Check if debug mode is enabled"""
    return get_settings().debug


def get_cors_origins() -> List[str]:
    """Get CORS origins from settings"""
    return get_settings().cors_origins


def get_secret_key() -> str:
    """Get secret key from settings"""
    return get_settings().secret_key


def get_jwt_secret() -> str:
    """Get JWT secret key from settings"""
    return get_settings().jwt_secret_key