"""
Service layer implementation for caching operations providing high-level caching functionality
for projects, specifications, and bullet items with Redis backend.

Human Tasks:
1. Verify Redis connection parameters with infrastructure team
2. Confirm Redis cluster configuration if using clustering
3. Review cache TTL values with the team
4. Ensure Redis version compatibility (6.0+)
5. Validate memory limits and eviction policies
"""

# External imports - version requirements
from typing import Dict, Optional, Union  # version: 3.9+
import json  # version: 3.9+

# Internal imports
from ..cache.redis import RedisCache
from ..cache.keys import (
    make_project_key,
    make_spec_key,
    make_bullet_key,
    make_rate_limit_key,
    make_session_key
)
from ..utils.exceptions import DatabaseError

class CacheService:
    """
    Service class providing high-level caching operations for application entities.
    
    Requirement: Cache Management - Redis 6+ used as caching layer for session storage,
    query caching and rate limiting
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        password: Optional[str] = None,
        db: Optional[int] = None
    ) -> None:
        """
        Initialize cache service with Redis connection parameters.
        
        Args:
            host: Redis server hostname
            port: Redis server port
            password: Optional Redis password
            db: Optional Redis database number
            
        Raises:
            DatabaseError: If Redis connection fails
        """
        try:
            self._cache = RedisCache(
                host=host,
                port=port,
                password=password,
                db=db
            )
        except Exception as e:
            raise DatabaseError() from e

    def get_project(self, project_id: Union[str, int]) -> Optional[Dict]:
        """
        Retrieve project data from cache.
        
        Requirement: Performance Optimization - Cache implementation for performance
        optimization using Redis
        
        Args:
            project_id: Unique identifier of the project
            
        Returns:
            Optional[Dict]: Project data if exists in cache, None otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_project_key(project_id)
        return self._cache.get(key)

    def set_project(
        self,
        project_id: Union[str, int],
        project_data: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store project data in cache.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for query caching
        
        Args:
            project_id: Unique identifier of the project
            project_data: Project data to cache
            ttl: Optional TTL in seconds
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_project_key(project_id)
        return self._cache.set(key, project_data, ttl)

    def get_specification(self, spec_id: Union[str, int]) -> Optional[Dict]:
        """
        Retrieve specification data from cache.
        
        Requirement: Performance Optimization - Cache implementation for performance
        optimization using Redis
        
        Args:
            spec_id: Unique identifier of the specification
            
        Returns:
            Optional[Dict]: Specification data if exists in cache, None otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_spec_key(spec_id)
        return self._cache.get(key)

    def set_specification(
        self,
        spec_id: Union[str, int],
        spec_data: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store specification data in cache.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for query caching
        
        Args:
            spec_id: Unique identifier of the specification
            spec_data: Specification data to cache
            ttl: Optional TTL in seconds
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_spec_key(spec_id)
        return self._cache.set(key, spec_data, ttl)

    def get_bullet_item(self, bullet_id: Union[str, int]) -> Optional[Dict]:
        """
        Retrieve bullet item data from cache.
        
        Requirement: Performance Optimization - Cache implementation for performance
        optimization using Redis
        
        Args:
            bullet_id: Unique identifier of the bullet item
            
        Returns:
            Optional[Dict]: Bullet item data if exists in cache, None otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_bullet_key(bullet_id)
        return self._cache.get(key)

    def set_bullet_item(
        self,
        bullet_id: Union[str, int],
        bullet_data: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store bullet item data in cache.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for query caching
        
        Args:
            bullet_id: Unique identifier of the bullet item
            bullet_data: Bullet item data to cache
            ttl: Optional TTL in seconds
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_bullet_key(bullet_id)
        return self._cache.set(key, bullet_data, ttl)

    def check_rate_limit(
        self,
        user_id: str,
        endpoint: str,
        limit: int,
        window: int
    ) -> bool:
        """
        Check and update rate limit counter for user and endpoint.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for rate limiting
        
        Args:
            user_id: Identifier of the user being rate limited
            endpoint: API endpoint being accessed
            limit: Maximum number of requests allowed
            window: Time window in seconds
            
        Returns:
            bool: True if under limit, False if limit exceeded
            
        Raises:
            DatabaseError: If cache operation fails
        """
        key = make_rate_limit_key(user_id, endpoint)
        try:
            counter = self._cache.increment(key, ttl=window)
            return counter <= limit
        except Exception as e:
            raise DatabaseError() from e

    def clear_cache(self) -> bool:
        """
        Clear all cache entries.
        
        Requirement: Cache Management - Cache clearing functionality
        
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If cache operation fails
        """
        try:
            return self._cache.clear()
        except Exception as e:
            raise DatabaseError() from e