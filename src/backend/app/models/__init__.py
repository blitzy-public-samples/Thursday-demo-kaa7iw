"""
Package initializer for SQLAlchemy models that exports all database models and establishes model relationships.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for all model operations
2. Review database indexing strategy for all tables
3. Confirm cascade delete settings are properly configured
4. Check database audit logging is enabled for all operations
"""

# External imports - versions specified as per requirements
from typing import List  # version: 3.9+
from sqlalchemy.orm import relationship  # version: 1.4+

# Internal imports - importing models in dependency order
from .base import Base
from .user import User
from .project import Project
from .specification import Specification
from .bullet_item import BulletItem

# Requirement: 1.2 Scope/2. Project Organization - Single-user ownership model
User.projects = relationship(
    "Project",
    back_populates="user",
    cascade="all, delete-orphan",
    doc="List of projects owned by this user"
)

# Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization
Project.specifications = relationship(
    "Specification",
    back_populates="project",
    cascade="all, delete-orphan",
    doc="List of specifications in this project"
)

# Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
Specification.bullet_items = relationship(
    "BulletItem",
    back_populates="specification",
    cascade="all, delete-orphan",
    order_by="BulletItem.order",
    doc="Ordered list of bullet items in this specification"
)

# Export all models
__all__ = [
    'Base',      # Export base model class for inheritance
    'User',      # Export user model for authentication and user management
    'Project',   # Export project model for project management
    'Specification',  # Export specification model for specification management
    'BulletItem'     # Export bullet item model for requirement management
]