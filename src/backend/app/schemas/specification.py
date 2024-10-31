"""
Marshmallow schema definitions for specification data validation and serialization.

Human Tasks:
1. Review validation error messages with product team for user-friendliness
2. Verify error code mappings with API documentation team
3. Confirm maximum content length with UX team
"""

# External imports
from marshmallow import Schema, fields, validates, ValidationError  # version: 3.0+
from typing import Any  # version: 3.9+
from uuid import UUID

# Internal imports
from ..models.specification import Specification
from .bullet_item import BulletItemSchema

class SpecificationSchema(Schema):
    """
    Base Marshmallow schema for specification serialization and validation.
    
    Requirement: Data Management - Data validation and constraint enforcement for specifications
    """
    
    # Primary fields
    spec_id = fields.UUID(dump_only=True)
    project_id = fields.UUID(required=True)
    content = fields.String(required=True)
    
    # Nested fields
    bullet_items = fields.Nested(
        BulletItemSchema,
        many=True,
        dump_only=True
    )
    
    # Timestamps
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        """Schema metadata configuration."""
        model = Specification
        ordered = True
        unknown = fields.EXCLUDE
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize schema with marshmallow configuration.
        
        Requirement: Data Management - Schema configuration for validation
        """
        super().__init__(*args, **kwargs)
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Validate specification content is not empty.
        
        Requirement: Data Management - Data validation and constraint enforcement
        
        Args:
            content: The specification content to validate
            
        Returns:
            bool: True if content is valid
            
        Raises:
            ValidationError: If content validation fails
        """
        if not content or not content.strip():
            raise ValidationError("Specification content cannot be empty")
        
        # Additional content validation could be added here
        # e.g., length limits, format requirements, etc.
        
        return True

class SpecificationCreateSchema(Schema):
    """
    Schema for validating specification creation requests.
    
    Requirement: Data Management - Data validation for specification creation
    """
    
    project_id = fields.UUID(required=True)
    content = fields.String(required=True)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize create schema with required fields only.
        
        Requirement: Data Management - Schema configuration for creation validation
        """
        super().__init__(*args, **kwargs)
        self.unknown = fields.EXCLUDE
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Validate content for specification creation.
        
        Args:
            content: The specification content
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If content is invalid
        """
        if not content or not content.strip():
            raise ValidationError("Specification content cannot be empty")
        return True

class SpecificationUpdateSchema(Schema):
    """
    Schema for validating specification update requests.
    
    Requirement: Data Management - Data validation for specification updates
    """
    
    content = fields.String(required=True)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize update schema with partial validation.
        
        Requirement: Data Management - Schema configuration for partial updates
        """
        super().__init__(*args, **kwargs)
        self.unknown = fields.EXCLUDE
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Validate content for specification update.
        
        Args:
            content: The specification content
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If content is invalid
        """
        if not content or not content.strip():
            raise ValidationError("Specification content cannot be empty")
        return True