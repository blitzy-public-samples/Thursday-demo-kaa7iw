"""
Database operations module providing generic CRUD operations and transaction management.

Human Tasks:
1. Verify PostgreSQL connection settings in environment variables
2. Review database user permissions for CRUD operations
3. Confirm database backup and recovery procedures
4. Check monitoring setup for database operations
"""

# External imports - versions specified as per requirements
from typing import Dict, List, Optional, Type, TypeVar, Any  # version: 3.9+
from uuid import UUID  # version: 3.9+
from sqlalchemy import and_  # version: 1.4+
from sqlalchemy.orm import Query  # version: 1.4+

# Internal imports
from .session import session_scope
from ..models.base import Base
from ..utils.exceptions import DatabaseError

# Type variable for generic model operations
T = TypeVar('T', bound=Base)

def create_record(model_class: Type[T], data: Dict[str, Any]) -> T:
    """
    Create a new record in the database.
    
    Args:
        model_class: SQLAlchemy model class
        data: Dictionary containing model attributes
        
    Returns:
        T: Created model instance
        
    Raises:
        DatabaseError: If database operation fails
        
    Requirement: 1.2 Scope/4. Data Management - CRUD operations for projects, specifications, and bullet items
    """
    try:
        with session_scope() as session:
            # Create new instance with provided data
            instance = model_class(**data)
            session.add(instance)
            session.flush()  # Flush to get the ID without committing
            
            # Refresh instance to ensure all relationships are loaded
            session.refresh(instance)
            return instance
    except Exception as e:
        raise DatabaseError() from e

def get_record(model_class: Type[T], record_id: UUID) -> Optional[T]:
    """
    Retrieve a record by ID.
    
    Args:
        model_class: SQLAlchemy model class
        record_id: UUID of the record to retrieve
        
    Returns:
        Optional[T]: Found model instance or None
        
    Raises:
        DatabaseError: If database operation fails
        
    Requirement: 1.2 Scope/4. Data Management - Data retrieval operations
    """
    try:
        with session_scope() as session:
            # Query for record with given ID that isn't soft deleted
            return session.query(model_class).filter(
                and_(
                    model_class.id == record_id,
                    model_class.is_deleted.is_(False)
                )
            ).first()
    except Exception as e:
        raise DatabaseError() from e

def update_record(record: T, data: Dict[str, Any]) -> T:
    """
    Update an existing record.
    
    Args:
        record: Model instance to update
        data: Dictionary containing updated attributes
        
    Returns:
        T: Updated model instance
        
    Raises:
        DatabaseError: If database operation fails
        
    Requirement: 1.2 Scope/4. Data Management - Data update operations
    """
    try:
        with session_scope() as session:
            # Update record with provided data
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            
            session.add(record)
            session.flush()
            session.refresh(record)
            return record
    except Exception as e:
        raise DatabaseError() from e

def delete_record(record: T) -> None:
    """
    Soft delete a record.
    
    Args:
        record: Model instance to delete
        
    Raises:
        DatabaseError: If database operation fails
        
    Requirement: 1.2 Scope/4. Data Management - Data deletion operations
    Requirement: 10.2.3 Database Security - Secure deletion with audit trail
    """
    try:
        with session_scope() as session:
            # Perform soft delete
            record.soft_delete()
            session.add(record)
    except Exception as e:
        raise DatabaseError() from e

def list_records(
    model_class: Type[T],
    filters: Optional[Dict[str, Any]] = None
) -> List[T]:
    """
    List all records of a model class with optional filtering.
    
    Args:
        model_class: SQLAlchemy model class
        filters: Optional dictionary of filter conditions
        
    Returns:
        List[T]: List of model instances
        
    Raises:
        DatabaseError: If database operation fails
        
    Requirement: 1.2 Scope/4. Data Management - Data listing and filtering
    """
    try:
        with session_scope() as session:
            # Start with base query excluding soft deleted records
            query: Query = session.query(model_class).filter(
                model_class.is_deleted.is_(False)
            )
            
            # Apply additional filters if provided
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    if hasattr(model_class, key):
                        filter_conditions.append(getattr(model_class, key) == value)
                
                if filter_conditions:
                    query = query.filter(and_(*filter_conditions))
            
            # Execute query and return results
            return query.all()
    except Exception as e:
        raise DatabaseError() from e