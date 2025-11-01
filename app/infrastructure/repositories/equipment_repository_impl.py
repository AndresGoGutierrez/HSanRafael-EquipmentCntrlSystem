from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.ports.equipment_repository import EquipmentRepository
from app.domain.entities.equipment import Equipment
from app.infrastructure.models.equipment_model import EquipmentModel


class EquipmentRepositoryImpl(EquipmentRepository):
    """SQLAlchemy implementation of the EquipmentRepository interface."""

    def __init__(self, db: Session):
        self.db = db

    # Mappers

    def _to_entity(self, model: Optional[EquipmentModel]) -> Optional[Equipment]:
        """Convert ORM model to domain entity."""
        if model is None:
            return None
        return Equipment(
            id=model.id,
            name=model.name,
            equipment_type=model.equipment_type,
            category=model.category,
            serial_number=model.serial_number,
            qr_code=model.qr_code,
            image_url=model.image_url,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Equipment) -> EquipmentModel:
        """Convert domain entity to ORM model."""
        return EquipmentModel(
            id=entity.id,
            name=entity.name,
            equipment_type=entity.equipment_type,
            category=entity.category,
            serial_number=entity.serial_number,
            qr_code=entity.qr_code,
            image_url=entity.image_url,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    # CRUD Operations

    def create(self, equipment: Equipment) -> Equipment:
        """Create and persist new equipment."""
        try:
            db_equipment = self._to_model(equipment)
            self.db.add(db_equipment)
            self.db.commit()
            self.db.refresh(db_equipment)
            return self._to_entity(db_equipment)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """Retrieve equipment by ID."""
        db_equipment = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.id == equipment_id)
            .first()
        )
        return self._to_entity(db_equipment)

    def get_by_qr_code(self, qr_code: str) -> Optional[Equipment]:
        """Retrieve equipment by its QR code."""
        db_equipment = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.qr_code == qr_code)
            .first()
        )
        return self._to_entity(db_equipment)

    def get_by_serial_number(self, serial_number: str) -> Optional[Equipment]:
        """Retrieve equipment by its serial number."""
        db_equipment = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.serial_number == serial_number)
            .first()
        )
        return self._to_entity(db_equipment)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Equipment]:
        """Retrieve a paginated list of all equipment."""
        db_equipment = self.db.query(EquipmentModel).offset(skip).limit(limit).all()
        return [self._to_entity(eq) for eq in db_equipment]

    def update(self, equipment: Equipment) -> Optional[Equipment]:
        """Update existing equipment data."""
        db_equipment = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.id == equipment.id)
            .first()
        )

        if not db_equipment:
            return None

        db_equipment.name = equipment.name
        db_equipment.equipment_type = equipment.equipment_type
        db_equipment.category = equipment.category
        db_equipment.serial_number = equipment.serial_number
        db_equipment.qr_code = equipment.qr_code
        db_equipment.image_url = equipment.image_url
        db_equipment.description = equipment.description
        db_equipment.is_active = equipment.is_active

        try:
            self.db.commit()
            self.db.refresh(db_equipment)
            return self._to_entity(db_equipment)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, equipment_id: int) -> bool:
        """Delete equipment by ID."""
        db_equipment = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.id == equipment_id)
            .first()
        )

        if not db_equipment:
            return False

        try:
            self.db.delete(db_equipment)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise
