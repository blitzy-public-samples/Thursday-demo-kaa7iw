"""
Cache package initializer that exposes Redis cache implementation and key management 
functions for the application's caching layer.

Human Tasks:
1. Verify Redis connection parameters in configuration
2. Ensure Redis 6+ is installed and accessible
3. Review cache TTL values in configuration
4. Validate Redis memory limits and eviction policies
"""

# Internal imports
from .redis import RedisCache
from .keys import (
    make_key,
    make_project_key,
    make_spec_key,
    make_bullet_key,
    make_rate_limit_key,
    make_session_key,
    DEFAULT_TTL
)

# Expose all required components for application-wide caching needs
__all__ = [
    'RedisCache',          # Redis cache implementation
    'make_key',           # Generic cache key generator
    'make_project_key',   # Project cache key generator
    'make_spec_key',      # Specification cache key generator
    'make_bullet_key',    # Bullet item cache key generator
    'make_rate_limit_key', # Rate limit cache key generator
    'make_session_key',   # Session cache key generator
    'DEFAULT_TTL'         # Default cache TTL value
]

# This package implements the following requirements:
# 1. Cache Management - Redis 6+ used as caching layer for session storage, 
#    query caching and rate limiting
# 2. Performance Optimization - Cache implementation for performance optimization 
#    using Redis