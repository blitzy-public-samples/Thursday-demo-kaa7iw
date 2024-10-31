"""
Flask middleware component that adds security headers to all HTTP responses to protect against common web vulnerabilities.

Human Tasks:
1. Verify that the security headers comply with the organization's security policies
2. Ensure Content-Security-Policy header values align with allowed content sources
3. Confirm HSTS max-age value is appropriate for the production environment
"""

# External imports
from flask import Flask, Response  # version: 2.0+
from typing import Callable  # version: 3.9+

# Internal imports
from ..utils.constants import SECURITY_HEADERS

class SecurityHeadersMiddleware:
    """
    Middleware class that adds security headers to all HTTP responses.
    
    Implements security requirements from:
    - 10.3.2 Security Headers
    - 7.6 Security Architecture/Application Controls
    """
    
    def __init__(self, app: Flask) -> None:
        """
        Initialize the middleware with Flask application instance.
        
        Args:
            app (Flask): The Flask application instance to attach the middleware to
        """
        self.app = app
        self._register_after_request()
    
    def _register_after_request(self) -> None:
        """Register the after_request callback with the Flask application."""
        self.app.after_request(self.after_request)
    
    def after_request(self, response: Response) -> Response:
        """
        Add security headers to each response if not already present.
        
        Args:
            response (Response): The Flask response object
            
        Returns:
            Response: The modified response with security headers
            
        Implementation of:
        - Security Headers Implementation (10.3.2)
        - Application Security Layer controls (7.6)
        """
        # Iterate through security headers and add them if not present
        for header, value in SECURITY_HEADERS.items():
            if header not in response.headers:
                response.headers[header] = value
        
        return response