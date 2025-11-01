from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.domain.ports.access_record_repository import AccessRecordRepository
from app.domain.entities.access_record import AccessRecord, AccessStatus
from app.infrastructure.models.access_record_model import AccessRecordModel


class AccessRecordRepositoryImpl(AccessRecordRepository):
    """Concrete implementation of the AccessRecordRepository interface."""

    def __init__(self, db: Session):
        self.db = db


    # Private mapping helpers

    def _to_entity(self, model: AccessRecordModel) -> AccessRecord:
        """Convert ORM model to domain entity."""
        if not model:
            return None
        return AccessRecord(
            id=model.id,
            equipment_id=model.equipment_id,
            user_id=model.user_id,
            access_type=model.access_type,
            status=model.status,
            entry_time=model.entry_time,
            exit_time=model.exit_time,
            expected_exit_time=model.expected_exit_time,
            notes=model.notes,
            created_at=model.created_at,
        )

    def _to_model(self, entity: AccessRecord) -> AccessRecordModel:
        """Convert domain entity to ORM model."""
        return AccessRecordModel(
            id=entity.id,
            equipment_id=entity.equipment_id,
            user_id=entity.user_id,
            access_type=entity.access_type,
            status=entity.status,
            entry_time=entity.entry_time,
            exit_time=entity.exit_time,
            expected_exit_time=entity.expected_exit_time,
            notes=entity.notes,
            created_at=entity.created_at,
        )


    # CRUD operations

    def create(self, access_record: AccessRecord) -> AccessRecord:
        """Create a new access record."""
        db_record = self._to_model(access_record)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return self._to_entity(db_record)

    def get_by_id(self, record_id: int) -> Optional[AccessRecord]:
        """Retrieve an access record by its ID."""
        db_record = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.id == record_id)
            .first()
        )
        return self._to_entity(db_record)

    def get_active_by_equipment(self, equipment_id: int) -> Optional[AccessRecord]:
        """Retrieve the currently active access record for a given equipment."""
        db_record = (
            self.db.query(AccessRecordModel)
            .filter(
                and_(
                    AccessRecordModel.equipment_id == equipment_id,
                    AccessRecordModel.status == AccessStatus.ACTIVO,
                )
            )
            .first()
        )
        return self._to_entity(db_record)

    def get_by_equipment(
        self, equipment_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """List all access records for a specific equipment."""
        db_records = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.equipment_id == equipment_id)
            .order_by(AccessRecordModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_records]

    def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """List all access records for a specific user."""
        db_records = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.user_id == user_id)
            .order_by(AccessRecordModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_records]

    def get_active_records(self) -> List[AccessRecord]:
        """Retrieve all currently active access records."""
        db_records = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.status == AccessStatus.ACTIVO)
            .order_by(AccessRecordModel.entry_time.desc())
            .all()
        )
        return [self._to_entity(r) for r in db_records]

    def get_expired_records(self) -> List[AccessRecord]:
        """Retrieve all expired access records (still active but past expected exit)."""
        now = datetime.utcnow()
        db_records = (
            self.db.query(AccessRecordModel)
            .filter(
                and_(
                    AccessRecordModel.status == AccessStatus.ACTIVO,
                    AccessRecordModel.expected_exit_time < now,
                )
            )
            .all()
        )
        return [self._to_entity(r) for r in db_records]

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AccessRecord]:
        """Retrieve access records within a date range."""
        db_records = (
            self.db.query(AccessRecordModel)
            .filter(
                and_(
                    AccessRecordModel.created_at >= start_date,
                    AccessRecordModel.created_at <= end_date,
                )
            )
            .order_by(AccessRecordModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_records]

    def update(self, access_record: AccessRecord) -> Optional[AccessRecord]:
        """Update an existing access record."""
        db_record = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.id == access_record.id)
            .first()
        )
        if not db_record:
            return None

        db_record.status = access_record.status
        db_record.exit_time = access_record.exit_time
        db_record.notes = access_record.notes
        self.db.commit()
        self.db.refresh(db_record)
        return self._to_entity(db_record)

    def delete(self, record_id: int) -> bool:
        """Delete an access record by ID."""
        db_record = (
            self.db.query(AccessRecordModel)
            .filter(AccessRecordModel.id == record_id)
            .first()
        )
        if not db_record:
            return False

        self.db.delete(db_record)
        self.db.commit()
        return True
