"""
Validation utilities for data validation across the application.

Human Tasks:
1. Review email regex pattern with security team for compliance
2. Verify maximum content length limits with product team
3. Confirm character restrictions for project titles with UX team
"""

# External imports
import re  # version: 3.9+
from typing import Dict, List  # version: 3.9+

# Internal imports
from .exceptions import ValidationError
from .constants import MAX_BULLET_ITEMS

# Constants for validation
MAX_TITLE_LENGTH: int = 100
MAX_CONTENT_LENGTH: int = 5000
TITLE_PATTERN: str = r'^[a-zA-Z0-9\s\-_\.]+$'
EMAIL_PATTERN: str = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_project_title(title: str) -> bool:
    """
    Validates project title according to requirements.
    
    Requirement: Data Validation - Project title validation rules
    
    Args:
        title: The project title to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If title is invalid with appropriate error code
    """
    if not title or not isinstance(title, str):
        raise ValidationError('PRJ001', {'title': ['Title is required']})
    
    title = title.strip()
    if len(title) == 0 or len(title) > MAX_TITLE_LENGTH:
        raise ValidationError('PRJ001', {
            'title': [f'Title must be between 1 and {MAX_TITLE_LENGTH} characters']
        })
    
    if not re.match(TITLE_PATTERN, title):
        raise ValidationError('PRJ001', {
            'title': ['Title contains invalid characters']
        })
    
    return True

def validate_specification_content(content: str) -> bool:
    """
    Validates specification content according to requirements.
    
    Requirement: Data Validation - Specification content validation
    
    Args:
        content: The specification content to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If content is invalid with appropriate error code
    """
    if not content or not isinstance(content, str):
        raise ValidationError('SPEC001', {'content': ['Content is required']})
    
    content = content.strip()
    if len(content) == 0:
        raise ValidationError('SPEC001', {'content': ['Content cannot be empty']})
    
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValidationError('SPEC001', {
            'content': [f'Content exceeds maximum length of {MAX_CONTENT_LENGTH} characters']
        })
    
    return True

def validate_bullet_item(content: str, order: int) -> bool:
    """
    Validates bullet item content and order according to requirements.
    
    Requirement: Bullet Item Constraints - Content and order validation
    
    Args:
        content: The bullet item content to validate
        order: The order position of the bullet item
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If content or order is invalid with appropriate error code
    """
    if not content or not isinstance(content, str):
        raise ValidationError('ITEM002', {'content': ['Content is required']})
    
    content = content.strip()
    if len(content) == 0:
        raise ValidationError('ITEM002', {'content': ['Content cannot be empty']})
    
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValidationError('ITEM002', {
            'content': [f'Content exceeds maximum length of {MAX_CONTENT_LENGTH} characters']
        })
    
    if not isinstance(order, int):
        raise ValidationError('ITEM002', {'order': ['Order must be an integer']})
    
    if order < 0 or order >= MAX_BULLET_ITEMS:
        raise ValidationError('ITEM002', {
            'order': [f'Order must be between 0 and {MAX_BULLET_ITEMS-1}']
        })
    
    return True

def validate_bullet_items_count(current_count: int) -> bool:
    """
    Validates that specification does not exceed maximum bullet items.
    
    Requirement: Bullet Item Constraints - Maximum items limit validation
    
    Args:
        current_count: The current number of bullet items
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If count exceeds limit with ITEM001 code
    """
    if not isinstance(current_count, int):
        raise ValidationError('ITEM001', {'count': ['Count must be an integer']})
    
    if current_count >= MAX_BULLET_ITEMS:
        raise ValidationError('ITEM001', {
            'count': [f'Cannot exceed maximum of {MAX_BULLET_ITEMS} bullet items']
        })
    
    return True

def validate_email(email: str) -> bool:
    """
    Validates email format.
    
    Requirement: Data Validation - Email format validation
    
    Args:
        email: The email address to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If email format is invalid
    """
    if not email or not isinstance(email, str):
        raise ValidationError('AUTH003', {'email': ['Email is required']})
    
    email = email.strip()
    if len(email) == 0:
        raise ValidationError('AUTH003', {'email': ['Email cannot be empty']})
    
    if not re.match(EMAIL_PATTERN, email):
        raise ValidationError('AUTH003', {'email': ['Invalid email format']})
    
    return True