"""
Base model class providing common SQLAlchemy model functionality.

Human Tasks:
1. Verify PostgreSQL extensions for UUID support are enabled
2. Review database audit logging configuration
3. Confirm row-level security policies are properly configured
4. Check database user permissions for CRUD operations
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any  # version: 3.9+
from uuid import uuid4  # version: 3.9+
from sqlalchemy.ext.declarative import declarative_base  # version: 1.4+
from sqlalchemy import Column, DateTime, Boolean  # version: 1.4+
from sqlalchemy.dialects.postgresql import UUID  # version: 1.4+

# Internal imports
from ..database.session import DatabaseSession, session_scope

# Create declarative base class
Base = declarative_base()

class Base(Base):
    """
    SQLAlchemy declarative base class that all models inherit from.
    
    Requirement: 1.1 System Overview/Data Access Layer - PostgreSQL database interactions
    Requirement: 1.2 Scope/4. Data Management - CRUD operations and data validation
    Requirement: 10.2.3 Database Security - Secure database operations with audit logging
    """
    
    __abstract__ = True  # Marks this as an abstract base class
    
    # Common columns for all models
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
        unique=True,
        doc="Unique identifier for the record"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp when the record was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Timestamp when the record was last updated"
    )
    
    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="Soft delete flag for the record"
    )
    
    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize base model with common fields.
        
        Args:
            **kwargs: Keyword arguments for model attributes
        """
        if 'id' not in kwargs:
            kwargs['id'] = uuid4()
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        if 'is_deleted' not in kwargs:
            kwargs['is_deleted'] = False
            
        super().__init__(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of model instance
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            
            # Convert datetime objects to ISO format
            if isinstance(value, datetime):
                value = value.isoformat()
            
            # Convert UUID objects to string
            elif isinstance(value, uuid4.__class__):
                value = str(value)
                
            result[column.name] = value
            
        return result
    
    def soft_delete(self) -> None:
        """
        Mark record as deleted without removing from database.
        
        Requirement: 10.2.3 Database Security - Audit logging for data changes
        """
        with session_scope() as session:
            self.is_deleted = True
            self.updated_at = datetime.utcnow()
            session.add(self)
    
    def update(self, attributes: Dict[str, Any]) -> None:
        """
        Update model with provided attributes.
        
        Args:
            attributes: Dictionary of attributes to update
            
        Requirement: 1.2 Scope/4. Data Management - Data validation for updates
        """
        with session_scope() as session:
            for key, value in attributes.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            
            self.updated_at = datetime.utcnow()
            session.add(self)