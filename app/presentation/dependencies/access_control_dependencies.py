from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.repositories.access_record_repository_impl import (
    AccessRecordRepositoryImpl,
)
from app.infrastructure.repositories.equipment_repository_impl import (
    EquipmentRepositoryImpl,
)
from app.application.use_cases.access_control_use_cases import AccessControlUseCases


# Repository dependencies


def get_access_record_repository(
    db: Session = Depends(get_db),
) -> AccessRecordRepositoryImpl:
    """
    Provide an instance of AccessRecordRepository.
    """
    return AccessRecordRepositoryImpl(db)


def get_equipment_repository(db: Session = Depends(get_db)) -> EquipmentRepositoryImpl:
    """
    Provide an instance of EquipmentRepository.
    """
    return EquipmentRepositoryImpl(db)


# Use case dependencies
def get_access_control_use_cases(
    access_record_repository: AccessRecordRepositoryImpl = Depends(
        get_access_record_repository
    ),
    equipment_repository: EquipmentRepositoryImpl = Depends(get_equipment_repository),
) -> AccessControlUseCases:
    """
    Provide the AccessControlUseCases service with its dependencies injected.
    """
    return AccessControlUseCases(access_record_repository, equipment_repository)
