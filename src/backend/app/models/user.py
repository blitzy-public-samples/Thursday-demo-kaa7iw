"""
SQLAlchemy model for user management, handling user data persistence and authentication-related functionality.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for encryption operations
2. Ensure environment variables for encryption keys are properly configured
3. Review email validation regex pattern with security team
4. Confirm database audit logging is enabled for user operations
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any  # version: 3.9+
from sqlalchemy import Column, String, DateTime, Boolean  # version: 1.4+

# Internal imports
from .base import Base
from ..utils.security import encrypt_sensitive_data, decrypt_sensitive_data
from ..utils.validators import validate_email

class User(Base):
    """
    SQLAlchemy model representing a user in the system.
    
    Requirement: 1.2 Scope/1. User Management - Secure user data persistence
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    """
    
    __tablename__ = 'users'
    
    # Email is stored encrypted for security
    email = Column(
        String(255),
        nullable=False,
        unique=True,
        doc="Encrypted email address of the user"
    )
    
    name = Column(
        String(100),
        nullable=False,
        doc="Display name of the user"
    )
    
    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of user's last login"
    )
    
    def __init__(self, email: str, name: str) -> None:
        """
        Initialize a new user instance.
        
        Requirement: 1.2 Scope/1. User Management - User data validation
        
        Args:
            email: User's email address
            name: User's display name
            
        Raises:
            ValidationError: If email format is invalid
        """
        super().__init__()
        
        # Validate and set email
        validate_email(email)
        self.email = encrypt_sensitive_data(email.lower().strip())
        
        # Set name
        self.name = name.strip()
        
        # Initialize timestamps
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_login = None
        self.is_deleted = False
    
    def get_email(self) -> str:
        """
        Get decrypted email address.
        
        Requirement: 10.2.2 Encryption Standards - Secure data decryption
        
        Returns:
            str: Decrypted email address
        """
        return decrypt_sensitive_data(self.email)
    
    def set_email(self, email: str) -> None:
        """
        Set and encrypt email address.
        
        Requirement: 10.2.2 Encryption Standards - Secure data encryption
        Requirement: 1.2 Scope/4. Data Management - Data validation
        
        Args:
            email: New email address to set
            
        Raises:
            ValidationError: If email format is invalid
        """
        validate_email(email)
        self.email = encrypt_sensitive_data(email.lower().strip())
        self.updated_at = datetime.utcnow()
    
    def update_last_login(self) -> None:
        """
        Update the last login timestamp.
        
        Requirement: 1.2 Scope/1. User Management - Login tracking
        """
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user instance to dictionary.
        
        Requirement: 1.2 Scope/4. Data Management - Data serialization
        
        Returns:
            Dict[str, Any]: Dictionary representation of user
        """
        base_dict = super().to_dict()
        
        # Add user-specific fields with decrypted email
        user_dict = {
            'email': self.get_email(),
            'name': self.name,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        # Combine base and user-specific dictionaries
        return {**base_dict, **user_dict}