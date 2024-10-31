"""
Core security utility functions for handling JWT token management, encryption, security headers, 
and authentication/authorization helpers.

Human Tasks:
1. Set up and securely store the JWT_SECRET_KEY in the environment variables
2. Configure the AES_KEY in the environment variables for data encryption
3. Review and approve the security headers configuration
4. Ensure proper SSL/TLS configuration on the application server
5. Verify that the token expiration times align with security requirements
"""

# External imports
import jwt  # version: 2.4.0
from cryptography.fernet import Fernet  # version: 37.0.0
from cryptography.hazmat.primitives import hashes  # version: 37.0.0
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # version: 37.0.0
from cryptography.hazmat.primitives import padding  # version: 37.0.0
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # version: 37.0.0
import base64
from datetime import datetime, timedelta
from typing import Dict, Any  # version: 3.9+
import os

# Internal imports
from ..utils.constants import (
    SECURITY_HEADERS,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES
)
from ..utils.exceptions import AuthenticationError

def generate_jwt_token(payload: Dict[str, Any], is_refresh_token: bool = False) -> str:
    """
    Generate a new JWT token for authenticated users.
    
    Requirement: 10.1.3 Token Management - JWT token generation with proper expiration
    
    Args:
        payload (Dict[str, Any]): The payload to encode in the token
        is_refresh_token (bool): Whether to generate a refresh token with longer expiration
    
    Returns:
        str: The encoded JWT token
    
    Raises:
        AuthenticationError: If token generation fails
    """
    try:
        # Add issued at timestamp
        payload['iat'] = datetime.utcnow()
        
        # Calculate expiration based on token type
        expiration = JWT_REFRESH_TOKEN_EXPIRES if is_refresh_token else JWT_ACCESS_TOKEN_EXPIRES
        payload['exp'] = datetime.utcnow() + timedelta(seconds=expiration)
        
        # Encode and sign token
        return jwt.encode(
            payload,
            os.environ['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        raise AuthenticationError('AUTH001')

def validate_jwt_token(token: str) -> Dict[str, Any]:
    """
    Validate and decode a JWT token.
    
    Requirement: 10.1.3 Token Management - JWT token validation and verification
    
    Args:
        token (str): The JWT token to validate
    
    Returns:
        Dict[str, Any]: The decoded token payload
    
    Raises:
        AuthenticationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            os.environ['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        
        # Verify expiration
        if datetime.fromtimestamp(payload['exp']) < datetime.utcnow():
            raise AuthenticationError('AUTH002')
            
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('AUTH002')
    except jwt.InvalidTokenError:
        raise AuthenticationError('AUTH001')

def encrypt_sensitive_data(data: str) -> str:
    """
    Encrypt sensitive data using AES-256.
    
    Requirement: 10.2.2 Encryption Standards - AES-256 encryption implementation
    
    Args:
        data (str): The data to encrypt
    
    Returns:
        str: Base64 encoded encrypted data
    """
    try:
        # Generate a random 16-byte IV
        iv = os.urandom(16)
        
        # Create cipher with AES-256
        cipher = Cipher(
            algorithms.AES(base64.b64decode(os.environ['AES_KEY'])),
            modes.CBC(iv)
        )
        encryptor = cipher.encryptor()
        
        # Add padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        
        # Encrypt data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and encrypted data and encode as base64
        return base64.b64encode(iv + encrypted_data).decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Encryption failed: {str(e)}")

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    Decrypt AES-256 encrypted data.
    
    Requirement: 10.2.2 Encryption Standards - AES-256 decryption implementation
    
    Args:
        encrypted_data (str): Base64 encoded encrypted data
    
    Returns:
        str: Decrypted data string
    """
    try:
        # Decode base64 data
        raw_data = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Extract IV (first 16 bytes) and encrypted data
        iv = raw_data[:16]
        encrypted_content = raw_data[16:]
        
        # Create cipher for decryption
        cipher = Cipher(
            algorithms.AES(base64.b64decode(os.environ['AES_KEY'])),
            modes.CBC(iv)
        )
        decryptor = cipher.decryptor()
        
        # Decrypt data
        padded_data = decryptor.update(encrypted_content) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {str(e)}")

def get_security_headers() -> Dict[str, str]:
    """
    Get security headers for HTTP responses.
    
    Requirement: 10.3.2 Security Headers - Security header management
    
    Returns:
        Dict[str, str]: Dictionary of security headers
    """
    return SECURITY_HEADERS