"""
Health check implementation for monitoring system components including database, cache,
and overall application health status.

Human Tasks:
1. Verify database connection settings in environment variables
2. Confirm Redis connection parameters in configuration
3. Review health check thresholds with operations team
4. Set up monitoring alerts based on health check results
"""

# External imports
from enum import Enum  # version: 3.9+
from dataclasses import dataclass  # version: 3.9+
from typing import Dict, Any  # version: 3.9+

# Internal imports
from ..database.session import session_scope
from ..cache.redis import RedisClient

# Requirement: 7.1 High-Level Architecture/Core Components - Health monitoring status types
class HealthStatus(Enum):
    """Enumeration of possible health check statuses."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"

class HealthCheck:
    """
    Health check manager for system components.
    
    Requirement: 7.1 High-Level Architecture/Core Components - Health monitoring for core system components
    """
    
    def __init__(self, redis_client: RedisClient) -> None:
        """
        Initialize health check manager.
        
        Args:
            redis_client: Redis client instance for cache health checks
        """
        self._redis_client = redis_client

    def check_database(self) -> HealthStatus:
        """
        Check database connection health.
        
        Requirement: 7.1 High-Level Architecture/Core Components - Database health monitoring
        
        Returns:
            HealthStatus: Database connection status
        """
        try:
            # Attempt to create database session and execute simple query
            with session_scope() as session:
                # Simple query to test database connection
                session.execute("SELECT 1")
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def check_redis(self) -> HealthStatus:
        """
        Check Redis cache connection health.
        
        Requirement: 7.1 High-Level Architecture/Core Components - Cache health monitoring
        
        Returns:
            HealthStatus: Redis connection status
        """
        try:
            # Attempt to ping Redis server
            self._redis_client.ping()
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def check_all(self) -> Dict[str, HealthStatus]:
        """
        Check health of all system components.
        
        Requirement: 7.1 High-Level Architecture/Core Components - Comprehensive system health monitoring
        
        Returns:
            Dict[str, HealthStatus]: Health status of all components
        """
        return {
            "database": self.check_database(),
            "cache": self.check_redis()
        }

def get_system_health(health_checker: HealthCheck) -> Dict[str, Any]:
    """
    Get overall system health status.
    
    Requirement: 11.5.2 Pipeline Stages - Health checks for deployment validation
    
    Args:
        health_checker: HealthCheck instance to perform health checks
        
    Returns:
        Dict[str, Any]: System health status and details containing:
            - overall_status: HealthStatus
            - components: Dict of component statuses
            - timestamp: ISO 8601 timestamp
    """
    from datetime import datetime, timezone
    
    # Get status of all components
    component_status = health_checker.check_all()
    
    # Determine overall system health
    if all(status == HealthStatus.HEALTHY for status in component_status.values()):
        overall_status = HealthStatus.HEALTHY
    elif all(status == HealthStatus.UNHEALTHY for status in component_status.values()):
        overall_status = HealthStatus.UNHEALTHY
    else:
        overall_status = HealthStatus.DEGRADED
    
    return {
        "overall_status": overall_status,
        "components": {
            component: status.value
            for component, status in component_status.items()
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }