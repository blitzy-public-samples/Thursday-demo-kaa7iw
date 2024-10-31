"""
Rate limiting middleware implementation that enforces request rate limits per IP address
using Redis as the backend store.

Human Tasks:
1. Verify Redis connection parameters with infrastructure team
2. Review rate limit values with the security team
3. Confirm rate limit key format with the infrastructure team
4. Validate rate limit error responses with the API documentation
"""

# External imports
from flask import request  # version: 2.0+
from functools import wraps  # version: 3.9+
from typing import Callable, Optional  # version: 3.9+

# Internal imports
from ..cache.redis import RedisCache
from ..cache.keys import make_rate_limit_key
from ..utils.exceptions import RateLimitError

# Global rate limit constants
RATE_LIMIT_REQUESTS = 100  # Maximum requests per window
RATE_LIMIT_WINDOW = 60    # Time window in seconds

class RateLimiter:
    """
    Rate limiting middleware class that enforces request limits.
    
    Requirement: 10.3.1 Request Security - Rate limiting implementation
    """
    
    def __init__(
        self,
        cache: RedisCache,
        max_requests: Optional[int] = None,
        window: Optional[int] = None
    ) -> None:
        """
        Initialize rate limiter with Redis cache and limits.
        
        Args:
            cache: Redis cache instance for storing rate limit counters
            max_requests: Optional maximum requests per window, defaults to RATE_LIMIT_REQUESTS
            window: Optional time window in seconds, defaults to RATE_LIMIT_WINDOW
        """
        self._cache = cache
        self._max_requests = max_requests or RATE_LIMIT_REQUESTS
        self._window = window or RATE_LIMIT_WINDOW

    def check_rate_limit(self, user_id: str, endpoint: str) -> bool:
        """
        Check if request is within rate limit.
        
        Requirement: 10.3.1 Request Security - Rate limit checking implementation
        
        Args:
            user_id: Identifier for the user (IP address)
            endpoint: API endpoint being accessed
            
        Returns:
            bool: True if within limit, False if exceeded
            
        Raises:
            DatabaseError: If Redis operation fails
        """
        # Generate rate limit key for user and endpoint
        key = make_rate_limit_key(user_id, endpoint)
        
        # Increment counter and get current value, setting TTL if new key
        current_count = self._cache.increment(key, ttl=self._window)
        
        # Return True if under limit, False if exceeded
        return current_count <= self._max_requests

def rate_limit(f: Callable) -> Callable:
    """
    Decorator that applies rate limiting to routes.
    
    Requirement: 10.3.1 Request Security - Rate limiting decorator for routes
    
    Args:
        f: Function to wrap with rate limiting
        
    Returns:
        Callable: Wrapped function with rate limiting
        
    Raises:
        RateLimitError: If rate limit is exceeded
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get user IP address from request
        user_ip = request.remote_addr
        
        # Get current endpoint
        endpoint = request.endpoint or request.path
        
        # Get rate limiter instance from app config
        rate_limiter = request.app.config['RATE_LIMITER']
        
        # Check rate limit for IP and endpoint
        if not rate_limiter.check_rate_limit(user_ip, endpoint):
            raise RateLimitError()
            
        # Call original function if within limit
        return f(*args, **kwargs)
        
    return decorated_function