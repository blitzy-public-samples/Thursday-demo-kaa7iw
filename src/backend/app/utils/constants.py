"""
System-wide constants for the Code Generation Web Application.

Human Tasks:
1. Verify that the JWT token expiration times align with the authentication service configuration
2. Ensure security headers comply with the organization's security policies
3. Confirm rate limiting values are appropriate for the production environment
4. Validate database timeout value with the database administrator
5. Review cache TTL settings with the infrastructure team
"""

# External imports
from typing import Dict  # version: 3.9+

# Error codes and messages
# Requirement: A.4 Error Codes and Messages - Definition of standardized error codes
ERROR_CODES: Dict[str, str] = {
    # Authentication errors
    'AUTH001': 'Invalid token',
    'AUTH002': 'Token expired',
    'AUTH003': 'Invalid Google token',
    
    # Project-related errors
    'PRJ001': 'Project not found',
    'PRJ002': 'Unauthorized access',
    
    # Specification-related errors
    'SPEC001': 'Specification not found',
    'SPEC002': 'Invalid project reference',
    
    # Bullet item errors
    'ITEM001': 'Maximum items reached',
    'ITEM002': 'Invalid order value',
    
    # System errors
    'SYS001': 'Database error',
    'SYS002': 'Rate limit exceeded'
}

# Security header configurations
# Requirement: 10.3.2 Security Headers - Security header configurations for HTTP responses
SECURITY_HEADERS: Dict[str, str] = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}

# JWT token expiration times (in seconds)
# Requirement: 10.1.3 Token Management - JWT token expiration durations
JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hour
JWT_REFRESH_TOKEN_EXPIRES: int = 86400  # 24 hours

# Bullet item constraints
# Requirement: 1.2 Scope/3. Specification Management - Maximum limit of bullet items
MAX_BULLET_ITEMS: int = 10

# Database configuration
DATABASE_TIMEOUT: int = 30  # Database operation timeout in seconds

# Rate limiting configuration
RATE_LIMIT_REQUESTS: int = 100  # Maximum requests per period
RATE_LIMIT_PERIOD: int = 60  # Time period in seconds (1 minute)

# Cache configuration
CACHE_TTL: int = 300  # Cache time-to-live in seconds (5 minutes)