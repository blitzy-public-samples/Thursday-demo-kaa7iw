# External imports - versions specified as per requirements
from flask import Blueprint, request, jsonify  # version: 2.0+
from typing import Dict, Any, Tuple, List  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ...models.bullet_item import BulletItem
from ...schemas.bullet_item import (
    BulletItemSchema,
    BulletItemCreateSchema,
    BulletItemUpdateSchema
)
from ...services.bullet_item_service import BulletItemService
from ...middleware.auth import require_auth

# Human Tasks:
# 1. Configure rate limiting for bullet item endpoints
# 2. Set up monitoring for bullet item operations
# 3. Review error messages with product team
# 4. Configure logging for bullet item operations

# Create Blueprint for bullet item routes
bullet_items_bp = Blueprint('bullet_items', __name__)

# Initialize service
bullet_item_service = BulletItemService()

@bullet_items_bp.route('/<uuid:spec_id>/items', methods=['POST'])
@require_auth
def create_bullet_item(spec_id: UUID) -> Tuple[Dict[str, Any], int]:
    """
    Create a new bullet item within a specification.
    
    Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Tuple[Dict[str, Any], int]: Created bullet item data and 201 status code
    """
    # Get request data
    data = request.get_json()
    
    # Add specification ID to data
    data['spec_id'] = str(spec_id)
    
    # Create bullet item through service
    created_item = bullet_item_service.create_bullet_item(data)
    
    return created_item, 201

@bullet_items_bp.route('/items/<uuid:item_id>', methods=['GET'])
@require_auth
def get_bullet_item(item_id: UUID) -> Dict[str, Any]:
    """
    Retrieve a specific bullet item by ID.
    
    Requirement: 1.2 Scope/4. Data Management - Data retrieval operations
    
    Args:
        item_id: UUID of the bullet item
        
    Returns:
        Dict[str, Any]: Bullet item data
    """
    # Get bullet item through service
    item = bullet_item_service.get_bullet_item(item_id)
    
    return item

@bullet_items_bp.route('/items/<uuid:item_id>', methods=['PUT'])
@require_auth
def update_bullet_item(item_id: UUID) -> Dict[str, Any]:
    """
    Update an existing bullet item.
    
    Requirement: 1.2 Scope/4. Data Management - Data update operations
    
    Args:
        item_id: UUID of the bullet item
        
    Returns:
        Dict[str, Any]: Updated bullet item data
    """
    # Get request data
    data = request.get_json()
    
    # Update bullet item through service
    updated_item = bullet_item_service.update_bullet_item(item_id, data)
    
    return updated_item

@bullet_items_bp.route('/items/<uuid:item_id>', methods=['DELETE'])
@require_auth
def delete_bullet_item(item_id: UUID) -> Tuple[Dict[str, str], int]:
    """
    Delete a bullet item.
    
    Requirement: 1.2 Scope/4. Data Management - Data deletion operations
    
    Args:
        item_id: UUID of the bullet item
        
    Returns:
        Tuple[Dict[str, str], int]: Success message and 200 status code
    """
    # Delete bullet item through service
    result = bullet_item_service.delete_bullet_item(item_id)
    
    return result, 200

@bullet_items_bp.route('/<uuid:spec_id>/items', methods=['GET'])
@require_auth
def list_specification_items(spec_id: UUID) -> Dict[str, List[Dict[str, Any]]]:
    """
    List all bullet items for a specification.
    
    Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: List of bullet items
    """
    # Get bullet items through service
    items = bullet_item_service.list_specification_items(spec_id)
    
    return {'items': items}

@bullet_items_bp.route('/<uuid:spec_id>/items/reorder', methods=['PUT'])
@require_auth
def reorder_items(spec_id: UUID) -> Dict[str, List[Dict[str, Any]]]:
    """
    Update the order of multiple bullet items within a specification.
    
    Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
    
    Args:
        spec_id: UUID of the specification
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: List of updated bullet items
    """
    # Get request data
    data = request.get_json()
    
    # Validate request data structure
    if not isinstance(data, dict) or 'orders' not in data:
        return {'error': 'Invalid request format'}, 400
    
    # Reorder items through service
    updated_items = bullet_item_service.reorder_items(spec_id, data['orders'])
    
    return {'items': updated_items}