"""
SQLAlchemy model for managing bullet items within specifications, supporting ordered requirement entries.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for bullet item operations
2. Review database indexing strategy for bullet item queries
3. Confirm cascade delete settings are properly configured
4. Check database audit logging is enabled for bullet item operations
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any  # version: 3.9+
from sqlalchemy import Column, String, ForeignKey, Integer, Text  # version: 1.4+
from sqlalchemy.orm import relationship  # version: 1.4+
from sqlalchemy.dialects.postgresql import UUID  # version: 1.4+

# Internal imports
from .base import Base
from .specification import Specification

class BulletItem(Base):
    """
    SQLAlchemy model representing an ordered bullet item within a specification.
    
    Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    """
    
    __tablename__ = 'bullet_items'
    
    # Foreign key to specification table
    spec_id = Column(
        UUID(as_uuid=True),
        ForeignKey('specifications.id', ondelete='CASCADE'),
        nullable=False,
        doc="ID of the specification this bullet item belongs to"
    )
    
    # Bullet item content
    content = Column(
        Text,
        nullable=False,
        doc="Content of the bullet item"
    )
    
    # Order within specification (0-9)
    order = Column(
        Integer,
        nullable=False,
        doc="Order of the bullet item within its specification (0-9)"
    )
    
    # Relationship to specification
    specification = relationship(
        "Specification",
        back_populates="bullet_items",
        doc="Specification that owns this bullet item"
    )
    
    def __init__(self, spec_id: UUID, content: str, order: int) -> None:
        """
        Initialize a new bullet item instance.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
        
        Args:
            spec_id: ID of the specification this bullet item belongs to
            content: Content of the bullet item
            order: Order within the specification (0-9)
            
        Raises:
            ValueError: If content is empty or order is invalid
        """
        super().__init__()
        
        # Validate content is not empty
        if not content or not content.strip():
            raise ValueError("Bullet item content cannot be empty")
            
        # Validate order is within allowed range
        if not self.validate_order(order):
            raise ValueError("Bullet item order must be between 0 and 9")
        
        self.spec_id = spec_id
        self.content = content.strip()
        self.order = order
    
    def validate_order(self, order: int) -> bool:
        """
        Validate if the order value is within allowed range.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
        
        Args:
            order: Order value to validate
            
        Returns:
            bool: True if order is valid (0-9), False otherwise
        """
        try:
            order_int = int(order)
            return 0 <= order_int <= 9
        except (TypeError, ValueError):
            return False
    
    def validate_spec_access(self, spec_id: UUID) -> bool:
        """
        Validate if bullet item belongs to given specification.
        
        Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
        
        Args:
            spec_id: ID of the specification to check access against
            
        Returns:
            bool: True if bullet item belongs to specification, False otherwise
        """
        return self.spec_id == spec_id
    
    def update_order(self, new_order: int) -> None:
        """
        Update the order of the bullet item.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
        
        Args:
            new_order: New order value for the bullet item
            
        Raises:
            ValueError: If new order is invalid
        """
        if not self.validate_order(new_order):
            raise ValueError("New order must be between 0 and 9")
            
        self.order = new_order
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert bullet item instance to dictionary representation.
        
        Requirement: 1.2 Scope/4. Data Management - Data serialization
        
        Returns:
            Dict[str, Any]: Dictionary representation of bullet item
        """
        # Get base dictionary from parent class
        base_dict = super().to_dict()
        
        # Add bullet item specific fields
        bullet_dict = {
            'spec_id': str(self.spec_id),
            'content': self.content,
            'order': self.order
        }
        
        # Combine base and bullet item specific dictionaries
        return {**base_dict, **bullet_dict}