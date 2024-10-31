"""
Middleware package initialization module that exports all middleware components for Flask application
security, authentication, validation, error handling, and rate limiting.

Human Tasks:
1. Verify security headers configuration in constants.py
2. Review rate limit values with security team
3. Configure Redis connection parameters
4. Set up Google Cloud User Store credentials
5. Configure JWT secret key in environment variables
"""

# External imports - versions specified as per requirements
from flask import Flask  # version: 2.0+
from typing import Any  # version: 3.9+

# Internal imports for middleware components
from .security_headers import SecurityHeadersMiddleware
from .request_validator import RequestValidator, validate_request_middleware
from .error_handler import ErrorHandler
from .rate_limiter import RateLimiter, rate_limit
from .auth import require_auth, get_current_user

# Export all middleware components
__all__ = [
    'SecurityHeadersMiddleware',
    'RequestValidator',
    'validate_request_middleware',
    'ErrorHandler',
    'RateLimiter',
    'rate_limit',
    'require_auth',
    'get_current_user'
]

def init_middleware(app: Flask) -> None:
    """
    Initialize all middleware components for the Flask application.
    
    Implements requirements:
    - 7.6 Security Architecture/Application Controls
    - 10.3.1 Request Security
    
    Args:
        app: Flask application instance
    """
    # Initialize security headers middleware
    # Requirement: Security headers implementation for HTTP responses
    SecurityHeadersMiddleware(app)
    
    # Initialize error handler middleware
    # Requirement: Comprehensive error handling and logging
    ErrorHandler(app)
    
    # Initialize rate limiter middleware
    # Requirement: Rate limiting implementation
    rate_limiter = RateLimiter(app.cache)
    app.config['RATE_LIMITER'] = rate_limiter
    
    # Initialize request validator middleware
    # Requirement: Input validation implementation
    request_validator = RequestValidator()
    app.config['REQUEST_VALIDATOR'] = request_validator
    
    # Register middleware order
    # The order is important for proper request/response processing
    @app.before_request
    def before_request() -> Any:
        """Execute middleware in correct order before request processing."""
        # Rate limiting check happens first
        if hasattr(app, 'rate_limiter'):
            app.rate_limiter.check_rate_limit()
        
        # Authentication check follows
        # Note: Individual routes use @require_auth decorator
        
        # Request validation happens last
        # Note: Individual routes use @validate_request_middleware decorator
    
    @app.after_request
    def after_request(response: Any) -> Any:
        """Execute middleware in correct order after request processing."""
        # Security headers are added to response
        return response