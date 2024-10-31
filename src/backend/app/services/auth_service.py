"""
Authentication service implementing Google Cloud User Store integration, JWT token management,
and user session handling.

Human Tasks:
1. Set up Google Cloud User Store credentials and configuration
2. Configure Redis connection parameters in environment variables
3. Set up JWT secret key in environment variables
4. Review token expiration times with security team
5. Verify Redis cluster configuration for token blacklisting
"""

# External imports - versions specified as per requirements
from datetime import datetime  # version: 3.9+
from typing import Dict, Any, Optional  # version: 3.9+
from google.oauth2 import id_token  # version: 2.0+
from google.auth.transport import requests  # version: 2.0+

# Internal imports
from ..models.user import User
from ..database.session import session_scope
from ..utils.security import generate_jwt_token, validate_jwt_token
from ..cache.redis import RedisCache

class AuthenticationService:
    """
    Service class handling user authentication, token management, and session operations.
    
    Requirement: 1.2 Scope/1. User Management - Secure authentication through Google Cloud User Store
    Requirement: 1.1 System Overview/Authentication Layer - Google Cloud User Store integration
    Requirement: 10.1.3 Token Management - JWT-based session management
    """
    
    def __init__(self, cache: RedisCache) -> None:
        """
        Initialize authentication service with Redis cache.
        
        Args:
            cache: Redis cache instance for token management
        """
        self._cache = cache

    def authenticate_google_token(self, google_token: str) -> Dict[str, Any]:
        """
        Verify Google OAuth token and get or create user.
        
        Requirement: 1.1 System Overview/Authentication Layer - Google Cloud User Store integration
        Requirement: 1.2 Scope/1. User Management - Secure authentication
        
        Args:
            google_token: Google OAuth ID token
            
        Returns:
            Dict containing JWT tokens and user information
            
        Raises:
            AuthenticationError: If token validation fails
        """
        try:
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                google_token,
                requests.Request()
            )

            # Extract user information
            email = idinfo['email']
            name = idinfo.get('name', email.split('@')[0])

            # Get or create user in database
            with session_scope() as session:
                user = session.query(User).filter(
                    User.email == email,
                    User.is_deleted.is_(False)
                ).first()

                if not user:
                    user = User(email=email, name=name)
                    session.add(user)

                # Update last login
                user.update_last_login()
                session.commit()

                # Generate tokens
                user_data = user.to_dict()
                access_payload = {
                    'user_id': user_data['id'],
                    'email': user_data['email'],
                    'type': 'access'
                }
                refresh_payload = {
                    'user_id': user_data['id'],
                    'type': 'refresh'
                }

                access_token = generate_jwt_token(access_payload)
                refresh_token = generate_jwt_token(refresh_payload, is_refresh_token=True)

                # Cache refresh token
                self._cache.set(
                    f"refresh_token:{refresh_token}",
                    {'user_id': user_data['id']},
                    ttl=86400  # 24 hours
                )

                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user_data
                }

        except Exception as e:
            raise AuthenticationError('AUTH003') from e

    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Generate new access token using refresh token.
        
        Requirement: 10.1.3 Token Management - JWT token refresh functionality
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dict containing new access token
            
        Raises:
            AuthenticationError: If refresh token is invalid or blacklisted
        """
        try:
            # Validate refresh token
            payload = validate_jwt_token(refresh_token)
            if payload['type'] != 'refresh':
                raise AuthenticationError('AUTH001')

            # Check if token is blacklisted
            if self._cache.get(f"blacklist:{refresh_token}"):
                raise AuthenticationError('AUTH001')

            # Get cached token data
            token_data = self._cache.get(f"refresh_token:{refresh_token}")
            if not token_data:
                raise AuthenticationError('AUTH001')

            # Generate new access token
            access_payload = {
                'user_id': token_data['user_id'],
                'type': 'access'
            }
            
            return {
                'access_token': generate_jwt_token(access_payload)
            }

        except Exception as e:
            raise AuthenticationError('AUTH001') from e

    def logout(self, refresh_token: str) -> bool:
        """
        Invalidate user's refresh token.
        
        Requirement: 1.2 Scope/1. User Management - Session management
        
        Args:
            refresh_token: Refresh token to invalidate
            
        Returns:
            bool: Success status
            
        Raises:
            AuthenticationError: If refresh token is invalid
        """
        try:
            # Validate refresh token
            payload = validate_jwt_token(refresh_token)
            if payload['type'] != 'refresh':
                raise AuthenticationError('AUTH001')

            # Add token to blacklist
            expiration = int(payload['exp'] - datetime.utcnow().timestamp())
            self._cache.set(
                f"blacklist:{refresh_token}",
                {'invalidated_at': datetime.utcnow().isoformat()},
                ttl=expiration
            )

            # Remove from active refresh tokens
            self._cache.delete(f"refresh_token:{refresh_token}")

            return True

        except Exception as e:
            raise AuthenticationError('AUTH001') from e

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate access token and return payload.
        
        Requirement: 10.1.3 Token Management - JWT token validation
        
        Args:
            token: JWT access token
            
        Returns:
            Dict containing decoded token payload
            
        Raises:
            AuthenticationError: If token is invalid
        """
        try:
            # Validate JWT token
            payload = validate_jwt_token(token)
            
            # Verify token type
            if payload['type'] != 'access':
                raise AuthenticationError('AUTH001')
                
            return payload

        except Exception as e:
            raise AuthenticationError('AUTH001') from e