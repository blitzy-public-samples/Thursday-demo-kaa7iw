"""
Main Flask application factory and initialization module.

Human Tasks:
1. Configure Google Cloud User Store credentials in environment
2. Set up PostgreSQL connection string in environment
3. Configure Redis connection parameters in environment
4. Review and adjust rate limiting settings
5. Set up monitoring endpoints and credentials
6. Configure logging levels and handlers
7. Review security headers configuration
"""

# External imports - versions specified as per requirements
from flask import Flask  # version: 2.0+
from typing import Optional  # version: 3.9+
import logging  # version: 3.9+
from logging.config import dictConfig  # version: 3.9+

# Internal imports
from .extensions import init_extensions
from .api.v1 import api_v1_bp
from .middleware.auth import require_auth
from .middleware.rate_limiter import configure_rate_limiting
from .middleware.security_headers import configure_security_headers
from .middleware.error_handler import configure_error_handlers
from .logging.config import get_logging_config
from .monitoring.health import configure_health_checks
from .monitoring.metrics import configure_metrics

def create_app(config_object: str) -> Flask:
    """
    Flask application factory that initializes and configures the application instance.
    
    Requirement: 1.1 System Overview - Implements layered backend architecture
    Requirement: 7.6 Security Architecture - Implements security layers
    
    Args:
        config_object: String path to configuration object
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    try:
        # Load configuration
        app.config.from_object(config_object)
        
        # Configure logging first
        dictConfig(get_logging_config(app.config))
        logger = logging.getLogger(__name__)
        logger.info(f"Starting application with config: {config_object}")
        
        # Initialize extensions (database, cache, metrics)
        init_extensions(app)
        logger.info("Extensions initialized successfully")
        
        # Configure security headers
        configure_security_headers(app)
        logger.info("Security headers configured")
        
        # Configure rate limiting
        configure_rate_limiting(app)
        logger.info("Rate limiting configured")
        
        # Configure error handlers
        configure_error_handlers(app)
        logger.info("Error handlers configured")
        
        # Configure health checks
        configure_health_checks(app)
        logger.info("Health checks configured")
        
        # Configure metrics collection
        configure_metrics(app)
        logger.info("Metrics collection configured")
        
        # Register API v1 blueprint
        app.register_blueprint(api_v1_bp)
        logger.info("API v1 blueprint registered")
        
        # Add authentication middleware to app context
        app.before_request(require_auth)
        logger.info("Authentication middleware configured")
        
        # Register teardown handlers
        @app.teardown_appcontext
        def cleanup(resp: Optional[Exception]) -> None:
            """
            Clean up resources on application context teardown.
            
            Args:
                resp: Optional exception that occurred
            """
            # Close database sessions
            if hasattr(app, 'extensions') and 'db_session' in app.extensions:
                app.extensions['db_session'].remove()
        
        logger.info("Application initialization completed successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise

def get_version() -> str:
    """
    Get the current application version.
    
    Returns:
        str: Application version string
    """
    return '1.0.0'  # Update version manually on releases

# Initialize logging for module
logger = logging.getLogger(__name__)

# Export the create_app factory function
__all__ = ['create_app']