"""
Flask application extensions initialization and management module.

Human Tasks:
1. Verify Redis connection parameters in environment variables
2. Confirm PostgreSQL connection string in environment variables
3. Review metrics collection configuration with SRE team
4. Ensure monitoring endpoints are properly secured
5. Validate cache TTL settings with the team
"""

# External imports
from typing import Optional  # version: 3.9+
from flask import Flask  # version: 2.0+

# Internal imports
from .cache.redis import RedisCache
from .database.session import DatabaseSession, init_db
from .monitoring.metrics import MetricsCollector, get_metrics_collector

# Global instances
# Requirement: Data Access Layer - PostgreSQL database interactions for persistent storage
db: DatabaseSession = DatabaseSession()

# Requirement: Cache Management - Redis 6+ used as caching layer
cache: Optional[RedisCache] = None

# Requirement: System Monitoring - Core monitoring system component
metrics: Optional[MetricsCollector] = None

def init_extensions(app: Flask) -> None:
    """
    Initialize all Flask application extensions including database, cache, and metrics collectors.
    
    Args:
        app: Flask application instance
        
    Requirement: Data Access Layer - Initialize database connection
    Requirement: Cache Management - Initialize Redis cache
    Requirement: System Monitoring - Initialize metrics collection
    """
    global cache, metrics
    
    try:
        # Initialize database
        init_db()
        app.logger.info("Database initialized successfully")
        
        # Initialize Redis cache
        cache = RedisCache(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config.get('REDIS_PASSWORD'),
            db=app.config.get('REDIS_DB', 0),
            default_ttl=app.config.get('REDIS_DEFAULT_TTL', 3600)
        )
        app.logger.info("Redis cache initialized successfully")
        
        # Initialize metrics collector
        metrics = get_metrics_collector()
        app.logger.info("Metrics collector initialized successfully")
        
        # Register extensions with application context
        app.extensions['db_session'] = db
        app.extensions['redis_cache'] = cache
        app.extensions['metrics'] = metrics
        
    except Exception as e:
        app.logger.error(f"Failed to initialize extensions: {str(e)}")
        raise

def get_db() -> DatabaseSession:
    """
    Get the global database session instance.
    
    Returns:
        DatabaseSession: Global database session instance
        
    Requirement: Data Access Layer - Database session access
    """
    return db

def get_cache() -> Optional[RedisCache]:
    """
    Get the global Redis cache instance.
    
    Returns:
        Optional[RedisCache]: Global Redis cache instance
        
    Requirement: Cache Management - Redis cache access
    """
    return cache

def get_metrics() -> Optional[MetricsCollector]:
    """
    Get the global metrics collector instance.
    
    Returns:
        Optional[MetricsCollector]: Global metrics collector instance
        
    Requirement: System Monitoring - Metrics collector access
    """
    return metrics