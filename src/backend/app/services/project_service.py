"""
Service layer implementation for project management operations providing high-level business logic
for project CRUD operations with caching support.

Human Tasks:
1. Verify Redis cache configuration in environment variables
2. Review project-related error codes in API documentation
3. Confirm database indexes are created for project queries
4. Validate project title constraints with product team
"""

# External imports - versions specified as per requirements
from typing import Dict, List, Optional  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ..models.project import Project
from ..schemas.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema
from ..database.operations import (
    create_record,
    get_record,
    update_record,
    delete_record,
    list_records
)
from .cache_service import CacheService
from ..utils.exceptions import (
    ResourceNotFoundError,
    AuthorizationError,
    ValidationError
)

class ProjectService:
    """
    Service class providing high-level project management operations with caching.
    
    Requirement: 1.2 Scope/2. Project Organization - Creation and management of projects
    with single-user ownership model and project-level access control
    """
    
    def __init__(self, cache_service: CacheService) -> None:
        """
        Initialize project service with cache service instance.
        
        Args:
            cache_service: Instance of CacheService for caching operations
        """
        self._cache = cache_service
        self._schema = ProjectSchema()
        self._create_schema = ProjectCreateSchema()
        self._update_schema = ProjectUpdateSchema()

    def create_project(self, user_id: UUID, project_data: Dict) -> Dict:
        """
        Create a new project for a user.
        
        Requirement: 1.2 Scope/2. Project Organization - Creation of projects with single-user ownership
        Requirement: 1.2 Scope/4. Data Management - CRUD operations with data validation
        
        Args:
            user_id: UUID of the user creating the project
            project_data: Dictionary containing project data
            
        Returns:
            Dict: Created project data
            
        Raises:
            ValidationError: If project data validation fails
            DatabaseError: If database operation fails
        """
        # Validate project data
        errors = self._create_schema.validate(project_data)
        if errors:
            raise ValidationError('PRJ001', errors)
        
        # Add user_id to project data
        project_data['user_id'] = user_id
        
        # Create project record
        project = create_record(Project, project_data)
        
        # Serialize project data
        project_dict = self._schema.dump(project)
        
        # Cache project data
        self._cache.set_project(str(project.id), project_dict)
        
        return project_dict

    def get_project(self, project_id: UUID, user_id: UUID) -> Dict:
        """
        Retrieve a project by ID with owner validation.
        
        Requirement: 1.2 Scope/2. Project Organization - Project-level access control
        Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
        
        Args:
            project_id: UUID of the project to retrieve
            user_id: UUID of the user requesting the project
            
        Returns:
            Dict: Project data
            
        Raises:
            ResourceNotFoundError: If project doesn't exist
            AuthorizationError: If user is not the project owner
            DatabaseError: If database operation fails
        """
        # Try to get from cache first
        cached_project = self._cache.get_project(str(project_id))
        if cached_project:
            # Validate ownership even for cached data
            if cached_project['user_id'] != str(user_id):
                raise AuthorizationError('PRJ002')
            return cached_project
        
        # Get from database if not in cache
        project = get_record(Project, project_id)
        if not project:
            raise ResourceNotFoundError('PRJ001')
        
        # Validate project ownership
        if not project.validate_ownership(user_id):
            raise AuthorizationError('PRJ002')
        
        # Serialize project data
        project_dict = self._schema.dump(project)
        
        # Cache project data
        self._cache.set_project(str(project_id), project_dict)
        
        return project_dict

    def update_project(self, project_id: UUID, user_id: UUID, project_data: Dict) -> Dict:
        """
        Update an existing project with owner validation.
        
        Requirement: 1.2 Scope/2. Project Organization - Project-level access control
        Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
        
        Args:
            project_id: UUID of the project to update
            user_id: UUID of the user requesting the update
            project_data: Dictionary containing updated project data
            
        Returns:
            Dict: Updated project data
            
        Raises:
            ResourceNotFoundError: If project doesn't exist
            AuthorizationError: If user is not the project owner
            ValidationError: If update data validation fails
            DatabaseError: If database operation fails
        """
        # Get project from database
        project = get_record(Project, project_id)
        if not project:
            raise ResourceNotFoundError('PRJ001')
        
        # Validate project ownership
        if not project.validate_ownership(user_id):
            raise AuthorizationError('PRJ002')
        
        # Validate update data
        errors = self._update_schema.validate(project_data)
        if errors:
            raise ValidationError('PRJ001', errors)
        
        # Update project record
        updated_project = update_record(project, project_data)
        
        # Serialize updated project data
        project_dict = self._schema.dump(updated_project)
        
        # Update cache
        self._cache.set_project(str(project_id), project_dict)
        
        return project_dict

    def delete_project(self, project_id: UUID, user_id: UUID) -> None:
        """
        Soft delete a project with owner validation.
        
        Requirement: 1.2 Scope/2. Project Organization - Project-level access control
        Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
        
        Args:
            project_id: UUID of the project to delete
            user_id: UUID of the user requesting deletion
            
        Raises:
            ResourceNotFoundError: If project doesn't exist
            AuthorizationError: If user is not the project owner
            DatabaseError: If database operation fails
        """
        # Get project from database
        project = get_record(Project, project_id)
        if not project:
            raise ResourceNotFoundError('PRJ001')
        
        # Validate project ownership
        if not project.validate_ownership(user_id):
            raise AuthorizationError('PRJ002')
        
        # Soft delete project record
        delete_record(project)
        
        # Remove from cache
        self._cache.set_project(str(project_id), None)

    def list_user_projects(self, user_id: UUID) -> List[Dict]:
        """
        List all active projects for a user.
        
        Requirement: 1.2 Scope/2. Project Organization - Project listing for single-user ownership
        Requirement: 1.2 Scope/4. Data Management - Data retrieval with filtering
        
        Args:
            user_id: UUID of the user whose projects to list
            
        Returns:
            List[Dict]: List of project data dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        # Query database for user's projects with filter
        projects = list_records(Project, {'user_id': user_id})
        
        # Serialize project list
        return self._schema.dump(projects, many=True)