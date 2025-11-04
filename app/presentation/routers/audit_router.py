from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.user import User
from app.domain.entities.audit_log import AuditAction
from app.presentation.schemas.audit_log_schema import (
    AuditLogResponse,
    AuditLogWithUser,
)
from app.presentation.dependencies.audit_dependencies import get_audit_use_cases
from app.presentation.dependencies.auth_dependencies import require_ti_or_admin
from app.application.use_cases.audit_use_cases import AuditUseCases

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


@router.get("/logs", response_model=List[AuditLogWithUser])
async def get_audit_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(
        100, ge=1, le=500, description="Maximum number of records to return"
    ),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[AuditAction] = Query(None, description="Filter by action type"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    audit_use_cases: AuditUseCases = Depends(get_audit_use_cases),
    current_user: User = Depends(require_ti_or_admin),
) -> List[AuditLogWithUser]:
    """
    Retrieve audit logs with optional filters.
    Requires a user with TI or Administrator role.
    """

    # We delegate the method selection logic to the use case.
    if user_id:
        logs = audit_use_cases.get_logs_by_user(user_id, skip, limit)
    elif action:
        logs = audit_use_cases.get_logs_by_action(action, skip, limit)
    elif start_date and end_date:
        logs = audit_use_cases.get_logs_by_date_range(start_date, end_date, skip, limit)
    else:
        logs = audit_use_cases.get_all_logs(skip, limit)

    # If there are no logs, we return 404 for clarity.
    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audit logs found with the given filters.",
        )

    # Ideally, user “enrichment” should be done in the use case.
    # But if we keep it here, at least we simplify it:
    enriched_logs = audit_use_cases.enrich_logs_with_user_data(logs)
    return enriched_logs


@router.get("/logs/user/{user_id}", response_model=List[AuditLogResponse])
async def get_user_audit_logs(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    audit_use_cases: AuditUseCases = Depends(get_audit_use_cases),
    current_user: User = Depends(require_ti_or_admin),
) -> List[AuditLogResponse]:
    """
    Retrieve audit logs for a specific user.
    """
    logs = audit_use_cases.get_logs_by_user(user_id, skip, limit)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this user.")
    return logs


@router.get("/logs/action/{action}", response_model=List[AuditLogResponse])
async def get_action_audit_logs(
    action: AuditAction,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    audit_use_cases: AuditUseCases = Depends(get_audit_use_cases),
    current_user: User = Depends(require_ti_or_admin),
) -> List[AuditLogResponse]:
    """
    Retrieve audit logs filtered by a specific action type.
    """
    logs = audit_use_cases.get_logs_by_action(action, skip, limit)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this action.")
    return logs
