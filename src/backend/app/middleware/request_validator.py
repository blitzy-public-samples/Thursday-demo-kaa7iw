"""
Flask middleware for validating incoming HTTP requests against defined schemas and enforcing data validation rules.

Human Tasks:
1. Review schema validation error messages with the API documentation team
2. Verify schema registry initialization in Flask app setup
3. Confirm error response format with frontend team
"""

# External imports
from flask import Request  # version: 2.0+
from marshmallow import Schema, ValidationError as MarshmallowError  # version: 3.0+
from functools import wraps  # version: 3.9+
from typing import Dict, Callable, Any  # version: 3.9+

# Internal imports
from ..utils.exceptions import ValidationError
from ..utils.validators import (
    validate_project_title,
    validate_specification_content,
    validate_bullet_item
)

class RequestValidator:
    """
    Middleware class for validating incoming HTTP requests.
    
    Requirement: Data Validation - Request validation middleware
    """
    
    def __init__(self) -> None:
        """
        Initialize the request validator middleware.
        
        Requirement: Data Validation - Schema registry initialization
        """
        self._schema_registry: Dict[str, Schema] = {}

    def register_schema(self, endpoint: str, schema: Schema) -> None:
        """
        Register a schema for a specific endpoint.
        
        Requirement: Data Validation - Schema registration for endpoints
        
        Args:
            endpoint: The endpoint path to register schema for
            schema: The marshmallow schema to use for validation
        """
        self._schema_registry[endpoint] = schema

    def validate_request(self, request: Request, endpoint: str) -> Dict:
        """
        Validate incoming request data against registered schema.
        
        Requirement: Input Validation - Request data validation
        
        Args:
            request: The Flask request object
            endpoint: The endpoint path for schema lookup
            
        Returns:
            Dict: Validated request data
            
        Raises:
            ValidationError: If validation fails with error details
        """
        schema = self._schema_registry.get(endpoint)
        if not schema:
            raise ValidationError(
                code='SYS001',
                errors={'schema': [f'No schema registered for endpoint: {endpoint}']}
            )

        try:
            # Load JSON data from request
            json_data = request.get_json()
            if json_data is None:
                raise ValidationError(
                    code='SYS001',
                    errors={'json': ['Invalid JSON in request body']}
                )

            # Validate against schema
            validated_data = schema.load(json_data)

            # Perform additional validation based on data type
            if 'title' in validated_data:
                validate_project_title(validated_data['title'])
            if 'content' in validated_data:
                validate_specification_content(validated_data['content'])
            if 'order' in validated_data:
                validate_bullet_item(validated_data['content'], validated_data['order'])

            return validated_data

        except MarshmallowError as e:
            # Convert marshmallow validation errors to our format
            raise ValidationError(
                code='SYS001',
                errors=e.messages
            )

def validate_request_middleware(schema: Schema) -> Callable:
    """
    Decorator function to validate requests for specific endpoints.
    
    Requirement: Input Validation - Request validation decorator
    
    Args:
        schema: The marshmallow schema to validate against
        
    Returns:
        Callable: Decorated route function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get request validator instance from Flask app
            validator = RequestValidator()
            
            # Register schema for this endpoint
            endpoint = f.__name__
            validator.register_schema(endpoint, schema)
            
            # Validate request
            validated_data = validator.validate_request(request, endpoint)
            
            # Add validated data to kwargs
            kwargs['validated_data'] = validated_data
            
            return f(*args, **kwargs)
        return wrapper
    return decorator