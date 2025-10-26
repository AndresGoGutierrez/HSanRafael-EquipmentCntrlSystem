from __future__ import annotations
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from app.core.config import settings

class AccessType(str, Enum):
    """Types of access records"""
    INGRESO = "ingreso"
    EGRESO = "egreso"

class AccessStatus(str, Enum):
    """Status of access records"""
    ACTIVO = "activo"
    COMPLETADO = "completado"
    VENCIDO = "vencido"
    BLOQUEADO = "bloqueado"

class AccessRecord:
    """Entity representing an access record"""

    def __init__(
        self,
        *,
        id: Optional[int] = None,
        equipment_id: int,
        user_id: int,
        access_type: AccessType,
        status: AccessStatus = AccessStatus.ACTIVO,
        entry_time: Optional[datetime] = None,
        exit_time: Optional[datetime] = None,
        expected_exit_time: Optional[datetime] = None,
        notes: Optional[str]= None,
        created_at: Optional[datetime]= None
    ):
        utc_now = datetime.now(timezone.utc)

        self.id = id
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.access_type = access_type
        self.status = status
        self.entry_time = entry_time or utc_now
        self.exit_time = exit_time
        self.expected_exit_time = expected_exit_time or (
            utc_now + timedelta(days=settings.EQUIPMENT_MAX_STAY_DAYS)
        )
        self.notes = notes
        self.created_at = created_at or utc_now

    def is_expired(self) -> bool:
        """Determine if the access record has expired base on expected exit time"""
        if self.expected_exit_time and self.status == AccessStatus.ACTIVO:
            return datetime.now(timezone.utc) > self.expected_exit_time
        return False

    def mark_as_completed(self) -> None:
        """Mark the access record as completed by setting exit time and updating status"""
        if not self.exit_time:
            self.exit_time = datetime.now(timezone.utc)
        self.status = AccessStatus.COMPLETADO

    def calculate_expected_exit(self) -> datetime:
        """Calculate the expected exit time based on the current time and max stay duration"""
        return datetime.now(timezone.utc) + timedelta(days=settings.EQUIPMENT_MAX_STAY_DAYS)

    def to_dict(self) -> dict:
        """Convert the AccessRecord instance to a dictionary representation"""
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "user_id": self.user_id,
            "access_type": self.access_type.value,
            "status": self.status.value,
            "entry_time": self.entry_time.isoformat() if self.entry_time else None,
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
            "expected_exit_time": self.expected_exit_time.isoformat() if self.expected_exit_time else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"<AccessRecord id={self.id} type={self.access_type.value} "
            f"status={self.status.value} user_id={self.user_id} equipment_id={self.equipment_id}>"
        )