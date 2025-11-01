from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.repositories.audit_log_repository_impl import (
    AuditLogRepositoryImpl,
)
from app.application.use_cases.audit_use_cases import AuditUseCases
from app.application.use_cases.report_use_cases import ReportUseCases


# Repository dependencies


def get_audit_log_repository(db: Session = Depends(get_db)) -> AuditLogRepositoryImpl:
    """
    Provide an instance of the AuditLogRepository implementation.
    """
    return AuditLogRepositoryImpl(db)


# Use case dependencies


def get_audit_use_cases(
    audit_log_repository: AuditLogRepositoryImpl = Depends(get_audit_log_repository),
) -> AuditUseCases:
    """
    Provide the AuditUseCases service with injected dependencies.
    """
    return AuditUseCases(audit_log_repository)


def get_report_use_cases(
    db: Session = Depends(get_db),
) -> ReportUseCases:
    """
    Provide the ReportUseCases service.
    """
    return ReportUseCases(db)
