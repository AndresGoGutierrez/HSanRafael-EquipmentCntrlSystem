"""
Initialize SQLAlchemy models for the application.

This module ensures that all model classes are imported and
registered with the SQLAlchemy Base metadata before table creation.
"""

from app.infrastructure.models.user_model import UserModel
from app.infrastructure.models.audit_log_model import AuditLogModel
from app.infrastructure.models.access_record_model import AccessRecordModel
from app.infrastructure.models.equipment_model import EquipmentModel

__all__ = [
    "UserModel",
    "AuditLogModel",
    "AccessRecordModel",
    "EquipmentModel",
]
