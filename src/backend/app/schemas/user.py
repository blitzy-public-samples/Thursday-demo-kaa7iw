"""
Marshmallow schema for user data serialization and validation.

Human Tasks:
1. Review email validation regex pattern with security team
2. Verify field length constraints with product team
3. Confirm datetime format requirements with frontend team
"""

# External imports - versions specified as per requirements
from marshmallow import Schema, fields, validates, ValidationError  # version: 3.0+
from typing import Any  # version: 3.9+

# Internal imports
from ..models.user import User
from ..utils.validators import validate_email

class UserSchema(Schema):
    """
    Marshmallow schema for serializing and deserializing user data.
    
    Requirement: 1.2 Scope/1. User Management - User-specific data validation
    Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
    """
    
    # Read-only fields
    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    
    # Read-write fields
    email = fields.Email(required=True)
    name = fields.String(required=True)
    
    class Meta:
        """Schema configuration."""
        ordered = True
        
    @validates('email')
    def validate_email(self, value: str) -> str:
        """
        Custom email validator using application's email validation rules.
        
        Requirement: 1.2 Scope/4. Data Management - Data validation
        
        Args:
            value: Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email validation fails
        """
        try:
            validate_email(value)
            return value
        except ValidationError as e:
            raise ValidationError(e.messages['email'])

class UserCreateSchema(Schema):
    """
    Schema for user creation requests.
    
    Requirement: 1.2 Scope/1. User Management - User data validation
    """
    
    email = fields.Email(required=True)
    name = fields.String(required=True)
    
    class Meta:
        """Schema configuration."""
        ordered = True
        
    @validates('email')
    def validate_email(self, value: str) -> str:
        """
        Validate email for user creation.
        
        Args:
            value: Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email validation fails
        """
        try:
            validate_email(value)
            return value
        except ValidationError as e:
            raise ValidationError(e.messages['email'])

class UserUpdateSchema(Schema):
    """
    Schema for user update requests.
    
    Requirement: 1.2 Scope/1. User Management - User data validation
    """
    
    name = fields.String(required=True)
    
    class Meta:
        """Schema configuration."""
        ordered = True