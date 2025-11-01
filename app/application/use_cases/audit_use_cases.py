from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import Request

from app.domain.entities.audit_log import AuditLog, AuditAction
from app.domain.entities.user import User
from app.domain.ports.audit_log_repository import AuditLogRepository


class AuditUseCases:
    """Application service for managing audit logs and tracking user/system actions."""

    def __init__(self, audit_log_repository: AuditLogRepository):
        self._audit_log_repository = audit_log_repository

    # === ACTION LOGGING ===
    def log_action(
        self,
        action: AuditAction,
        entity_type: str,
        entity_id: Optional[int] = None,
        user: Optional[User] = None,
        details: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None,
    ) -> AuditLog:
        """
        Create an audit log entry for a performed action.

        Args:
            action: Type of action performed (e.g., CREATE, UPDATE, DELETE).
            entity_type: The type or name of the affected entity (e.g., "Equipment").
            entity_id: Optional ID of the affected entity.
            user: Optional User who performed the action.
            details: Optional structured metadata about the action.
            request: Optional FastAPI Request object (used for IP and user agent tracking).

        Returns:
            The created AuditLog entity.
        """
        ip_address = None
        user_agent = None

        # Extract metadata from request
        if request:
            client = getattr(request, "client", None)
            ip_address = getattr(client, "host", None)
            user_agent = request.headers.get("user-agent")

        audit_log = AuditLog(
            id=None,
            user_id=user.id if user else None,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow(),
        )

        return self._audit_log_repository.create(audit_log)

    # === QUERY METHODS ===
    def get_logs_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        """
        Retrieve audit logs for a specific user.

        Args:
            user_id: User ID.
            skip: Offset for pagination.
            limit: Maximum number of results.

        Returns:
            List of AuditLog entries.
        """
        return self._audit_log_repository.get_by_user(user_id, skip, limit)

    def get_logs_by_action(
        self, action: AuditAction, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        """
        Retrieve audit logs filtered by action type.

        Args:
            action: Type of action (CREATE, UPDATE, DELETE, etc.).
            skip: Offset for pagination.
            limit: Maximum number of results.

        Returns:
            List of AuditLog entries.
        """
        return self._audit_log_repository.get_by_action(action, skip, limit)

    def get_logs_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """
        Retrieve audit logs within a specific date range.

        Args:
            start_date: Start of the date range.
            end_date: End of the date range.
            skip: Offset for pagination.
            limit: Maximum number of results.

        Returns:
            List of AuditLog entries.
        """
        return self._audit_log_repository.get_by_date_range(
            start_date, end_date, skip, limit
        )

    def get_all_logs(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """
        Retrieve all audit logs.

        Args:
            skip: Offset for pagination.
            limit: Maximum number of results.

        Returns:
            List of all AuditLog entries.
        """
        return self._audit_log_repository.get_all(skip, limit)
