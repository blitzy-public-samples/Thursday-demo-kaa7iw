"""
Main entry point for the utils package that exposes commonly used utility functions, constants, exceptions, and security helpers.

Human Tasks:
1. Verify that all environment variables are properly set in production:
   - JWT_SECRET_KEY for token generation/validation
   - AES_KEY for sensitive data encryption
2. Review security headers configuration with the security team
3. Confirm rate limiting values are appropriate for production load
4. Validate error codes and messages with the API documentation
"""

# External imports
from typing import Dict, List, Any  # version: 3.9+

# Constants imports
# Requirement: A.4 Error Codes and Messages - Expose error codes for standardized error handling
from .constants import (
    ERROR_CODES,
    SECURITY_HEADERS,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
    MAX_BULLET_ITEMS,
    DATABASE_TIMEOUT,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_PERIOD,
    CACHE_TTL
)

# Exception class imports
# Requirement: A.4 Error Codes and Messages - Expose exception classes for error handling
from .exceptions import (
    BaseAPIException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    ResourceNotFoundError,
    RateLimitError,
    DatabaseError
)

# Validation function imports
# Requirement: 1.2 Scope/4. Data Management - Expose validation utilities
from .validators import (
    validate_project_title,
    validate_specification_content,
    validate_bullet_item,
    validate_bullet_items_count,
    validate_email
)

# Security function imports
# Requirement: 10.3.2 Security Headers - Expose security constants and utility functions
from .security import (
    generate_jwt_token,
    validate_jwt_token,
    encrypt_sensitive_data,
    decrypt_sensitive_data,
    get_security_headers
)

# Helper function imports
# Requirement: 1.2 Scope/4. Data Management - Expose helper utilities
from .helpers import (
    validate_uuid,
    sanitize_string,
    format_timestamp,
    generate_error_response
)

__all__ = [
    # Constants
    'ERROR_CODES',
    'SECURITY_HEADERS',
    
    # Exception classes
    'BaseAPIException',
    'AuthenticationError',
    'AuthorizationError',
    'ValidationError',
    'ResourceNotFoundError',
    'RateLimitError',
    'DatabaseError',
    
    # Validation functions
    'validate_project_title',
    'validate_specification_content',
    'validate_bullet_item',
    'validate_bullet_items_count',
    'validate_email',
    
    # Security functions
    'generate_jwt_token',
    'validate_jwt_token',
    'encrypt_sensitive_data',
    'decrypt_sensitive_data',
    'get_security_headers',
    
    # Helper functions
    'validate_uuid',
    'sanitize_string',
    'format_timestamp',
    'generate_error_response'
]