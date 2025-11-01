from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.entities.equipment import EquipmentType, EquipmentCategory


# Base Schema


class EquipmentBase(BaseModel):
    """Base schema containing common equipment attributes."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the equipment (e.g., 'ECG Monitor').",
        examples=["Ultrasound Scanner"],
    )
    equipment_type: EquipmentType = Field(
        ..., description="Type of the equipment, based on functional classification."
    )
    category: EquipmentCategory = Field(
        ...,
        description="Category the equipment belongs to (e.g., diagnostic, surgical).",
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional description or details about the equipment.",
        examples=["Used for cardiac monitoring in ICU."],
    )


# Create Schema


class EquipmentCreate(EquipmentBase):
    """Schema used when creating new equipment records."""

    serial_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Unique serial number of the equipment, if available.",
        examples=["SN-AX45-2025"],
    )


# Update Schema


class EquipmentUpdate(BaseModel):
    """Schema for updating existing equipment information."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Updated name of the equipment."
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Updated description of the equipment."
    )
    is_active: Optional[bool] = Field(
        None, description="Set to False to deactivate the equipment."
    )


# Response Schema


class EquipmentResponse(EquipmentBase):
    """Schema returned in equipment API responses."""

    id: int = Field(..., description="Unique identifier of the equipment.")
    serial_number: Optional[str] = Field(None, description="Equipment serial number.")
    qr_code: Optional[str] = Field(
        None, description="QR code string for quick identification."
    )
    image_url: Optional[str] = Field(
        None, description="URL of the stored equipment image."
    )
    is_active: bool = Field(
        ..., description="Indicates whether the equipment is active."
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the equipment was created."
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the equipment was last updated."
    )

    model_config = ConfigDict(from_attributes=True)


# Extended Schema (with QR Image)


class EquipmentWithQR(EquipmentResponse):
    """Schema for equipment responses that include a Base64-encoded QR image."""

    qr_code_image: Optional[str] = Field(
        None,
        description="Base64-encoded QR image representing the equipment.",
        examples=["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."],
    )


# Search Schema


class EquipmentSearch(BaseModel):
    """Schema used for searching and filtering equipment."""

    query: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Search query for matching equipment name, serial number, or QR code.",
        examples=["monitor"],
    )
    equipment_type: Optional[EquipmentType] = Field(
        None, description="Filter by specific equipment type."
    )
    category: Optional[EquipmentCategory] = Field(
        None, description="Filter by equipment category."
    )
    is_active: Optional[bool] = Field(
        True, description="Filter by active/inactive status. Defaults to True."
    )
