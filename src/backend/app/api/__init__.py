"""
API package initialization module that configures and exports the API Blueprint hierarchy.

Human Tasks:
1. Review rate limiting configuration for all API endpoints
2. Verify error response format consistency across endpoints
3. Set up monitoring for API performance metrics
4. Configure logging levels for API operations
"""

# External imports - versions specified as per requirements
from flask import Blueprint  # version: 2.0+

# Internal imports
from .v1 import api_v1_bp

# Create main API Blueprint
# Requirement: API Layer - RESTful endpoints handling HTTP requests and responses
api_bp = Blueprint('api', __name__)

def init_app(app):
    """
    Initializes the API package with the Flask application, registering all API version blueprints.
    
    Requirement: Component Architecture - Integration of API Gateway with service components
    
    Args:
        app: Flask application instance
        
    Returns:
        None
    """
    # Register v1 API Blueprint with main API Blueprint
    api_bp.register_blueprint(api_v1_bp)
    
    # Register main API Blueprint with Flask application
    app.register_blueprint(api_bp)
    
    # Configure API-wide settings
    
    # Set default JSON response settings
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    # Configure CORS headers for API endpoints
    @api_bp.after_request
    def add_security_headers(response):
        # Set security headers as defined in technical specification section 10.3.2
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
    
    # Configure API error handling
    @api_bp.errorhandler(Exception)
    def handle_error(error):
        """
        Global error handler for API exceptions.
        Formats error responses consistently across all endpoints.
        """
        if hasattr(error, 'code'):
            status_code = error.code
        else:
            status_code = 500
            
        return {
            'error': {
                'code': getattr(error, 'code_name', 'SYS001'),
                'message': str(error),
                'status': status_code
            }
        }, status_code