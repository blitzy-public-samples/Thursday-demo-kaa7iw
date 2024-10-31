"""
Cache key generation module for Redis cache operations.

This module provides functions to generate standardized cache keys for various
entities in the system including projects, specifications, bullet items,
rate limiting, and sessions.

Human Tasks:
1. Verify Redis key prefix conventions with the infrastructure team
2. Confirm cache key separator aligns with existing Redis key patterns
3. Review rate limit key format with the security team
4. Validate session key format with the authentication service requirements
"""

# External imports
from typing import Union, List  # version: 3.9+

# Internal imports
from ..utils.constants import CACHE_TTL

# Default cache TTL from constants
DEFAULT_TTL = CACHE_TTL

# Cache key constants
KEY_SEPARATOR = ':'
PROJECT_PREFIX = 'project'
SPEC_PREFIX = 'spec'
BULLET_PREFIX = 'bullet'
RATE_LIMIT_PREFIX = 'rate'
SESSION_PREFIX = 'session'

def make_key(prefix: str, components: Union[str, int, List[Union[str, int]]]) -> str:
    """
    Generate a Redis cache key with prefix and components.
    
    Requirement: Cache Management - Redis 6+ used as caching layer for session storage,
    query caching and rate limiting
    
    Args:
        prefix: The prefix for the cache key
        components: Single value or list of values to form the key
    
    Returns:
        str: Generated cache key with components joined by separator
    """
    # Convert single component to list for uniform handling
    if not isinstance(components, list):
        components = [components]
    
    # Convert all components to strings
    str_components = [str(component) for component in components]
    
    # Join prefix and components with separator
    return KEY_SEPARATOR.join([prefix] + str_components)

def make_project_key(project_id: Union[str, int]) -> str:
    """
    Generate cache key for project data.
    
    Requirement: Performance Optimization - Cache key generation for performance
    optimization using Redis
    
    Args:
        project_id: Unique identifier of the project
    
    Returns:
        str: Cache key for project
    """
    return make_key(PROJECT_PREFIX, project_id)

def make_spec_key(spec_id: Union[str, int]) -> str:
    """
    Generate cache key for specification data.
    
    Requirement: Performance Optimization - Cache key generation for performance
    optimization using Redis
    
    Args:
        spec_id: Unique identifier of the specification
    
    Returns:
        str: Cache key for specification
    """
    return make_key(SPEC_PREFIX, spec_id)

def make_bullet_key(bullet_id: Union[str, int]) -> str:
    """
    Generate cache key for bullet item data.
    
    Requirement: Performance Optimization - Cache key generation for performance
    optimization using Redis
    
    Args:
        bullet_id: Unique identifier of the bullet item
    
    Returns:
        str: Cache key for bullet item
    """
    return make_key(BULLET_PREFIX, bullet_id)

def make_rate_limit_key(user_id: str, endpoint: str) -> str:
    """
    Generate cache key for rate limiting.
    
    Requirement: Cache Management - Redis 6+ used as caching layer for rate limiting
    
    Args:
        user_id: Identifier of the user being rate limited
        endpoint: API endpoint being accessed
    
    Returns:
        str: Cache key for rate limit counter
    """
    return make_key(RATE_LIMIT_PREFIX, [user_id, endpoint])

def make_session_key(session_id: str) -> str:
    """
    Generate cache key for user session data.
    
    Requirement: Cache Management - Redis 6+ used as caching layer for session storage
    
    Args:
        session_id: Unique identifier of the user session
    
    Returns:
        str: Cache key for session data
    """
    return make_key(SESSION_PREFIX, session_id)