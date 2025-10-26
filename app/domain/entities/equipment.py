from datetime import datetime, timezone
from enum import Enum
from typing import Optional

class EquipmentType(str, Enum):
    """Equipment type classification"""
    FRECUENTE = "frecuente"
    NO_FRECUENTE = "no_frecuente"

class EquipmentCategory(str, Enum):
    """Equipment category"""
    TECNOLOGICO = "tecnologico"
    BIOMEDICO = "bioomedico"

class Equipment: 
    """Equipment entity representing on equipment item in the inventory"""

    def __init__(
        self,
        id: Optional[int],
        name: str,
        equipment_type: EquipmentType,
        category: EquipmentCategory,
        serial_number: Optional[str] = None,
        qr_code: Optional[str] = None,
        image_url: Optional[str] = None,
        description: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        
        if not name:
            raise ValueError("Equipmen name cannot be empty")
        
        if not isinstance(equipment_type, EquipmentType):
            raise ValueError("equipment_type must be an instance of EquipmentType Enum")
        
        if not isinstance(category, EquipmentCategory):
            raise ValueError("category must be an instance of EquipmentCategory Enum")
        
        # Atributes

        self.id = id
        self.name = name
        self.equipment_type = equipment_type
        self.category = category
        self.serial_number = serial_number.strip() if serial_number else None
        self.qr_code = qr_code.strip() if qr_code else None
        self.image_url = image_url
        self.description = description
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

        # Methods of negotiation

    def requires_photo(self) -> bool:
        """Determine if the equipment requires a photo based on its category"""
        return self.category == EquipmentCategory.BIOMEDICO
        
    def is_frequent(self) -> bool:
        """Check if the equipment is classified as frequent"""
        return self.equipment_type == EquipmentType.FRECUENTE
        
    def deactivate(self) -> None:
        """Deactivate the equipment"""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        """Activate the equipment"""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        """Representation of the Equipment entity"""
        return f"<Equipment(id={self.id}, name='{self.name}', type='{self.equipment_type.value}')>"