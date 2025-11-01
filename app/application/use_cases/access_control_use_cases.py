from typing import List, Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.domain.entities.access_record import AccessRecord, AccessType, AccessStatus
from app.domain.entities.user import User
from app.domain.ports.access_record_repository import AccessRecordRepository
from app.domain.ports.equipment_repository import EquipmentRepository


class AccessControlUseCases:
    """Handles all business logic for equipment access control (entry, exit, audit, and monitoring)."""

    def __init__(
        self,
        access_record_repository: AccessRecordRepository,
        equipment_repository: EquipmentRepository,
    ):
        self.access_record_repository = access_record_repository
        self.equipment_repository = equipment_repository

    # Helpers

    def _find_equipment(self, identifier: str):
        """Find equipment by QR code or serial number."""
        equipment = self.equipment_repository.get_by_qr_code(
            identifier
        ) or self.equipment_repository.get_by_serial_number(identifier)
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipment not found with the provided identifier",
            )
        return equipment


    # Entry registration

    def register_entry(
        self, equipment_identifier: str, user: User, notes: Optional[str] = None
    ) -> AccessRecord:
        """
        Register the entry of equipment into the hospital.
        """
        equipment = self._find_equipment(equipment_identifier)

        if not equipment.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipment is not active",
            )

        # Check if there’s already an active record for this equipment
        active_record = self.access_record_repository.get_active_by_equipment(
            equipment.id
        )
        if active_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Equipment already inside since {active_record.entry_time}",
            )

        now = datetime.now(timezone.utc)
        access_record = AccessRecord(
            id=None,
            equipment_id=equipment.id,
            user_id=user.id,
            access_type=AccessType.INGRESO,
            status=AccessStatus.ACTIVO,
            entry_time=now,
            exit_time=None,
            expected_exit_time=None,
            notes=notes,
        )

        access_record.expected_exit_time = access_record.calculate_expected_exit()
        return self.access_record_repository.create(access_record)


    #  Exit registration

    def register_exit(
        self, equipment_identifier: str, user: User, notes: Optional[str] = None
    ) -> AccessRecord:
        """
        Register the exit of equipment from the hospital.
        """
        equipment = self._find_equipment(equipment_identifier)

        # Get the currently active record
        active_record = self.access_record_repository.get_active_by_equipment(
            equipment.id
        )
        if not active_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No active entry found for this equipment",
            )

        # Sanity check: ensure the equipment ID matches
        if active_record.equipment_id != equipment.id:
            active_record.status = AccessStatus.BLOQUEADO
            self.access_record_repository.update(active_record)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Equipment mismatch detected. Exit blocked for security reasons.",
            )

        active_record.exit_time = datetime.now(timezone.utc)
        active_record.status = AccessStatus.COMPLETADO
        if notes:
            active_record.notes = f"{active_record.notes or ''}\nExit: {notes}".strip()

        return self.access_record_repository.update(active_record)


    #  Queries

    def get_active_equipment(self) -> List[AccessRecord]:
        """Retrieve all currently active access records."""
        return self.access_record_repository.get_active_records()

    def get_expired_equipment(self) -> List[AccessRecord]:
        """Retrieve all equipment records whose expected exit time has passed."""
        expired_records = self.access_record_repository.get_expired_records()

        # Mark expired active records
        for record in expired_records:
            if record.status == AccessStatus.ACTIVO:
                record.status = AccessStatus.VENCIDO
                self.access_record_repository.update(record)

        return expired_records

    def get_equipment_history(
        self, equipment_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """Retrieve the access history of a specific equipment."""
        equipment = self.equipment_repository.get_by_id(equipment_id)
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
            )
        return self.access_record_repository.get_by_equipment(equipment_id, skip, limit)

    def get_user_history(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """Retrieve all access records created by a specific user."""
        return self.access_record_repository.get_by_user(user_id, skip, limit)

    def get_records_by_date_range(
        self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """Retrieve all records within a specific date range."""
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date",
            )

        return self.access_record_repository.get_by_date_range(
            start_date, end_date, skip, limit
        )


    # Forced exit (admin)

    def force_exit(self, record_id: int, user: User, reason: str) -> AccessRecord:
        """
        Force exit of equipment (admin only).
        """
        record = self.access_record_repository.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Access record not found"
            )

        if record.status not in (AccessStatus.ACTIVO, AccessStatus.VENCIDO):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Record is not active or expired",
            )

        record.exit_time = datetime.now(timezone.utc)
        record.status = AccessStatus.COMPLETADO
        record.notes = (
            f"{record.notes or ''}\nForced exit by {user.full_name}: {reason}".strip()
        )

        return self.access_record_repository.update(record)
