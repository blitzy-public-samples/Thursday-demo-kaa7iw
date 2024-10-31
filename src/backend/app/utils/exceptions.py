"""
Custom exception classes for handling various error scenarios in the application.

Human Tasks:
1. Verify that HTTP status codes align with the API documentation
2. Ensure error messages in ERROR_CODES match the API documentation
3. Review error handling patterns with the team for consistency
"""

# External imports
from typing import Dict, List  # version: 3.9+

# Internal imports
from ..utils.constants import ERROR_CODES

class BaseAPIException(Exception):
    """
    Base exception class for all API related exceptions.
    
    Requirement: A.4 Error Handling - Base exception class for standardized error handling
    """
    def __init__(self, code: str, message: str, status_code: int) -> None:
        """Initialize base API exception with code, message and status code."""
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code

class AuthenticationError(BaseAPIException):
    """
    Exception for authentication related errors.
    
    Requirement: 10.1 Authentication and Authorization - Authentication error handling
    """
    def __init__(self, code: str) -> None:
        """Initialize authentication error with specific error code."""
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=401)

class AuthorizationError(BaseAPIException):
    """
    Exception for authorization related errors.
    
    Requirement: 10.1 Authentication and Authorization - Authorization error handling
    """
    def __init__(self, code: str) -> None:
        """Initialize authorization error with specific error code."""
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=403)

class ResourceNotFoundError(BaseAPIException):
    """
    Exception for resource not found errors.
    
    Requirement: A.4 Error Handling - Resource not found error handling
    """
    def __init__(self, code: str) -> None:
        """Initialize resource not found error with specific error code."""
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=404)

class ValidationError(BaseAPIException):
    """
    Exception for data validation errors.
    
    Requirement: A.4 Error Handling - Validation error handling with detailed error messages
    """
    def __init__(self, code: str, errors: Dict[str, List[str]]) -> None:
        """Initialize validation error with specific error code and validation errors."""
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=400)
        self.errors = errors

class RateLimitError(BaseAPIException):
    """
    Exception for rate limit exceeded errors.
    
    Requirement: A.4 Error Handling - Rate limiting error handling
    """
    def __init__(self) -> None:
        """Initialize rate limit error."""
        code = 'SYS002'
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=429)

class DatabaseError(BaseAPIException):
    """
    Exception for database operation errors.
    
    Requirement: A.4 Error Handling - Database error handling
    """
    def __init__(self) -> None:
        """Initialize database error."""
        code = 'SYS001'
        message = ERROR_CODES[code]
        super().__init__(code=code, message=message, status_code=500)