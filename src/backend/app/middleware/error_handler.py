"""
Flask middleware for handling and formatting application errors into standardized JSON responses with appropriate logging.

Human Tasks:
1. Verify log level configuration in logging config file
2. Ensure error codes in constants.py match API documentation
3. Review error response format with frontend team
"""

# External imports - versions specified as per technical requirements
from flask import Flask  # version: 2.0+
from werkzeug.exceptions import HTTPException  # version: 2.0+
import logging  # version: 3.9+
from typing import Tuple, Dict, Any  # version: 3.9+

# Internal imports
from ..utils.exceptions import (
    BaseAPIException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError,
    DatabaseError
)

class ErrorHandler:
    """
    Middleware class for handling various types of application errors and converting them to JSON responses.
    
    Requirement: A.4 Error Codes and Messages - Implementation of standardized error handling
    """
    
    def __init__(self, app: Flask) -> None:
        """
        Initialize the error handler with Flask application instance.
        
        Args:
            app: Flask application instance
        """
        self._app = app
        self._logger = logging.getLogger(__name__)
        self.init_app()
    
    def init_app(self) -> None:
        """
        Register all error handlers with the Flask application.
        
        Requirement: A.4 Error Handling - Registration of error handlers for different error types
        """
        # Register handler for custom API exceptions
        self._app.register_error_handler(BaseAPIException, self.handle_api_exception)
        
        # Register handler for HTTP exceptions
        self._app.register_error_handler(HTTPException, self.handle_http_exception)
        
        # Register handler for validation errors
        self._app.register_error_handler(ValidationError, self.handle_validation_error)
        
        # Register handler for generic exceptions
        self._app.register_error_handler(Exception, self.handle_generic_error)
    
    def handle_api_exception(self, error: BaseAPIException) -> Tuple[Dict[str, Any], int]:
        """
        Handle custom API exceptions and return formatted JSON response.
        
        Args:
            error: Instance of BaseAPIException or its subclasses
            
        Returns:
            Tuple containing error response dictionary and HTTP status code
            
        Requirement: A.4 Error Codes and Messages - Standardized error response formatting
        """
        # Log error with appropriate level based on status code
        if error.status_code >= 500:
            self._logger.error(f"API Error: {error.code} - {error.message}", exc_info=True)
        else:
            self._logger.warning(f"API Error: {error.code} - {error.message}")
        
        response = {
            "error": {
                "code": error.code,
                "message": error.message
            }
        }
        
        return response, error.status_code
    
    def handle_http_exception(self, error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """
        Handle Werkzeug HTTP exceptions and return formatted JSON response.
        
        Args:
            error: Instance of HTTPException
            
        Returns:
            Tuple containing error response dictionary and HTTP status code
            
        Requirement: A.4 Error Codes and Messages - HTTP error handling
        """
        self._logger.warning(f"HTTP Error {error.code}: {error.description}")
        
        response = {
            "error": {
                "code": f"HTTP{error.code}",
                "message": error.description
            }
        }
        
        return response, error.code
    
    def handle_validation_error(self, error: ValidationError) -> Tuple[Dict[str, Any], int]:
        """
        Handle validation errors with detailed field errors.
        
        Args:
            error: Instance of ValidationError containing field-specific errors
            
        Returns:
            Tuple containing error response dictionary and HTTP status code
            
        Requirement: A.4 Error Codes and Messages - Validation error handling with field details
        """
        self._logger.warning(f"Validation Error: {error.code} - {error.message}", extra={"validation_errors": error.errors})
        
        response = {
            "error": {
                "code": error.code,
                "message": error.message,
                "details": error.errors
            }
        }
        
        return response, error.status_code
    
    def handle_generic_error(self, error: Exception) -> Tuple[Dict[str, Any], int]:
        """
        Handle any unhandled exceptions as internal server errors.
        
        Args:
            error: Unhandled exception instance
            
        Returns:
            Tuple containing error response dictionary and HTTP status code
            
        Requirement: A.4 Error Codes and Messages - Generic error handling
        Requirement: 7.1 High-Level Architecture - Integration with core logging system
        """
        # Log unhandled exceptions with full stack trace
        self._logger.error(
            "Unhandled Exception",
            exc_info=True,
            extra={
                "error_type": error.__class__.__name__,
                "error_message": str(error)
            }
        )
        
        response = {
            "error": {
                "code": "SYS001",
                "message": "An unexpected error occurred. Please try again later."
            }
        }
        
        return response, 500