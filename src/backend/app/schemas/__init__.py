"""
Initializes the schemas package and exports all schema classes for request/response validation and serialization.

Human Tasks:
1. Review schema imports with API documentation team for consistency
2. Verify error message strings with product team for user-friendliness
3. Confirm validation rules with security team
"""

# External imports - versions specified as per requirements
from marshmallow import Schema, fields  # version: 3.0+
from typing import List, Dict, Any  # version: 3.9+

# Authentication schemas
from .auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    TokenRefreshSchema,
    UserSchema as AuthUserSchema
)

# User schemas
from .user import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema
)

# Project schemas
from .project import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema
)

# Specification schemas
from .specification import (
    SpecificationSchema,
    SpecificationCreateSchema,
    SpecificationUpdateSchema
)

# Bullet item schemas
from .bullet_item import (
    BulletItemSchema,
    BulletItemCreateSchema,
    BulletItemUpdateSchema
)

# Schema exports for authentication
auth_schemas = {
    'LoginRequestSchema': LoginRequestSchema,
    'LoginResponseSchema': LoginResponseSchema,
    'TokenRefreshSchema': TokenRefreshSchema,
    'UserSchema': AuthUserSchema
}

# Schema exports for user management
user_schemas = {
    'UserSchema': UserSchema,
    'UserCreateSchema': UserCreateSchema,
    'UserUpdateSchema': UserUpdateSchema
}

# Schema exports for project management
project_schemas = {
    'ProjectSchema': ProjectSchema,
    'ProjectCreateSchema': ProjectCreateSchema,
    'ProjectUpdateSchema': ProjectUpdateSchema
}

# Schema exports for specification management
specification_schemas = {
    'SpecificationSchema': SpecificationSchema,
    'SpecificationCreateSchema': SpecificationCreateSchema,
    'SpecificationUpdateSchema': SpecificationUpdateSchema
}

# Schema exports for bullet item management
bullet_item_schemas = {
    'BulletItemSchema': BulletItemSchema,
    'BulletItemCreateSchema': BulletItemCreateSchema,
    'BulletItemUpdateSchema': BulletItemUpdateSchema
}

# Export all schemas
__all__ = [
    # Authentication schemas
    'LoginRequestSchema',
    'LoginResponseSchema',
    'TokenRefreshSchema',
    'AuthUserSchema',
    
    # User schemas
    'UserSchema',
    'UserCreateSchema',
    'UserUpdateSchema',
    
    # Project schemas
    'ProjectSchema',
    'ProjectCreateSchema',
    'ProjectUpdateSchema',
    
    # Specification schemas
    'SpecificationSchema',
    'SpecificationCreateSchema',
    'SpecificationUpdateSchema',
    
    # Bullet item schemas
    'BulletItemSchema',
    'BulletItemCreateSchema',
    'BulletItemUpdateSchema',
    
    # Schema collections
    'auth_schemas',
    'user_schemas',
    'project_schemas',
    'specification_schemas',
    'bullet_item_schemas'
]