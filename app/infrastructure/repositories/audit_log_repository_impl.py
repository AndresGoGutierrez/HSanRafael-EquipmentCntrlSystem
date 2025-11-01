from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from app.domain.ports.audit_log_repository import AuditLogRepository
from app.domain.entities.audit_log import AuditLog, AuditAction
from app.infrastructure.models.audit_log_model import AuditLogModel


class AuditLogRepositoryImpl(AuditLogRepository):
    """SQLAlchemy implementation of the AuditLogRepository interface."""

    def __init__(self, db: Session):
        self.db = db

    # Mapping helpers


    def _to_entity(self, model: Optional[AuditLogModel]) -> Optional[AuditLog]:
        """Convert ORM model to domain entity."""
        if model is None:
            return None
        return AuditLog(
            id=model.id,
            user_id=model.user_id,
            action=model.action,
            entity_type=model.entity_type,
            entity_id=model.entity_id,
            details=model.details,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            created_at=model.created_at,
        )

    def _to_model(self, entity: AuditLog) -> AuditLogModel:
        """Convert domain entity to ORM model."""
        return AuditLogModel(
            id=entity.id,
            user_id=entity.user_id,
            action=entity.action,
            entity_type=entity.entity_type,
            entity_id=entity.entity_id,
            details=entity.details,
            ip_address=entity.ip_address,
            user_agent=entity.user_agent,
            created_at=entity.created_at,
        )


    # CRUD Operations


    def create(self, audit_log: AuditLog) -> AuditLog:
        """Persist a new audit log entry."""
        try:
            db_log = self._to_model(audit_log)
            self.db.add(db_log)
            self.db.commit()
            self.db.refresh(db_log)
            return self._to_entity(db_log)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, log_id: int) -> Optional[AuditLog]:
        """Retrieve a single audit log by its ID."""
        db_log = self.db.query(AuditLogModel).filter(AuditLogModel.id == log_id).first()
        return self._to_entity(db_log)

    def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve audit logs for a specific user."""
        db_logs = (
            self.db.query(AuditLogModel)
            .filter(AuditLogModel.user_id == user_id)
            .order_by(AuditLogModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(log) for log in db_logs]

    def get_by_action(
        self, action: AuditAction, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve audit logs by action type."""
        db_logs = (
            self.db.query(AuditLogModel)
            .filter(AuditLogModel.action == action)
            .order_by(AuditLogModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(log) for log in db_logs]

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """Retrieve audit logs within a date range."""
        db_logs = (
            self.db.query(AuditLogModel)
            .filter(
                and_(
                    AuditLogModel.created_at >= start_date,
                    AuditLogModel.created_at <= end_date,
                )
            )
            .order_by(AuditLogModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(log) for log in db_logs]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Retrieve all audit logs, paginated."""
        db_logs = (
            self.db.query(AuditLogModel)
            .order_by(AuditLogModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(log) for log in db_logs]
