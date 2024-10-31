"""
Service layer initialization module that exports all service classes for the application.

Human Tasks:
1. Verify all service dependencies are properly configured
2. Review service initialization order with the team
3. Confirm cache service configuration parameters
4. Validate service access patterns with security team
"""

# External imports - versions specified as per requirements
from typing import Dict, Any  # version: 3.9+

# Internal imports - Service classes
from .auth_service import AuthenticationService
from .project_service import ProjectService
from .specification_service import SpecificationService
from .bullet_item_service import BulletItemService
from .cache_service import CacheService

# Define __all__ for explicit exports
# Requirement: Service Layer Architecture - Core functionality for project, specification, and bullet item management
__all__ = [
    "AuthenticationService",
    "ProjectService",
    "SpecificationService",
    "BulletItemService",
    "CacheService"
]

"""
Service Layer Architecture Implementation

This module implements the Service Layer pattern providing centralized access to all service components
as specified in the technical requirements:

Requirement: 1.1 System Overview/Business Logic Layer
- Core functionality for project, specification, and bullet item management

Requirement: 7.2 Component Architecture
- Service components providing business logic implementation

The services exposed here provide:
1. Authentication and session management (AuthenticationService)
2. Project management operations (ProjectService)
3. Specification management operations (SpecificationService)
4. Bullet item management operations (BulletItemService)
5. Caching operations (CacheService)

Each service is designed to be instantiated with its required dependencies and provides
a clean interface for business logic operations while handling:
- Data validation
- Business rules enforcement
- Cache management
- Error handling
- Transaction management
"""