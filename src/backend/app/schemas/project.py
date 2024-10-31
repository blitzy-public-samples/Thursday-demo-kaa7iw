"""
Marshmallow schema for project data validation and serialization.

Human Tasks:
1. Verify that the error codes match the API documentation
2. Confirm the datetime format with the frontend team
3. Review the validation rules with the product team
"""

# External imports
from marshmallow import Schema, fields, validates, ValidationError  # version: 3.0+
from typing import Any  # version: 3.9+
from datetime import datetime

# Internal imports
from ..utils.validators import validate_project_title
from ..utils.constants import ERROR_CODES

class ProjectSchema(Schema):
    """
    Marshmallow schema for project data validation and serialization.
    
    Requirement: Project Organization - Creation and management of projects with single-user ownership model
    """
    id = fields.UUID(required=True, dump_only=True)
    title = fields.String(required=True)
    user_id = fields.UUID(required=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Boolean(dump_only=True)

    @validates('title')
    def validate_title(self, value: str) -> str:
        """
        Custom validator for project title field.
        
        Requirement: Data Management - Data validation and constraint enforcement for project operations
        
        Args:
            value: The project title to validate
            
        Returns:
            str: Validated title if valid
            
        Raises:
            ValidationError: If validation fails with PRJ001 code
        """
        try:
            validate_project_title(value)
            return value
        except ValidationError as e:
            raise ValidationError(
                ERROR_CODES['PRJ001'],
                field_name='title'
            )

class ProjectCreateSchema(Schema):
    """
    Schema for validating project creation requests.
    
    Requirement: Project Organization - Creation and management of projects with single-user ownership model
    """
    title = fields.String(required=True)

    @validates('title')
    def validate_title(self, value: str) -> str:
        """
        Custom validator for project title field during creation.
        
        Requirement: Data Management - Data validation and constraint enforcement for project operations
        
        Args:
            value: The project title to validate
            
        Returns:
            str: Validated title if valid
            
        Raises:
            ValidationError: If validation fails with PRJ001 code
        """
        try:
            validate_project_title(value)
            return value
        except ValidationError as e:
            raise ValidationError(
                ERROR_CODES['PRJ001'],
                field_name='title'
            )

class ProjectUpdateSchema(Schema):
    """
    Schema for validating project update requests.
    
    Requirement: Project Organization - Creation and management of projects with single-user ownership model
    """
    title = fields.String(required=True)

    @validates('title')
    def validate_title(self, value: str) -> str:
        """
        Custom validator for project title field during update.
        
        Requirement: Data Management - Data validation and constraint enforcement for project operations
        
        Args:
            value: The project title to validate
            
        Returns:
            str: Validated title if valid
            
        Raises:
            ValidationError: If validation fails with PRJ001 code
        """
        try:
            validate_project_title(value)
            return value
        except ValidationError as e:
            raise ValidationError(
                ERROR_CODES['PRJ001'],
                field_name='title'
            )