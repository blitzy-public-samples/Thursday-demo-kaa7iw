"""
REST API endpoints for project management operations including CRUD operations with authentication and validation.

Human Tasks:
1. Verify that error response formats match API documentation
2. Confirm rate limiting configuration for project endpoints
3. Review logging level configuration for project operations
4. Validate HTTP status codes with API documentation
"""

# External imports - versions specified as per requirements
from flask import Blueprint, request, jsonify  # version: 2.0+
from http import HTTPStatus  # version: 3.9+
from typing import Dict, Tuple  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ...services.project_service import ProjectService
from ...middleware.auth import require_auth, get_current_user
from ...schemas.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema
from ...utils.exceptions import (
    ResourceNotFoundError,
    AuthorizationError,
    ValidationError
)

# Create Blueprint for project routes
projects_blueprint = Blueprint('projects', __name__)

# Initialize schemas
project_schema = ProjectSchema()
project_create_schema = ProjectCreateSchema()
project_update_schema = ProjectUpdateSchema()

@projects_blueprint.route('/projects', methods=['POST'])
@require_auth
def create_project() -> Tuple[Dict, int]:
    """
    Create a new project for the authenticated user.
    
    Requirement: 1.2 Scope/2. Project Organization - Creation of projects with single-user ownership
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    
    Returns:
        Tuple[Dict, int]: Project data and HTTP 201 status code
        
    Raises:
        ValidationError: If project data validation fails
        AuthenticationError: If user is not authenticated
    """
    try:
        # Get current authenticated user
        current_user = get_current_user()
        
        # Extract and validate project data from request
        project_data = request.get_json()
        errors = project_create_schema.validate(project_data)
        if errors:
            raise ValidationError('PRJ001', errors)
        
        # Create project using service
        project_service: ProjectService = request.app.project_service
        created_project = project_service.create_project(
            user_id=UUID(current_user['id']),
            project_data=project_data
        )
        
        return jsonify(created_project), HTTPStatus.CREATED
        
    except ValidationError as e:
        raise
    except Exception as e:
        request.app.logger.error(f"Project creation failed: {str(e)}")
        raise

@projects_blueprint.route('/projects/<uuid:project_id>', methods=['GET'])
@require_auth
def get_project(project_id: UUID) -> Tuple[Dict, int]:
    """
    Retrieve a specific project by ID.
    
    Requirement: 1.2 Scope/2. Project Organization - Project-level access control
    Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
    
    Args:
        project_id: UUID of the project to retrieve
        
    Returns:
        Tuple[Dict, int]: Project data and HTTP 200 status code
        
    Raises:
        ResourceNotFoundError: If project doesn't exist
        AuthorizationError: If user is not the project owner
        AuthenticationError: If user is not authenticated
    """
    try:
        # Get current authenticated user
        current_user = get_current_user()
        
        # Retrieve project using service
        project_service: ProjectService = request.app.project_service
        project = project_service.get_project(
            project_id=project_id,
            user_id=UUID(current_user['id'])
        )
        
        return jsonify(project), HTTPStatus.OK
        
    except (ResourceNotFoundError, AuthorizationError) as e:
        raise
    except Exception as e:
        request.app.logger.error(f"Project retrieval failed: {str(e)}")
        raise

@projects_blueprint.route('/projects/<uuid:project_id>', methods=['PUT'])
@require_auth
def update_project(project_id: UUID) -> Tuple[Dict, int]:
    """
    Update an existing project.
    
    Requirement: 1.2 Scope/2. Project Organization - Project-level access control
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    
    Args:
        project_id: UUID of the project to update
        
    Returns:
        Tuple[Dict, int]: Updated project data and HTTP 200 status code
        
    Raises:
        ResourceNotFoundError: If project doesn't exist
        AuthorizationError: If user is not the project owner
        ValidationError: If update data validation fails
        AuthenticationError: If user is not authenticated
    """
    try:
        # Get current authenticated user
        current_user = get_current_user()
        
        # Extract and validate update data from request
        update_data = request.get_json()
        errors = project_update_schema.validate(update_data)
        if errors:
            raise ValidationError('PRJ001', errors)
        
        # Update project using service
        project_service: ProjectService = request.app.project_service
        updated_project = project_service.update_project(
            project_id=project_id,
            user_id=UUID(current_user['id']),
            project_data=update_data
        )
        
        return jsonify(updated_project), HTTPStatus.OK
        
    except (ResourceNotFoundError, AuthorizationError, ValidationError) as e:
        raise
    except Exception as e:
        request.app.logger.error(f"Project update failed: {str(e)}")
        raise

@projects_blueprint.route('/projects/<uuid:project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id: UUID) -> Tuple[Dict, int]:
    """
    Soft delete an existing project.
    
    Requirement: 1.2 Scope/2. Project Organization - Project-level access control
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    
    Args:
        project_id: UUID of the project to delete
        
    Returns:
        Tuple[Dict, int]: Success message and HTTP 204 status code
        
    Raises:
        ResourceNotFoundError: If project doesn't exist
        AuthorizationError: If user is not the project owner
        AuthenticationError: If user is not authenticated
    """
    try:
        # Get current authenticated user
        current_user = get_current_user()
        
        # Delete project using service
        project_service: ProjectService = request.app.project_service
        project_service.delete_project(
            project_id=project_id,
            user_id=UUID(current_user['id'])
        )
        
        return jsonify({'message': 'Project deleted successfully'}), HTTPStatus.NO_CONTENT
        
    except (ResourceNotFoundError, AuthorizationError) as e:
        raise
    except Exception as e:
        request.app.logger.error(f"Project deletion failed: {str(e)}")
        raise

@projects_blueprint.route('/projects', methods=['GET'])
@require_auth
def list_projects() -> Tuple[Dict, int]:
    """
    List all projects for the authenticated user.
    
    Requirement: 1.2 Scope/2. Project Organization - Project listing for single-user ownership
    Requirement: 1.2 Scope/4. Data Management - Data retrieval with filtering
    
    Returns:
        Tuple[Dict, int]: List of projects and HTTP 200 status code
        
    Raises:
        AuthenticationError: If user is not authenticated
    """
    try:
        # Get current authenticated user
        current_user = get_current_user()
        
        # List projects using service
        project_service: ProjectService = request.app.project_service
        projects = project_service.list_user_projects(
            user_id=UUID(current_user['id'])
        )
        
        return jsonify({'projects': projects}), HTTPStatus.OK
        
    except Exception as e:
        request.app.logger.error(f"Project listing failed: {str(e)}")
        raise