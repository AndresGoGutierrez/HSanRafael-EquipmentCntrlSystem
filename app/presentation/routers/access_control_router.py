from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.user import User
from app.application.use_cases.access_control_use_cases import AccessControlUseCases
from app.presentation.schemas.access_record_schema import (
    AccessRecordCreate,
    AccessRecordExit,
    AccessRecordResponse,
    ActiveEquipmentResponse,
)
from app.presentation.dependencies.access_control_dependencies import get_access_control_use_cases
from app.presentation.dependencies.auth_dependencies import (
    get_current_active_user,
    require_admin,
)
from app.infrastructure.models.equipment_model import EquipmentModel
from app.infrastructure.models.user_model import  UserModel


router = APIRouter(prefix="/access", tags=["Access Control"])


# ---------------------------------------------------------------------------
#                             Entry registration
# ---------------------------------------------------------------------------

@router.post(
    "/entry",
    response_model=AccessRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_entry(
    entry_data: AccessRecordCreate,
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """
    Register equipment entry into the hospital.

    Automatically records:
    - Timestamp and registering user
    - Expected exit time based on max stay configuration
    """
    return access_control.register_entry(
        equipment_identifier=entry_data.equipment_identifier,
        user=current_user,
        notes=entry_data.notes,
    )


# ---------------------------------------------------------------------------
#                             Exit registration
# ---------------------------------------------------------------------------

@router.post("/exit", response_model=AccessRecordResponse)
async def register_exit(
    exit_data: AccessRecordExit,
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """
    Register equipment exit from the hospital.

    Validates:
    - Equipment has an active entry
    - User has permission
    """
    return access_control.register_exit(
        equipment_identifier=exit_data.equipment_identifier,
        user=current_user,
        notes=exit_data.notes,
    )


# ---------------------------------------------------------------------------
#                             Active equipment
# ---------------------------------------------------------------------------

@router.get("/active", response_model=List[ActiveEquipmentResponse])
async def get_active_equipment(
    db: Session = Depends(get_db),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve all equipment currently inside the hospital.
    Includes:
    - Equipment info
    - Entry & expected exit times
    - Days inside
    - Expiration status
    """
    active_records = access_control.get_active_equipment()

    responses = []
    for record in active_records:
        equipment = db.get(EquipmentModel, record.equipment_id)
        user = db.get(UserModel, record.user_id)

        if not equipment or not user:
            continue

        responses.append(
            ActiveEquipmentResponse(
                access_record_id=record.id,
                equipment_id=equipment.id,
                equipment_name=equipment.name,
                equipment_qr_code=equipment.qr_code,
                equipment_serial_number=equipment.serial_number,
                entry_time=record.entry_time,
                expected_exit_time=record.expected_exit_time,
                user_full_name=user.full_name,
                days_inside=(datetime.now(timezone.utc) - record.entry_time).days,
                is_expired=record.is_expired(),
                status=record.status,
            )
        )
    return responses


# ---------------------------------------------------------------------------
#                            Expired equipment
# ---------------------------------------------------------------------------

@router.get("/expired", response_model=List[ActiveEquipmentResponse])
async def get_expired_equipment(
    db: Session = Depends(get_db),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve all expired equipment (past expected stay).
    """
    expired_records = access_control.get_expired_equipment()

    responses = []
    for record in expired_records:
        equipment = db.get(EquipmentModel, record.equipment_id)
        user = db.get(UserModel, record.user_id)

        if not equipment or not user:
            continue

        responses.append(
            ActiveEquipmentResponse(
                access_record_id=record.id,
                equipment_id=equipment.id,
                equipment_name=equipment.name,
                equipment_qr_code=equipment.qr_code,
                equipment_serial_number=equipment.serial_number,
                entry_time=record.entry_time,
                expected_exit_time=record.expected_exit_time,
                user_full_name=user.full_name,
                days_inside=(datetime.now(timezone.utc) - record.entry_time).days,
                is_expired=True,
                status=record.status,
            )
        )
    return responses


# ---------------------------------------------------------------------------
#                             History by equipment
# ---------------------------------------------------------------------------

@router.get("/equipment/{equipment_id}/history", response_model=List[AccessRecordResponse])
async def get_equipment_history(
    equipment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve full access history for a specific equipment."""
    return access_control.get_equipment_history(equipment_id, skip, limit)


# ---------------------------------------------------------------------------
#                             History by user
# ---------------------------------------------------------------------------

@router.get("/user/{user_id}/history", response_model=List[AccessRecordResponse])
async def get_user_history(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all access records created by a specific user."""
    return access_control.get_user_history(user_id, skip, limit)


# ---------------------------------------------------------------------------
#                             Records by date range
# ---------------------------------------------------------------------------

@router.get("/date-range", response_model=List[AccessRecordResponse])
async def get_records_by_date_range(
    start_date: datetime = Query(..., description="Start date (ISO format)"),
    end_date: datetime = Query(..., description="End date (ISO format)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve access records within a specific date range."""
    return access_control.get_records_by_date_range(start_date, end_date, skip, limit)


# ---------------------------------------------------------------------------
#                             Forced exit (admin only)
# ---------------------------------------------------------------------------

@router.post("/force-exit/{record_id}", response_model=AccessRecordResponse)
async def force_exit(
    record_id: int,
    reason: str = Query(..., description="Reason for forced exit"),
    access_control: AccessControlUseCases = Depends(get_access_control_use_cases),
    current_user: User = Depends(require_admin),
):
    """
    Force equipment exit (Admin only).

    Used in emergency or exceptional situations where
    standard exit flow cannot be executed.
    """
    return access_control.force_exit(record_id, current_user, reason)
