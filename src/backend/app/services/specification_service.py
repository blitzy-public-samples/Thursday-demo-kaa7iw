"""
Service layer implementation for managing specifications, providing business logic for CRUD operations
and validation of specifications within projects.

Human Tasks:
1. Verify PostgreSQL database user has proper permissions for specification operations
2. Review caching strategy and TTL values with the team
3. Confirm error message templates with product team
4. Validate rate limiting configuration for specification endpoints
"""

# External imports - versions specified as per requirements
from typing import Dict, List, Optional  # version: 3.9+
from uuid import UUID  # version: 3.9+

# Internal imports
from ..models.specification import Specification
from ..schemas.specification import (
    SpecificationSchema,
    SpecificationCreateSchema,
    SpecificationUpdateSchema
)
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
    ValidationError,
    DatabaseError
)

class SpecificationService:
    """
    Service class implementing business logic for specification management.
    
    Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization of specifications
    Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
    """
    
    def __init__(self, cache_service: CacheService) -> None:
        """
        Initialize specification service with cache service and schemas.
        
        Args:
            cache_service: Instance of CacheService for caching operations
        """
        self._cache_service = cache_service
        self._schema = SpecificationSchema()
        self._create_schema = SpecificationCreateSchema()
        self._update_schema = SpecificationUpdateSchema()

    def create_specification(self, project_id: UUID, spec_data: Dict) -> Dict:
        """
        Create a new specification within a project.
        
        Requirement: 1.2 Scope/4. Data Management - CRUD operations with validation
        
        Args:
            project_id: UUID of the project
            spec_data: Dictionary containing specification data
            
        Returns:
            Dict: Created specification data
            
        Raises:
            ValidationError: If specification data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate specification data
            spec_data['project_id'] = project_id
            validated_data = self._create_schema.load(spec_data)
            
            # Create specification record
            specification = create_record(Specification, validated_data)
            
            # Cache the new specification
            spec_dict = self._schema.dump(specification)
            self._cache_service.set_specification(
                str(specification.id),
                spec_dict
            )
            
            return spec_dict
            
        except ValidationError as e:
            raise ValidationError('SPEC001', e.messages)
        except Exception as e:
            raise DatabaseError() from e

    def get_specification(self, spec_id: UUID) -> Dict:
        """
        Retrieve a specification by ID.
        
        Requirement: 1.2 Scope/4. Data Management - Data retrieval operations
        
        Args:
            spec_id: UUID of the specification
            
        Returns:
            Dict: Specification data
            
        Raises:
            ResourceNotFoundError: If specification not found
            DatabaseError: If database operation fails
        """
        try:
            # Check cache first
            cached_spec = self._cache_service.get_specification(str(spec_id))
            if cached_spec:
                return cached_spec
            
            # If not in cache, get from database
            specification = get_record(Specification, spec_id)
            if not specification:
                raise ResourceNotFoundError('SPEC001')
            
            # Cache and return specification
            spec_dict = self._schema.dump(specification)
            self._cache_service.set_specification(
                str(spec_id),
                spec_dict
            )
            
            return spec_dict
            
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError() from e

    def update_specification(self, spec_id: UUID, spec_data: Dict) -> Dict:
        """
        Update an existing specification.
        
        Requirement: 1.2 Scope/4. Data Management - Data update operations
        
        Args:
            spec_id: UUID of the specification
            spec_data: Dictionary containing updated specification data
            
        Returns:
            Dict: Updated specification data
            
        Raises:
            ResourceNotFoundError: If specification not found
            ValidationError: If update data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Get existing specification
            specification = get_record(Specification, spec_id)
            if not specification:
                raise ResourceNotFoundError('SPEC001')
            
            # Validate update data
            validated_data = self._update_schema.load(spec_data)
            
            # Update specification
            updated_spec = update_record(specification, validated_data)
            
            # Update cache and return
            spec_dict = self._schema.dump(updated_spec)
            self._cache_service.set_specification(
                str(spec_id),
                spec_dict
            )
            
            return spec_dict
            
        except ValidationError as e:
            raise ValidationError('SPEC001', e.messages)
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError() from e

    def delete_specification(self, spec_id: UUID) -> None:
        """
        Soft delete a specification.
        
        Requirement: 1.2 Scope/4. Data Management - Data deletion operations
        
        Args:
            spec_id: UUID of the specification
            
        Raises:
            ResourceNotFoundError: If specification not found
            DatabaseError: If database operation fails
        """
        try:
            # Get existing specification
            specification = get_record(Specification, spec_id)
            if not specification:
                raise ResourceNotFoundError('SPEC001')
            
            # Delete specification
            delete_record(specification)
            
            # Remove from cache
            self._cache_service.clear_cache()
            
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError() from e

    def list_project_specifications(self, project_id: UUID) -> List[Dict]:
        """
        List all specifications for a project.
        
        Requirement: 1.2 Scope/3. Specification Management - Hierarchical organization
        
        Args:
            project_id: UUID of the project
            
        Returns:
            List[Dict]: List of specification data
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            # List specifications with project filter
            specifications = list_records(
                Specification,
                {'project_id': project_id}
            )
            
            # Serialize specifications
            specs_dict = self._schema.dump(specifications, many=True)
            
            # Cache results with project key
            self._cache_service.set_project(
                str(project_id),
                {'specifications': specs_dict}
            )
            
            return specs_dict
            
        except Exception as e:
            raise DatabaseError() from e

    def validate_project_access(self, spec_id: UUID, project_id: UUID) -> bool:
        """
        Validate if specification belongs to given project.
        
        Requirement: 1.2 Scope/4. Data Management - Data validation and constraint enforcement
        
        Args:
            spec_id: UUID of the specification
            project_id: UUID of the project
            
        Returns:
            bool: True if specification belongs to project
            
        Raises:
            ResourceNotFoundError: If specification not found
            DatabaseError: If database operation fails
        """
        try:
            # Get specification
            specification = get_record(Specification, spec_id)
            if not specification:
                raise ResourceNotFoundError('SPEC001')
            
            # Compare project IDs
            return specification.validate_project_access(project_id)
            
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError() from e