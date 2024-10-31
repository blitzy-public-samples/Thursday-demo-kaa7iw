"""
Authentication middleware for handling JWT token validation, user authentication, and authorization.

Human Tasks:
1. Configure JWT_SECRET_KEY in environment variables
2. Set up Google Cloud User Store credentials
3. Review and adjust token expiration times
4. Configure security headers in constants.py
5. Set up Redis connection for token management
"""

# External imports - versions specified as per requirements
from functools import wraps  # version: 3.9+
from typing import Callable, Dict, Any  # version: 3.9+
from flask import request, g, current_app  # version: 2.0+

# Internal imports
from ..services.auth_service import AuthenticationService
from ..utils.security import validate_jwt_token
from ..utils.exceptions import AuthenticationError

def require_auth(f: Callable) -> Callable:
    """
    Decorator function to enforce authentication on protected routes.
    
    Requirement: 1.2 Scope/1. User Management - Secure authentication through Google Cloud User Store
    Requirement: 10.1.1 Authentication Flow - Implementation of secure authentication flow
    
    Args:
        f: The route function to be wrapped
        
    Returns:
        Callable: Wrapped function that includes authentication check
        
    Raises:
        AuthenticationError: If authentication fails
    """
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError('AUTH001')
            
        try:
            # Check header format
            parts = auth_header.split()
            if parts[0].lower() != 'bearer' or len(parts) != 2:
                raise AuthenticationError('AUTH001')
                
            token = parts[1]
            
            # Validate JWT token
            payload = validate_jwt_token(token)
            
            # Verify token type
            if payload.get('type') != 'access':
                raise AuthenticationError('AUTH001')
            
            # Get user details from authentication service
            auth_service: AuthenticationService = current_app.auth_service
            user_data = auth_service.validate_token(token)
            
            # Attach user to request context
            g.user = user_data
            
            # Execute the protected route function
            return f(*args, **kwargs)
            
        except AuthenticationError:
            raise
        except Exception as e:
            current_app.logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationError('AUTH001')
            
    return decorated

def get_current_user() -> Dict[str, Any]:
    """
    Helper function to get current authenticated user from request context.
    
    Requirement: 1.2 Scope/1. User Management - Session management with JWT tokens
    
    Returns:
        Dict[str, Any]: Current authenticated user object
        
    Raises:
        AuthenticationError: If no authenticated user found in context
    """
    try:
        if not hasattr(g, 'user'):
            raise AuthenticationError('AUTH001')
        return g.user
    except Exception as e:
        current_app.logger.error(f"Failed to get current user: {str(e)}")
        raise AuthenticationError('AUTH001')