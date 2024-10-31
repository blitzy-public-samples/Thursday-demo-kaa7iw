"""
Alembic migration environment configuration file.

Human Tasks:
1. Verify PostgreSQL connection string format in environment variables
2. Ensure database user has sufficient privileges for migrations
3. Review logging configuration for migration operations
4. Confirm database backup before running migrations
"""

# External imports - versions specified for production use
from logging.config import fileConfig  # version: 3.9+
from sqlalchemy import engine_from_config  # version: 1.4+
from sqlalchemy import pool  # version: 1.4+
from alembic import context  # version: 1.7+
import logging  # version: 3.9+

# Internal imports
from app.models.base import Base
from config import load_config

# Initialize logging
logger = logging.getLogger('alembic.env')

# Load application configuration
config = load_config()

# Get database metadata from SQLAlchemy models
target_metadata = Base.metadata

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_engine_url() -> str:
    """
    Get database URL from configuration.
    
    Returns:
        str: Database connection URL
        
    Requirement: 1.1 System Overview/Data Access Layer - PostgreSQL database interactions
    """
    return config.DATABASE_URL

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode for generating SQL scripts.
    
    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine
    creation we don't even need a DBAPI to be available.
    
    Requirement: 1.2 Scope/4. Data Management - Database schema management and migrations
    """
    url = get_engine_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        try:
            context.run_migrations()
            logger.info("Offline migrations completed successfully")
        except Exception as e:
            logger.error(f"Error during offline migrations: {str(e)}")
            raise

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode for direct database changes.
    
    In this scenario we need to create an Engine and associate a
    connection with the context.
    
    Requirement: 1.2 Scope/4. Data Management - Database schema management and migrations
    """
    # Configure SQLAlchemy engine
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_engine_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            try:
                context.run_migrations()
                logger.info("Online migrations completed successfully")
            except Exception as e:
                logger.error(f"Error during online migrations: {str(e)}")
                raise

if context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()