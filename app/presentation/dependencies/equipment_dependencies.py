from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.repositories.equipment_repository_impl import (
    EquipmentRepositoryImpl,
)
from app.infrastructure.services.qr_service import QRCodeService
from app.infrastructure.services.storage_service import StorageService
from app.application.use_cases.equipment_use_cases import EquipmentUseCases


# --- Repository dependencies ---


def get_equipment_repository(db: Session = Depends(get_db)) -> EquipmentRepositoryImpl:
    """
    Dependency provider for the equipment repository.

    This creates an instance of the EquipmentRepositoryImpl
    with the current SQLAlchemy database session.
    """
    return EquipmentRepositoryImpl(db)


# --- Service dependencies ---


def get_qr_service() -> QRCodeService:
    """
    Dependency provider for the QR code generation service.
    """
    return QRCodeService()


def get_storage_service() -> StorageService:
    """
    Dependency provider for the storage service.
    """
    return StorageService()


# --- Use case dependencies ---


def get_equipment_use_cases(
    equipment_repository: EquipmentRepositoryImpl = Depends(get_equipment_repository),
    qr_service: QRCodeService = Depends(get_qr_service),
    storage_service: StorageService = Depends(get_storage_service),
) -> EquipmentUseCases:
    """
    Dependency provider for the equipment use cases.

    Combines the repository and service dependencies to
    instantiate the EquipmentUseCases class.
    """
    return EquipmentUseCases(
        equipment_repository=equipment_repository,
        qr_service=qr_service,
        storage_service=storage_service,
    )
