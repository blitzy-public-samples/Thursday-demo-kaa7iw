"""
WSGI entry point module for production deployment using Gunicorn or other WSGI servers.

Human Tasks:
1. Set FLASK_ENV environment variable (defaults to 'production')
2. Configure Google Cloud User Store credentials in environment
3. Set up PostgreSQL connection string in environment
4. Configure Redis connection parameters in environment
5. Review and adjust logging configuration
"""

# External imports - versions specified for production deployment
import os  # version: 3.9+

# Internal imports
from app import create_app
from config import config_by_name

# Get environment configuration - defaults to 'production' for safety
env = os.getenv('FLASK_ENV', 'production')

# Create Flask application instance using environment-specific configuration
# Requirement: 1.1 System Overview - Implements the Flask web server handling REST API requests
# Requirement: 11.1 Environment Architecture - Provides WSGI application entry point for production deployment
app = create_app(config_by_name[env]())

if __name__ == '__main__':
    # This section is only used for development
    # In production, the application should be run using a WSGI server like Gunicorn
    app.run()