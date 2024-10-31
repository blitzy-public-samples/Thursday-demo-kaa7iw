"""
Service layer for managing bullet item operations, handling CRUD operations and business logic.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for bullet item operations
2. Review database indexing strategy for bullet item queries
3. Confirm cascade delete settings are properly configured
4. Check database audit logging is enabled for bullet item operations
"""

# External imports - versions specified as per requirements
from typing import Dict, Any, List  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ..models.bullet_item import BulletItem
from ..schemas.bullet_item import (
    BulletItemSchema,
    BulletItemCreateSchema,
    BulletItemUpdateSchema
)
from ..database.operations import (
    create_record,
    get_record,
    update_record,
    delete_record,
    list_records
)
from ..utils.exceptions import ValidationError, ResourceNotFoundError

class BulletItemService:
    """
    Service class for managing bullet item operations.
    
    Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with data validation
    """
    
    def __init__(self) -> None:
        """
        Initialize bullet item service with schemas.
        
        Initializes schema instances for validation and serialization of bullet item data.
        """
        self.bullet_item_schema = BulletItemSchema()
        self.create_schema = BulletItemCreateSchema()
        self.update_schema = BulletItemUpdateSchema()
        self.model = BulletItem

    def create_bullet_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new bullet item within a specification.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for up to 10 ordered bullet items
        Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
        
        Args:
            data: Dictionary containing bullet item data
            
        Returns:
            Dict[str, Any]: Created bullet item data
            
        Raises:
            ValidationError: If data validation fails
            ResourceNotFoundError: If specification not found
        """
        # Validate input data
        validated_data = self.create_schema.load(data)
        
        # Check if specification exists and get current item count
        existing_items = list_records(
            self.model,
            filters={'spec_id': validated_data['spec_id']}
        )
        
        # Verify bullet item count is less than 10
        if len(existing_items) >= 10:
            raise ValidationError(
                'ITEM001',
                {'items': ['Maximum number of bullet items (10) reached']}
            )
        
        # Create bullet item record
        bullet_item = create_record(self.model, validated_data)
        
        # Return serialized data
        return self.bullet_item_schema.dump(bullet_item)

    def get_bullet_item(self, item_id: UUID) -> Dict[str, Any]:
        """
        Retrieve a bullet item by ID.
        
        Requirement: 1.2 Scope/4. Data Management - Data retrieval operations
        
        Args:
            item_id: UUID of the bullet item
            
        Returns:
            Dict[str, Any]: Bullet item data
            
        Raises:
            ResourceNotFoundError: If bullet item not found
        """
        # Get bullet item record
        bullet_item = get_record(self.model, item_id)
        
        if not bullet_item:
            raise ResourceNotFoundError('ITEM001')
        
        # Return serialized data
        return self.bullet_item_schema.dump(bullet_item)

    def update_bullet_item(self, item_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing bullet item.
        
        Requirement: 1.2 Scope/4. Data Management - Data update operations
        
        Args:
            item_id: UUID of the bullet item
            data: Dictionary containing update data
            
        Returns:
            Dict[str, Any]: Updated bullet item data
            
        Raises:
            ValidationError: If data validation fails
            ResourceNotFoundError: If bullet item not found
        """
        # Validate update data
        validated_data = self.update_schema.load(data)
        
        # Get existing bullet item
        bullet_item = get_record(self.model, item_id)
        if not bullet_item:
            raise ResourceNotFoundError('ITEM001')
        
        # Update bullet item record
        updated_item = update_record(bullet_item, validated_data)
        
        # Return serialized data
        return self.bullet_item_schema.dump(updated_item)

    def delete_bullet_item(self, item_id: UUID) -> Dict[str, str]:
        """
        Delete a bullet item.
        
        Requirement: 1.2 Scope/4. Data Management - Data deletion operations
        
        Args:
            item_id: UUID of the bullet item
            
        Returns:
            Dict[str, str]: Success message
            
        Raises:
            ResourceNotFoundError: If bullet item not found
        """
        # Get existing bullet item
        bullet_item = get_record(self.model, item_id)
        if not bullet_item:
            raise ResourceNotFoundError('ITEM001')
        
        # Soft delete bullet item record
        delete_record(bullet_item)
        
        return {'message': 'Bullet item deleted successfully'}

    def list_specification_items(self, spec_id: UUID) -> List[Dict[str, Any]]:
        """
        List all bullet items for a specification.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
        
        Args:
            spec_id: UUID of the specification
            
        Returns:
            List[Dict[str, Any]]: List of bullet items
        """
        # Get all bullet items for specification
        items = list_records(self.model, filters={'spec_id': spec_id})
        
        # Sort items by order
        items.sort(key=lambda x: x.order)
        
        # Return serialized data
        return self.bullet_item_schema.dump(items, many=True)

    def reorder_items(self, spec_id: UUID, order_updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Update the order of multiple bullet items.
        
        Requirement: 1.2 Scope/3. Specification Management - Support for ordered bullet items
        
        Args:
            spec_id: UUID of the specification
            order_updates: List of dictionaries containing item IDs and new orders
            
        Returns:
            List[Dict[str, Any]]: Updated bullet items
            
        Raises:
            ValidationError: If order updates are invalid
            ResourceNotFoundError: If any bullet item not found
        """
        # Validate order updates structure
        if not isinstance(order_updates, list):
            raise ValidationError(
                'ITEM002',
                {'order': ['Invalid order updates format']}
            )
        
        # Get all items for specification
        existing_items = list_records(self.model, filters={'spec_id': spec_id})
        existing_map = {str(item.id): item for item in existing_items}
        
        # Validate all items exist and belong to specification
        for update in order_updates:
            item_id = update.get('id')
            if not item_id or str(item_id) not in existing_map:
                raise ResourceNotFoundError('ITEM001')
            
            new_order = update.get('order')
            if not isinstance(new_order, int) or new_order < 0 or new_order > 9:
                raise ValidationError(
                    'ITEM002',
                    {'order': ['Order must be between 0 and 9']}
                )
        
        # Update order of each item
        updated_items = []
        for update in order_updates:
            item = existing_map[str(update['id'])]
            updated_item = update_record(item, {'order': update['order']})
            updated_items.append(updated_item)
        
        # Return serialized updated items
        return self.bullet_item_schema.dump(updated_items, many=True)