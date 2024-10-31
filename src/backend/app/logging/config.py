# Python standard library imports (version 3.9+)
import os
import logging
import logging.config

# Internal imports
from ..logging.handlers import JsonFormatter, CloudLoggingHandler

# Global constants for logging configuration
LOG_FORMAT = {'timestamp': '%(asctime)s', 'level': '%(levelname)s', 'module': '%(module)s', 'message': '%(message)s'}
DEFAULT_LOG_LEVEL = 'INFO'
DEVELOPMENT_LOG_LEVEL = 'DEBUG'

def get_logging_config(app_env: str, project_id: str) -> dict:
    """
    Generates logging configuration dictionary based on environment.
    
    Requirement addressed: Logging System
    - Provides environment-specific logging configuration
    - Configures appropriate log levels and handlers
    
    Args:
        app_env: Application environment ('development', 'staging', 'production')
        project_id: Google Cloud project ID for cloud logging
        
    Returns:
        Dictionary containing complete logging configuration
    """
    # Base configuration for all handlers
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': JsonFormatter,
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console'],
                'level': DEVELOPMENT_LOG_LEVEL if app_env == 'development' else DEFAULT_LOG_LEVEL,
                'propagate': True
            },
            'werkzeug': {  # Flask's built-in server logger
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            'sqlalchemy': {  # SQLAlchemy logger
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False
            }
        }
    }
    
    # Add Cloud Logging handler for non-development environments
    if app_env != 'development':
        config['handlers']['cloud'] = {
            '()': CloudLoggingHandler,
            'project_id': project_id,
            'formatter': 'json'
        }
        # Add cloud handler to root logger
        config['loggers']['']['handlers'].append('cloud')
    
    return config

def configure_logging(app_env: str, project_id: str) -> None:
    """
    Configures the application logging system based on the environment.
    
    Requirement addressed: Log Management
    - Sets up centralized logging for production environments
    - Configures development-specific logging settings
    - Ensures consistent log formatting across environments
    
    Args:
        app_env: Application environment ('development', 'staging', 'production')
        project_id: Google Cloud project ID for cloud logging
    """
    # Get logging configuration based on environment
    config = get_logging_config(app_env, project_id)
    
    # Apply logging configuration
    logging.config.dictConfig(config)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(
        'Logging system initialized',
        extra={
            'environment': app_env,
            'log_level': DEVELOPMENT_LOG_LEVEL if app_env == 'development' else DEFAULT_LOG_LEVEL
        }
    )