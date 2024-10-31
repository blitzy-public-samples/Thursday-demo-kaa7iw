"""
Configuration module for the Code Generation Web Application.

Human Tasks:
1. Create a .env file based on .env.example with appropriate values
2. Verify PostgreSQL connection string format and parameters
3. Confirm Redis connection string format and parameters
4. Set up Google OAuth client credentials in the environment
5. Generate and set secure secret keys for JWT and application
6. Review and adjust log levels for each environment
7. Configure allowed CORS origins for each environment
"""

# External imports - versions specified for production deployment
import os  # version: 3.9+
from typing import Dict, List, Type  # version: 3.9+
from dotenv import load_dotenv  # version: 0.19.0

# Internal imports
from app.utils.constants import (
    SECURITY_HEADERS,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES
)

class BaseConfig:
    """Base configuration class containing default settings and environment variable loading logic.
    
    Requirement: Environment Configuration - Provides configuration classes for all application components
    """
    
    def load_env_vars(self) -> None:
        """Loads environment variables from .env file.
        
        Requirement: Environment Configuration - Environment variable loading functionality
        """
        load_dotenv()
        
        # Security settings
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
        self.JWT_ACCESS_TOKEN_EXPIRES = JWT_ACCESS_TOKEN_EXPIRES
        self.JWT_REFRESH_TOKEN_EXPIRES = JWT_REFRESH_TOKEN_EXPIRES
        
        # Database settings
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.DATABASE_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', '5'))
        self.DATABASE_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', '10'))
        
        # Redis cache settings
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.REDIS_MAX_CONNECTIONS = int(os.getenv('REDIS_MAX_CONNECTIONS', '10'))
        
        # Google OAuth settings
        self.GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        self.GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
        
        # Rate limiting
        self.RATE_LIMIT_DEFAULT = int(os.getenv('RATE_LIMIT_DEFAULT', '100'))
        
        # Logging configuration
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # CORS settings
        cors_origins = os.getenv('CORS_ORIGINS', '')
        self.CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
        
        # Security headers
        self.SECURITY_HEADERS = SECURITY_HEADERS

class DevelopmentConfig(BaseConfig):
    """Development environment specific configuration.
    
    Requirement: Environment Configuration - Development environment settings
    """
    
    def __init__(self):
        self.DEBUG = True
        self.TESTING = False
        self.load_env_vars()

class ProductionConfig(BaseConfig):
    """Production environment specific configuration.
    
    Requirement: Environment Configuration - Production environment settings
    """
    
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.load_env_vars()

class TestingConfig(BaseConfig):
    """Testing environment specific configuration.
    
    Requirement: Environment Configuration - Testing environment settings
    """
    
    def __init__(self):
        self.DEBUG = True
        self.TESTING = True
        self.DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'postgresql://test:test@localhost:5432/test_db')
        self.load_env_vars()

# Configuration class mapping by environment name
# Requirement: Environment Configuration - Environment-specific configuration mapping
config_by_name: Dict[str, Type[BaseConfig]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}