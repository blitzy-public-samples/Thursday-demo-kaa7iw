"""
Authentication API endpoints handling Google OAuth login, token refresh, and logout operations.

Human Tasks:
1. Configure Google OAuth client ID and secret in environment variables
2. Set up Redis connection parameters for session management
3. Review rate limiting settings with the team
4. Verify JWT token expiration settings
5. Ensure CORS configuration is properly set up
"""

# External imports
from flask import Blueprint, request, jsonify  # version: 2.0+
from marshmallow import ValidationError  # version: 3.0+
from typing import Tuple, Dict, Any  # version: 3.9+
from http import HTTPStatus

# Internal imports
from ...schemas.auth import LoginRequestSchema, LoginResponseSchema, TokenRefreshSchema
from ...services.auth_service import AuthenticationService, AuthenticationError
from ...cache.redis import RedisCache
from ...middleware.request_validator import validate_schema

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Initialize services
auth_service = AuthenticationService(RedisCache())

@auth_bp.route('/login', methods=['POST'])
@validate_schema(LoginRequestSchema)
def login() -> Tuple[Dict[str, Any], int]:
    """
    Handle Google OAuth login requests.
    
    Requirement: User Management - Secure authentication through Google Cloud User Store
    Requirement: Authentication Layer - Google Cloud User Store integration
    
    Returns:
        tuple: Response tuple with JWT tokens and HTTP status
        
    Raises:
        ValidationError: If request schema validation fails
        AuthenticationError: If Google token validation fails
    """
    try:
        # Get validated Google token from request
        google_token = request.get_json()['google_token']
        
        # Authenticate with Google and get tokens
        auth_result = auth_service.authenticate_google_token(google_token)
        
        # Serialize response
        response = LoginResponseSchema().dump({
            'access_token': auth_result['access_token'],
            'refresh_token': auth_result['refresh_token'],
            'expires_in': 3600,  # 1 hour
            'token_type': 'Bearer'
        })
        
        return response, HTTPStatus.OK
        
    except AuthenticationError as e:
        return {
            'error': 'Authentication failed',
            'code': str(e)
        }, HTTPStatus.UNAUTHORIZED
        
    except Exception as e:
        return {
            'error': 'Internal server error',
            'code': 'SYS001'
        }, HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.route('/refresh', methods=['POST'])
@validate_schema(TokenRefreshSchema)
def refresh_token() -> Tuple[Dict[str, Any], int]:
    """
    Handle JWT token refresh requests.
    
    Requirement: User Management - Session management with JWT tokens
    
    Returns:
        tuple: Response tuple with new access token and HTTP status
        
    Raises:
        ValidationError: If request schema validation fails
        AuthenticationError: If refresh token is invalid
    """
    try:
        # Get validated refresh token from request
        refresh_token = request.get_json()['refresh_token']
        
        # Generate new access token
        token_result = auth_service.refresh_token(refresh_token)
        
        return {
            'access_token': token_result['access_token'],
            'token_type': 'Bearer',
            'expires_in': 3600  # 1 hour
        }, HTTPStatus.OK
        
    except AuthenticationError as e:
        return {
            'error': 'Invalid refresh token',
            'code': str(e)
        }, HTTPStatus.UNAUTHORIZED
        
    except Exception as e:
        return {
            'error': 'Internal server error',
            'code': 'SYS001'
        }, HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.route('/logout', methods=['POST'])
@validate_schema(TokenRefreshSchema)
def logout() -> Tuple[Dict[str, str], int]:
    """
    Handle user logout requests.
    
    Requirement: User Management - Session management with JWT tokens
    
    Returns:
        tuple: Response tuple with success message and HTTP status
        
    Raises:
        ValidationError: If request schema validation fails
        AuthenticationError: If refresh token is invalid
    """
    try:
        # Get validated refresh token from request
        refresh_token = request.get_json()['refresh_token']
        
        # Invalidate refresh token
        auth_service.logout(refresh_token)
        
        return {
            'message': 'Successfully logged out'
        }, HTTPStatus.OK
        
    except AuthenticationError as e:
        return {
            'error': 'Invalid refresh token',
            'code': str(e)
        }, HTTPStatus.UNAUTHORIZED
        
    except Exception as e:
        return {
            'error': 'Internal server error',
            'code': 'SYS001'
        }, HTTPStatus.INTERNAL_SERVER_ERROR