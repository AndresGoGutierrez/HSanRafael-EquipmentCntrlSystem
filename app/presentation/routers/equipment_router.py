from typing import List, Optional
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Query
from app.application.use_cases.equipment_use_cases import EquipmentUseCases
from app.presentation.schemas.equipment_schema import (
    EquipmentResponse,
    EquipmentWithQR,
)
from app.presentation.dependencies.equipment_dependencies import get_equipment_use_cases
from app.presentation.dependencies.auth_dependencies import (
    require_ti_or_admin,
    require_any_role,
)
from app.domain.entities.user import User
from app.domain.entities.equipment import EquipmentType, EquipmentCategory

router = APIRouter(prefix="/equipment", tags=["Equipment"])


# CREATE EQUIPMENT


@router.post(
    "/",
    response_model=EquipmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new equipment (TI or Admin only)",
)
async def create_equipment(
    name: str = Form(..., description="Equipment name"),
    equipment_type: EquipmentType = Form(..., description="frecuente or no_frecuente"),
    category: EquipmentCategory = Form(..., description="tecnologico or biomedico"),
    description: Optional[str] = Form(None, description="Optional description"),
    serial_number: Optional[str] = Form(
        None, description="Serial number (required for no_frecuente)"
    ),
    image: UploadFile = File(
        None, description="Photo file (required for biomedico)"
    ),
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """
    Create a new equipment item.

    - **name**: Equipment name
    - **equipment_type**: frecuente or no_frecuente
    - **category**: tecnologico or biomedico
    - **description**: Optional text description
    - **serial_number**: Required for non-frequent equipment
    - **image**: Required for biomedico category
    """
    return equipment_use_cases.create_equipment(
        name=name,
        equipment_type=equipment_type,
        category=category,
        description=description,
        serial_number=serial_number,
        image_file=image,
    )


# GET EQUIPMENT


@router.get(
    "/",
    response_model=List[EquipmentResponse],
    summary="Get all equipment with filters",
)
async def get_all_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    equipment_type: Optional[EquipmentType] = Query(None, description="Filter by type"),
    category: Optional[EquipmentCategory] = Query(
        None, description="Filter by category"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_any_role),
):
    """Retrieve all equipment with optional filters."""
    return equipment_use_cases.get_all_equipment(
        skip=skip,
        limit=limit,
        equipment_type=equipment_type,
        category=category,
        is_active=is_active,
    )


@router.get(
    "/{equipment_id}", response_model=EquipmentResponse, summary="Get equipment by ID"
)
async def get_equipment_by_id(
    equipment_id: int,
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_any_role),
):
    """Retrieve equipment by its ID."""
    return equipment_use_cases.get_equipment_by_id(equipment_id)


@router.get(
    "/{equipment_id}/qr",
    response_model=EquipmentWithQR,
    summary="Get equipment with QR code (base64)",
)
async def get_equipment_with_qr(
    equipment_id: int,
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_any_role),
):
    """
    Retrieve equipment details including a base64-encoded QR code image.
    """
    equipment = equipment_use_cases.get_equipment_by_id(equipment_id)
    qr_image = equipment_use_cases.generate_qr_code_image(equipment_id)
    return {**equipment.__dict__, "qr_code_image": qr_image}


@router.get(
    "/qr/{qr_code}",
    response_model=EquipmentResponse,
    summary="Get equipment by QR code",
)
async def get_equipment_by_qr(
    qr_code: str,
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_any_role),
):
    """Retrieve equipment using its QR code."""
    return equipment_use_cases.get_equipment_by_qr(qr_code)


@router.get(
    "/serial/{serial_number}",
    response_model=EquipmentResponse,
    summary="Get equipment by serial number",
)
async def get_equipment_by_serial(
    serial_number: str,
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_any_role),
):
    """Retrieve equipment using its serial number."""
    return equipment_use_cases.get_equipment_by_serial(serial_number)


# UPDATE / DELETE EQUIPMENT


@router.put(
    "/{equipment_id}",
    response_model=EquipmentResponse,
    summary="Update equipment (TI or Admin only)",
)
async def update_equipment(
    equipment_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """Update existing equipment details."""
    return equipment_use_cases.update_equipment(
        equipment_id=equipment_id,
        name=name,
        description=description,
        is_active=is_active,
        image_file=image,
    )


@router.delete(
    "/{equipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete equipment (TI or Admin only)",
)
async def delete_equipment(
    equipment_id: int,
    equipment_use_cases: EquipmentUseCases = Depends(get_equipment_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """Delete equipment by ID."""
    equipment_use_cases.delete_equipment(equipment_id)
    return None
