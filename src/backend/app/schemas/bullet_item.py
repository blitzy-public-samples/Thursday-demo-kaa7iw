"""
Marshmallow schema definitions for bullet item data validation and serialization.

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
from ..models.bullet_item import BulletItem
from ..utils.validators import validate_bullet_item

class BulletItemSchema(Schema):
    """
    Marshmallow schema for validating and serializing bullet item data.
    
    Requirement: Data Management - Data validation and constraint enforcement for bullet items
    """
    
    # Primary fields
    id = fields.UUID(dump_only=True)
    spec_id = fields.UUID(required=True)
    content = fields.String(required=True)
    order = fields.Integer(required=True)
    
    # Timestamps
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        """Schema metadata configuration."""
        model = BulletItem
        ordered = True
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Custom validator for bullet item content.
        
        Requirement: Data Management - Data validation and constraint enforcement
        
        Args:
            content: The bullet item content to validate
            
        Returns:
            bool: True if content is valid
            
        Raises:
            ValidationError: If content validation fails
        """
        try:
            return validate_bullet_item(content, 0)  # Order is validated separately
        except ValidationError as e:
            raise ValidationError(e.messages.get('content', ['Invalid content']))
    
    @validates("order")
    def validate_order(self, order: int) -> bool:
        """
        Custom validator for bullet item order.
        
        Requirement: Specification Management - Support for up to 10 ordered bullet items
        
        Args:
            order: The order value to validate
            
        Returns:
            bool: True if order is valid
            
        Raises:
            ValidationError: If order is invalid
        """
        if not isinstance(order, int) or order < 0 or order > 9:
            raise ValidationError("Order must be between 0 and 9")
        return True

class BulletItemCreateSchema(Schema):
    """
    Schema for validating bullet item creation requests.
    
    Requirement: Data Management - Data validation for bullet item creation
    """
    
    content = fields.String(required=True)
    order = fields.Integer(required=True)
    spec_id = fields.UUID(required=True)
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Validate content for bullet item creation.
        
        Args:
            content: The bullet item content
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If content is invalid
        """
        try:
            return validate_bullet_item(content, 0)  # Order validated separately
        except ValidationError as e:
            raise ValidationError(e.messages.get('content', ['Invalid content']))
    
    @validates("order")
    def validate_order(self, order: int) -> bool:
        """
        Validate order for bullet item creation.
        
        Args:
            order: The order value
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If order is invalid
        """
        if not isinstance(order, int) or order < 0 or order > 9:
            raise ValidationError("Order must be between 0 and 9")
        return True

class BulletItemUpdateSchema(Schema):
    """
    Schema for validating bullet item update requests.
    
    Requirement: Data Management - Data validation for bullet item updates
    """
    
    content = fields.String(required=False)
    order = fields.Integer(required=False)
    
    @validates("content")
    def validate_content(self, content: str) -> bool:
        """
        Validate content for bullet item update.
        
        Args:
            content: The bullet item content
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If content is invalid
        """
        try:
            return validate_bullet_item(content, 0)  # Order validated separately
        except ValidationError as e:
            raise ValidationError(e.messages.get('content', ['Invalid content']))
    
    @validates("order")
    def validate_order(self, order: int) -> bool:
        """
        Validate order for bullet item update.
        
        Args:
            order: The order value
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If order is invalid
        """
        if not isinstance(order, int) or order < 0 or order > 9:
            raise ValidationError("Order must be between 0 and 9")
        return True