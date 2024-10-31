"""
Marshmallow schemas for authentication-related request/response validation and serialization.

Human Tasks:
1. Verify Google OAuth token validation rules with the security team
2. Confirm JWT token expiration settings with the auth service team
3. Review email validation regex pattern for security compliance
"""

# External imports
from marshmallow import Schema, fields, validates, ValidationError  # version: 3.0+
from typing import Any, Dict  # version: 3.9+
from datetime import datetime
import uuid

# Internal imports
from ..utils.validators import validate_email
from ..utils.constants import ERROR_CODES, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

class LoginRequestSchema(Schema):
    """
    Schema for validating Google OAuth login requests.
    
    Requirement: User Management - Secure authentication through Google Cloud User Store
    """
    google_token = fields.String(required=True)
    
    @validates("google_token")
    def validate_token(self, value: str) -> str:
        """Validates the Google OAuth token format."""
        if not value or not isinstance(value, str):
            raise ValidationError(ERROR_CODES["AUTH003"])
            
        # Basic token format validation - should be a non-empty string
        value = value.strip()
        if len(value) == 0:
            raise ValidationError(ERROR_CODES["AUTH003"])
            
        # Token should be a reasonable length
        if len(value) < 20 or len(value) > 2048:  # Standard OAuth2 token length limits
            raise ValidationError(ERROR_CODES["AUTH003"])
            
        return value

class LoginResponseSchema(Schema):
    """
    Schema for serializing successful login responses.
    
    Requirement: User Management - Session management with JWT tokens
    """
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    expires_in = fields.Integer(required=True, default=JWT_ACCESS_TOKEN_EXPIRES)
    token_type = fields.String(required=True, default="Bearer")

class TokenRefreshSchema(Schema):
    """
    Schema for validating token refresh requests.
    
    Requirement: User Management - Session management with JWT tokens
    """
    refresh_token = fields.String(required=True)
    
    @validates("refresh_token")
    def validate_refresh_token(self, value: str) -> str:
        """Validates the refresh token format."""
        if not value or not isinstance(value, str):
            raise ValidationError(ERROR_CODES["AUTH001"])
            
        value = value.strip()
        if len(value) == 0:
            raise ValidationError(ERROR_CODES["AUTH001"])
            
        # JWT tokens should be three dot-separated base64 strings
        parts = value.split('.')
        if len(parts) != 3:
            raise ValidationError(ERROR_CODES["AUTH001"])
            
        return value

class UserSchema(Schema):
    """
    Schema for serializing user information.
    
    Requirement: Data Validation - Data validation and constraint enforcement
    """
    id = fields.UUID(required=True)
    email = fields.Email(required=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    last_login = fields.DateTime(allow_none=True)
    
    @validates("email")
    def validate_email(self, value: str) -> str:
        """Validates email format using validator utility."""
        try:
            validate_email(value)
            return value
        except ValidationError as e:
            raise ValidationError(str(e))