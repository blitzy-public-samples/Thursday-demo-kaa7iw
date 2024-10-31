"""
SQLAlchemy model for managing specifications within projects, supporting hierarchical organization and bullet item containment.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for specification operations
2. Review database indexing strategy for specification queries
3. Confirm cascade delete settings are properly configured for bullet items
4. Check database audit logging is enabled for specification operations
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any, List  # version: 3.9+
from sqlalchemy import Column, String, ForeignKey, Boolean, Text  # version: 1.4+
from sqlalchemy.orm import relationship  # version: 1.4+
from sqlalchemy.dialects.postgresql import UUID  # version: 1.4+

# Internal imports
from .base import Base
from .project import Project

class Specification(Base):
    """
    SQLAlchemy model representing a specification within a project that can contain bullet items.
    
    Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization of specifications
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    """
    
    __tablename__ = 'specifications'
    
    # Foreign key to project table
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey('projects.id', ondelete='CASCADE'),
        nullable=False,
        doc="ID of the project this specification belongs to"
    )
    
    # Specification content
    content = Column(
        Text,
        nullable=False,
        doc="Content of the specification"
    )
    
    # Relationships
    project = relationship(
        "Project",
        back_populates="specifications",
        doc="Project that owns this specification"
    )
    
    bullet_items = relationship(
        "BulletItem",
        back_populates="specification",
        cascade="all, delete-orphan",
        order_by="BulletItem.order",
        doc="Ordered list of bullet items in this specification"
    )
    
    def __init__(self, project_id: UUID, content: str) -> None:
        """
        Initialize a new specification instance.
        
        Requirement: 1.2 Scope/3. Specification Management - Specification creation
        
        Args:
            project_id: ID of the project this specification belongs to
            content: Content of the specification
            
        Raises:
            ValueError: If content is empty or invalid
        """
        super().__init__()
        
        # Validate content is not empty
        if not content or not content.strip():
            raise ValueError("Specification content cannot be empty")
        
        self.project_id = project_id
        self.content = content.strip()
        self.bullet_items = []
    
    def validate_project_access(self, project_id: UUID) -> bool:
        """
        Validate if specification belongs to given project.
        
        Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
        
        Args:
            project_id: ID of the project to check access against
            
        Returns:
            bool: True if specification belongs to project, False otherwise
        """
        return self.project_id == project_id
    
    def get_bullet_items(self) -> List["BulletItem"]:
        """
        Retrieve all active bullet items in this specification ordered by their order field.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
        
        Returns:
            List[BulletItem]: Ordered list of specification's active bullet items
        """
        return [
            item for item in self.bullet_items 
            if not item.is_deleted
        ]
    
    def validate_bullet_item_limit(self) -> bool:
        """
        Check if specification can accept more bullet items.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
        
        Returns:
            bool: True if under 10 items limit, False otherwise
        """
        active_items = len(self.get_bullet_items())
        return active_items < 10
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert specification instance to dictionary representation.
        
        Requirement: 1.2 Scope/4. Data Management - Data serialization
        
        Returns:
            Dict[str, Any]: Dictionary representation of specification
        """
        # Get base dictionary from parent class
        base_dict = super().to_dict()
        
        # Add specification-specific fields
        spec_dict = {
            'project_id': str(self.project_id),
            'content': self.content,
            'bullet_item_count': len(self.get_bullet_items())
        }
        
        # Combine base and specification-specific dictionaries
        return {**base_dict, **spec_dict}