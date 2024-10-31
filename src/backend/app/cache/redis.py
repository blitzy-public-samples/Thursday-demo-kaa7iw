"""
Redis cache implementation providing caching functionality for projects, specifications,
bullet items, sessions and rate limiting using Redis as the backend store.

Human Tasks:
1. Verify Redis connection parameters with infrastructure team
2. Confirm Redis cluster configuration if using clustering
3. Review cache TTL values with the team
4. Ensure Redis version compatibility (6.0+)
5. Validate memory limits and eviction policies
"""

# External imports
from redis import Redis  # version: 6.0+
from typing import Any, Optional  # version: 3.9+
import json  # version: 3.9+

# Internal imports
from .keys import make_key, DEFAULT_TTL
from ..utils.exceptions import DatabaseError

class RedisCache:
    """
    Redis cache implementation providing caching functionality with Redis backend.
    
    Requirement: Cache Management - Redis 6+ used as caching layer for session storage,
    query caching and rate limiting
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        password: Optional[str] = None,
        db: Optional[int] = 0,
        default_ttl: Optional[int] = None
    ) -> None:
        """
        Initialize Redis cache with connection parameters.
        
        Args:
            host: Redis server hostname
            port: Redis server port
            password: Optional Redis password
            db: Optional Redis database number
            default_ttl: Optional default TTL for cache entries
        
        Raises:
            DatabaseError: If Redis connection fails
        """
        try:
            self._client = Redis(
                host=host,
                port=port,
                password=password,
                db=db,
                decode_responses=True,
                socket_timeout=5.0,
                socket_connect_timeout=5.0,
                retry_on_timeout=True
            )
            # Test connection
            self._client.ping()
            
            # Set default TTL
            self._default_ttl = default_ttl or DEFAULT_TTL
            
        except Exception as e:
            raise DatabaseError() from e

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache by key.
        
        Requirement: Performance Optimization - Cache implementation for performance
        optimization using Redis
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Optional[Any]: Cached value if exists, None otherwise
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        try:
            value = self._client.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception as e:
            raise DatabaseError() from e

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store value in cache with key and optional TTL.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for
        session storage and query caching
        
        Args:
            key: Cache key to store
            value: Value to cache
            ttl: Optional TTL in seconds, defaults to instance default_ttl
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        try:
            serialized = json.dumps(value)
            return self._client.set(
                name=key,
                value=serialized,
                ex=ttl or self._default_ttl
            )
        except Exception as e:
            raise DatabaseError() from e

    def delete(self, key: str) -> bool:
        """
        Remove value from cache by key.
        
        Requirement: Cache Management - Cache entry removal functionality
        
        Args:
            key: Cache key to delete
            
        Returns:
            bool: True if key existed and was deleted, False otherwise
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        try:
            return bool(self._client.delete(key))
        except Exception as e:
            raise DatabaseError() from e

    def increment(self, key: str, ttl: Optional[int] = None) -> int:
        """
        Increment counter value for rate limiting.
        
        Requirement: Cache Management - Redis 6+ used as caching layer for rate limiting
        
        Args:
            key: Counter key to increment
            ttl: Optional TTL for counter
            
        Returns:
            int: New counter value
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        try:
            pipe = self._client.pipeline()
            pipe.incr(key)
            if ttl:
                pipe.expire(key, ttl)
            results = pipe.execute()
            return int(results[0])
        except Exception as e:
            raise DatabaseError() from e

    def clear(self) -> bool:
        """
        Clear all cache entries.
        
        Requirement: Cache Management - Cache clearing functionality
        
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        try:
            return self._client.flushdb()
        except Exception as e:
            raise DatabaseError() from e