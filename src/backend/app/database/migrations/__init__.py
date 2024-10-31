"""
Database migrations package initialization.

Human Tasks:
1. Verify PostgreSQL connection string format in environment variables
2. Ensure database user has sufficient privileges for migrations
3. Review logging configuration for migration operations
4. Confirm database backup before running migrations
"""

# External imports - versions specified for production use
from alembic import context  # version: 1.7+

# Internal imports
from .env import run_migrations_offline, run_migrations_online

# Global constants for migration configuration
MIGRATION_SCRIPT_TEMPLATE = 'script.py.mako'
MIGRATION_ENV_CONFIG = 'env.py'

# Export migration functions for external use
__all__ = ['run_migrations_offline', 'run_migrations_online']

def get_migration_context():
    """
    Get the current Alembic migration context.
    
    Returns:
        context: Alembic migration context
        
    Requirement: 1.2 Scope/4. Data Management - Database schema management and migrations
    """
    return context.get_context()

def is_offline_mode() -> bool:
    """
    Check if migrations are running in offline mode.
    
    Returns:
        bool: True if offline mode, False otherwise
        
    Requirement: 1.2 Scope/4. Data Management - Database schema management and migrations
    """
    return context.is_offline_mode()

def get_current_revision():
    """
    Get the current database migration revision.
    
    Returns:
        str: Current revision identifier
        
    Requirement: 1.2 Scope/4. Data Management - Database schema management and migrations
    """
    migration_context = get_migration_context()
    return migration_context.get_current_revision()