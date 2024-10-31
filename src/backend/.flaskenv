# Flask Environment Configuration
# Requirement: Environment Configuration - Configures Flask-specific environment settings for the web application
# Requirement: Application Layer Configuration - Sets up Flask web server configuration for the application layer

# Flask application entry point
FLASK_APP=wsgi.py

# Flask environment (development/staging/production)
FLASK_ENV=development

# Debug mode (1=enabled, 0=disabled)
FLASK_DEBUG=1

# Development server host
FLASK_RUN_HOST=0.0.0.0

# Development server port
FLASK_RUN_PORT=8000