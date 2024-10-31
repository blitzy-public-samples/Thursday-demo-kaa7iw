"""
SQLAlchemy model for managing projects, which are containers for specifications owned by a single user.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for project operations
2. Review database indexing strategy for project queries
3. Confirm cascade delete settings are properly configured
4. Check database audit logging is enabled for project operations
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any, List  # version: 3.9+
from sqlalchemy import Column, String, ForeignKey, Boolean  # version: 1.4+
from sqlalchemy.orm import relationship  # version: 1.4+
from sqlalchemy.dialects.postgresql import UUID  # version: 1.4+

# Internal imports
from .base import Base
from .user import User

class Project(Base):
    """
    SQLAlchemy model representing a project that contains specifications and is owned by a user.
    
    Requirement: 1.2 Scope/2. Project Organization - Creation and management of projects
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    """
    
    __tablename__ = 'projects'
    
    # Project title with length constraint
    title = Column(
        String(100),
        nullable=False,
        doc="Title of the project"
    )
    
    # Foreign key to user table
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        doc="ID of the user who owns this project"
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="projects",
        doc="User who owns this project"
    )
    
    specifications = relationship(
        "Specification",
        back_populates="project",
        cascade="all, delete-orphan",
        doc="List of specifications in this project"
    )
    
    def __init__(self, title: str, user_id: UUID) -> None:
        """
        Initialize a new project instance.
        
        Requirement: 1.2 Scope/2. Project Organization - Single-user ownership model
        
        Args:
            title: Title of the project
            user_id: ID of the user who owns this project
            
        Raises:
            ValueError: If title is empty or invalid
        """
        super().__init__()
        
        # Validate and set title
        if not title or not title.strip():
            raise ValueError("Project title cannot be empty")
        
        self.title = title.strip()
        self.user_id = user_id
        self.specifications = []
    
    def validate_ownership(self, user_id: UUID) -> bool:
        """
        Validate if project belongs to given user.
        
        Requirement: 1.2 Scope/2. Project Organization - Project-level access control
        
        Args:
            user_id: ID of the user to check ownership against
            
        Returns:
            bool: True if user owns project, False otherwise
        """
        return self.user_id == user_id
    
    def get_specifications(self) -> List["Specification"]:
        """
        Retrieve all active specifications in this project.
        
        Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization
        
        Returns:
            List[Specification]: List of active specifications in this project
        """
        return [
            spec for spec in self.specifications 
            if not spec.is_deleted
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert project instance to dictionary representation.
        
        Requirement: 1.2 Scope/4. Data Management - Data serialization
        
        Returns:
            Dict[str, Any]: Dictionary representation of project
        """
        # Get base dictionary from parent class
        base_dict = super().to_dict()
        
        # Add project-specific fields
        project_dict = {
            'title': self.title,
            'user_id': str(self.user_id),
            'specification_count': len(self.get_specifications())
        }
        
        # Combine base and project-specific dictionaries
        return {**base_dict, **project_dict}