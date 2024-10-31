"""
RESTful API endpoints for managing specifications within projects.

Human Tasks:
1. Configure rate limiting values in environment variables
2. Review error messages with product team
3. Set up monitoring for endpoint performance
4. Configure caching TTL values
"""

# External imports - versions specified as per requirements
from flask import Blueprint, request, jsonify  # version: 2.0+
from typing import Dict, Tuple, Any  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ...middleware.auth import require_auth
from ...services.specification_service import SpecificationService
from ...schemas.specification import (
    SpecificationSchema,
    SpecificationCreateSchema,
    SpecificationUpdateSchema
)

# Create Blueprint for specification routes
specification_routes = Blueprint('specifications', __name__)

@specification_routes.route('', methods=['POST'])
@require_auth
def create_specification() -> Tuple[Dict[str, Any], int]:
    """
    Create a new specification within a project.
    
    Requirement: 1.2 Scope/4. Data Management - CRUD operations for specifications
    Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization
    
    Returns:
        Tuple[Dict[str, Any], int]: Created specification data and HTTP 201 status
        
    Raises:
        ValidationError: If request data is invalid
        DatabaseError: If database operation fails
    """
    try:
        # Extract project ID and specification data from request
        project_id = UUID(request.args.get('project_id'))
        spec_data = request.get_json()
        
        # Get specification service from app context
        spec_service: SpecificationService = request.app.specification_service
        
        # Create specification
        created_spec = spec_service.create_specification(
            project_id=project_id,
            spec_data=spec_data
        )
        
        return jsonify(created_spec), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid project ID format'}), 400
    except Exception as e:
        request.app.logger.error(f"Failed to create specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@specification_routes.route('/<uuid:spec_id>', methods=['GET'])
@require_auth
def get_specification(spec_id: UUID) -> Tuple[Dict[str, Any], int]:
    """
    Retrieve a specification by ID.
    
    Requirement: 1.2 Scope/4. Data Management - Data retrieval operations
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Tuple[Dict[str, Any], int]: Specification data and HTTP 200 status
        
    Raises:
        ResourceNotFoundError: If specification not found
        DatabaseError: If database operation fails
    """
    try:
        # Get specification service from app context
        spec_service: SpecificationService = request.app.specification_service
        
        # Retrieve specification
        specification = spec_service.get_specification(spec_id)
        
        return jsonify(specification), 200
        
    except Exception as e:
        request.app.logger.error(f"Failed to get specification: {str(e)}")
        return jsonify({'error': str(e)}), 404

@specification_routes.route('/<uuid:spec_id>', methods=['PUT'])
@require_auth
def update_specification(spec_id: UUID) -> Tuple[Dict[str, Any], int]:
    """
    Update an existing specification.
    
    Requirement: 1.2 Scope/4. Data Management - Data update operations
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Tuple[Dict[str, Any], int]: Updated specification data and HTTP 200 status
        
    Raises:
        ResourceNotFoundError: If specification not found
        ValidationError: If update data is invalid
        DatabaseError: If database operation fails
    """
    try:
        # Extract update data from request
        update_data = request.get_json()
        
        # Get specification service from app context
        spec_service: SpecificationService = request.app.specification_service
        
        # Update specification
        updated_spec = spec_service.update_specification(
            spec_id=spec_id,
            spec_data=update_data
        )
        
        return jsonify(updated_spec), 200
        
    except Exception as e:
        request.app.logger.error(f"Failed to update specification: {str(e)}")
        return jsonify({'error': str(e)}), 400

@specification_routes.route('/<uuid:spec_id>', methods=['DELETE'])
@require_auth
def delete_specification(spec_id: UUID) -> Tuple[Dict[str, Any], int]:
    """
    Soft delete a specification.
    
    Requirement: 1.2 Scope/4. Data Management - Data deletion operations
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Tuple[Dict[str, Any], int]: Success message and HTTP 204 status
        
    Raises:
        ResourceNotFoundError: If specification not found
        DatabaseError: If database operation fails
    """
    try:
        # Get specification service from app context
        spec_service: SpecificationService = request.app.specification_service
        
        # Delete specification
        spec_service.delete_specification(spec_id)
        
        return jsonify({'message': 'Specification deleted successfully'}), 204
        
    except Exception as e:
        request.app.logger.error(f"Failed to delete specification: {str(e)}")
        return jsonify({'error': str(e)}), 404

@specification_routes.route('/project/<uuid:project_id>', methods=['GET'])
@require_auth
def list_project_specifications(project_id: UUID) -> Tuple[Dict[str, Any], int]:
    """
    List all specifications for a project.
    
    Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization
    
    Args:
        project_id: UUID of the project
        
    Returns:
        Tuple[Dict[str, Any], int]: List of specifications and HTTP 200 status
        
    Raises:
        DatabaseError: If database operation fails
    """
    try:
        # Get specification service from app context
        spec_service: SpecificationService = request.app.specification_service
        
        # List project specifications
        specifications = spec_service.list_project_specifications(project_id)
        
        return jsonify({'specifications': specifications}), 200
        
    except Exception as e:
        request.app.logger.error(f"Failed to list specifications: {str(e)}")
        return jsonify({'error': str(e)}), 500