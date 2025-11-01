from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.equipment import Equipment


class EquipmentRepository(ABC):
    """Port interface for equipment repository operations.
    
    Defines the contract for persistence and retrieval of Equipment entities.
    Any implementation (e.g., SQLAlchemy, MongoDB, or in-memory) must follow
    this interface to maintain independence from infrastructure details.
    """

    # ───────────────────────────────────────────────
    # CRUD OPERATIONS
    # ───────────────────────────────────────────────

    @abstractmethod
    def create(self, equipment: Equipment) -> Equipment:
        """Create a new equipment record.
        
        Args:
            equipment: Equipment domain entity to persist.
        
        Returns:
            The created Equipment entity with its ID populated.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """Retrieve equipment by its unique ID.
        
        Args:
            equipment_id: Database ID of the equipment.
        
        Returns:
            Equipment entity if found, otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_qr_code(self, qr_code: str) -> Optional[Equipment]:
        """Retrieve equipment using its QR code."""
        raise NotImplementedError

    @abstractmethod
    def get_by_serial_number(self, serial_number: str) -> Optional[Equipment]:
        """Retrieve equipment using its serial number."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Equipment]:
        """List all equipment with pagination support.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List of Equipment entities.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, equipment: Equipment) -> Equipment:
        """Update an existing equipment record.
        
        Args:
            equipment: Equipment entity with updated fields.
        
        Returns:
            Updated Equipment entity.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, equipment_id: int) -> bool:
        """Delete equipment by its ID.
        
        Args:
            equipment_id: ID of the equipment to delete.
        
        Returns:
            True if deletion was successful, False otherwise.
        """
        raise NotImplementedError