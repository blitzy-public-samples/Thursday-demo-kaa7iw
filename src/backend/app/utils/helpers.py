"""
Utility helper functions providing common functionality across the application.

Human Tasks:
1. Verify that the HTML tag removal regex patterns are comprehensive for your use case
2. Confirm SQL injection patterns are up to date with latest security recommendations
3. Review project title validation rules with the product team
4. Ensure timestamp format matches the frontend requirements
"""

# External imports
from typing import Dict, List, Any  # version: 3.9+
from datetime import datetime  # version: 3.9+
import uuid  # version: 3.9+
import re  # version: 3.9+

# Internal imports
from .constants import ERROR_CODES
from .exceptions import ValidationError

# Requirement: 10.2 Data Security - Regular expressions for input sanitization
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
SCRIPT_TAG_PATTERN = re.compile(r'<script[^>]*>.*?</script>', re.DOTALL)
SQL_INJECTION_PATTERN = re.compile(r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b)', re.IGNORECASE)
PROJECT_TITLE_PATTERN = re.compile(r'^[\w\s\-\.]{1,100}$')

def validate_uuid(uuid_string: str) -> bool:
    """
    Validates if a given string is a valid UUID.
    
    Requirement: 1.2 Scope/4. Data Management - Data validation for UUID fields
    
    Args:
        uuid_string: String to validate as UUID
        
    Returns:
        bool: True if valid UUID, False otherwise
    """
    try:
        uuid.UUID(str(uuid_string))
        return True
    except ValueError:
        return False

def validate_bullet_order(order: int) -> bool:
    """
    Validates if a bullet item order is within allowed range (0-9).
    
    Requirement: 1.2 Scope/3. Specification Management - Bullet item order validation
    
    Args:
        order: Integer order value to validate
        
    Returns:
        bool: True if valid order, False otherwise
    """
    return isinstance(order, int) and 0 <= order <= 9

def sanitize_string(input_string: str) -> str:
    """
    Sanitizes input string by removing dangerous characters and patterns.
    
    Requirement: 10.2 Data Security - Input sanitization for security
    
    Args:
        input_string: String to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not isinstance(input_string, str):
        return ""
    
    # Remove HTML and script tags
    sanitized = HTML_TAG_PATTERN.sub('', input_string)
    sanitized = SCRIPT_TAG_PATTERN.sub('', sanitized)
    
    # Remove potential SQL injection patterns
    sanitized = SQL_INJECTION_PATTERN.sub('', sanitized)
    
    # Strip whitespace and normalize spaces
    sanitized = ' '.join(sanitized.split())
    
    return sanitized

def format_timestamp(timestamp: datetime) -> str:
    """
    Formats datetime object to ISO 8601 string.
    
    Requirement: 1.2 Scope/4. Data Management - Standardized timestamp formatting
    
    Args:
        timestamp: Datetime object to format
        
    Returns:
        str: ISO 8601 formatted timestamp string
    """
    if not isinstance(timestamp, datetime):
        raise ValueError("Input must be a datetime object")
    
    return timestamp.isoformat()

def validate_project_title(title: str) -> bool:
    """
    Validates project title against required constraints.
    
    Requirement: 1.2 Scope/2. Project Organization - Project title validation
    
    Args:
        title: Project title to validate
        
    Returns:
        bool: True if valid title, False otherwise
    """
    if not isinstance(title, str):
        return False
    
    # Check length and character constraints using regex pattern
    return bool(PROJECT_TITLE_PATTERN.match(title))

def generate_error_response(error_code: str, validation_errors: Dict[str, List[str]] = None) -> Dict[str, Any]:
    """
    Generates standardized error response dictionary.
    
    Requirement: A.4 Error Codes and Messages - Standardized error response format
    
    Args:
        error_code: Error code from ERROR_CODES
        validation_errors: Optional dictionary of field-specific validation errors
        
    Returns:
        Dict[str, Any]: Standardized error response dictionary
        
    Raises:
        KeyError: If error_code is not found in ERROR_CODES
    """
    if error_code not in ERROR_CODES:
        raise KeyError(f"Unknown error code: {error_code}")
    
    response = {
        "code": error_code,
        "message": ERROR_CODES[error_code],
        "timestamp": format_timestamp(datetime.utcnow())
    }
    
    if validation_errors:
        response["errors"] = validation_errors
    
    return response