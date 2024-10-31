"""
Database package initialization module that exports core database functionality.

Human Tasks:
1. Verify DATABASE_URL environment variable is set with correct PostgreSQL connection string
2. Ensure database user has appropriate permissions for table creation and CRUD operations
3. Confirm PostgreSQL server configuration matches connection pool settings
4. Review database timeout and connection pool settings with operations team
5. Verify database backup and recovery procedures are in place
"""

# Internal imports
from .session import (
    DatabaseSession,
    session_scope,
    init_db
)
from .operations import (
    create_record,
    get_record,
    update_record,
    delete_record,
    list_records
)

# Export core database functionality
# Requirement: 1.1 System Overview/Data Access Layer - Core database functionality exports
__all__ = [
    'DatabaseSession',
    'session_scope',
    'init_db',
    'create_record',
    'get_record',
    'update_record',
    'delete_record',
    'list_records'
]

# Initialize logging
import logging
logger = logging.getLogger(__name__)

# Log package initialization
# Requirement: 1.1 System Overview/Data Access Layer - System logging
logger.info("Database package initialized successfully")