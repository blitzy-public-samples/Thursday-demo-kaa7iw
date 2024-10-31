"""
Database session management module for PostgreSQL connection pooling and transaction management.

Human Tasks:
1. Verify DATABASE_URL environment variable is set with correct PostgreSQL connection string
2. Ensure database user has appropriate permissions for table creation
3. Confirm PostgreSQL server configuration matches connection pool settings
4. Review database timeout settings with the operations team
"""

# External imports
from contextlib import contextmanager  # version: 3.9+
from typing import Generator  # version: 3.9+
import logging
from sqlalchemy import create_engine  # version: 1.4+
from sqlalchemy.orm import sessionmaker, Session  # version: 1.4+
from sqlalchemy.exc import SQLAlchemyError

# Internal imports
from ..utils.constants import DATABASE_TIMEOUT
from ..utils.exceptions import DatabaseError

# Configure logging
logger = logging.getLogger(__name__)

# Database connection configuration
# Requirement: 1.1 System Overview/Data Access Layer - PostgreSQL database configuration
DATABASE_URL = "postgresql://user:password@localhost:5432/db"  # Override with environment variable
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Maximum number of permanent connections
    max_overflow=20,  # Maximum number of additional connections
    pool_timeout=DATABASE_TIMEOUT,  # Connection timeout in seconds
    pool_recycle=1800  # Recycle connections after 30 minutes
)

# Create session factory with expire_on_commit=False to prevent detached instance errors
# Requirement: 1.2 Scope/4. Data Management - Session management for CRUD operations
Session = sessionmaker(bind=engine, expire_on_commit=False)

class DatabaseSession:
    """
    Database session manager class for handling SQLAlchemy session lifecycle.
    
    Requirement: 1.1 System Overview/Data Access Layer - Database session management
    """
    
    def __init__(self) -> None:
        """
        Initialize database session manager.
        
        Creates a new Session instance and stores it in the _session property.
        """
        self._session: Session = Session()
    
    def get_session(self) -> Session:
        """
        Get current database session.
        
        Returns:
            Session: SQLAlchemy session instance
        """
        return self._session
    
    def close(self) -> None:
        """
        Close current database session.
        
        Closes the current session if it exists and sets _session to None.
        """
        if self._session:
            try:
                self._session.close()
            except SQLAlchemyError as e:
                logger.error(f"Error closing database session: {str(e)}")
            finally:
                self._session = None

@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Context manager for handling database session lifecycle and transactions.
    
    Requirement: 1.2 Scope/4. Data Management - Transaction management
    Requirement: 10.2.3 Database Security - Secure session management
    
    Yields:
        Session: Database session for transaction execution
        
    Raises:
        DatabaseError: If any database operation fails
    """
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database transaction error: {str(e)}")
        raise DatabaseError()
    finally:
        session.close()

def init_db() -> None:
    """
    Initialize database connection and create all tables.
    
    Requirement: 1.1 System Overview/Data Access Layer - Database initialization
    """
    try:
        # Import all models to ensure they are registered with SQLAlchemy
        from ..models import base  # noqa: F401
        from ..models import user  # noqa: F401
        from ..models import project  # noqa: F401
        from ..models import specification  # noqa: F401
        from ..models import bullet_item  # noqa: F401
        
        # Create all tables
        base.Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise DatabaseError()