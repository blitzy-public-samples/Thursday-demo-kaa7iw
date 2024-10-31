"""Package initialization file for Alembic database migration versions.

Human Tasks:
1. Verify that initial_schema.py migration file exists and is properly configured
2. Ensure database user has necessary permissions to run migrations
3. Confirm database connection settings are properly configured
4. Review migration history table configuration
"""

# External imports - version specified as per requirements
from alembic import op  # version: 1.7+

# Internal imports - importing upgrade and downgrade functions from initial schema
from .initial_schema import upgrade, downgrade

# Export the initial schema migration functions
__all__ = ['initial_schema']

# This file makes the initial_schema migration importable and maintains version ordering
# Requirement addressed: 1.2 Scope/4. Data Management - Database schema management and version control