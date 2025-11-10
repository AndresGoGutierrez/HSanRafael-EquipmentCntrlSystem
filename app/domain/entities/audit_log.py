from __future__ import annotations  # Allows the use of future types (for Python <3.11)
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any


class AuditAction(str, Enum):
    """Tipes of audit actions"""

    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    EQUIPMENT_CREATED = "equipment_created"
    EQUIPMENT_UPDATED = "equipment_updated"
    EQUIPMENT_DELETED = "equipment_deleted"
    ACCESS_ENTRY = "access_entry"
    ACCESS_EXIT = "access_exit"
    ACCESS_BLOCKED = "access_blocked"
    ALERT_GENERATED = "alert_generated"
    REPORT_GENERATED = "report_generated"

    def __str__(self):
        return self.value


class AuditLog:
    """Audit Log entity representing an audit Log entry"""

    def __init__(
        self,
        *,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        action: AuditAction,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.details = details or {}
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the AuditLog instance to a dictionary representation"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat(),
        }

    def short_description(self) -> str:
        """Generate a short description of the audit log"""
        return f"[{self.created_at.isoformat()}] {self.action.value} on {self.entity_type} (ID={self.entity_id})"

    def __repr__(self) -> str:
        return f"<AuditLog action={self.action.value} entity={self.entity_type} id={self.entity_id}>"