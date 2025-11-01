from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.entities.access_record import AccessType, AccessStatus


# Base Schema


class AccessRecordBase(BaseModel):
    """Base schema for access records."""

    equipment_id: int = Field(
        ..., description="Unique ID of the equipment involved in the access record."
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional notes or observations about the access record.",
        examples=["Equipment entered for maintenance."],
    )


# Create & Exit Schemas


class AccessRecordCreate(BaseModel):
    """Schema for creating a new equipment entry record."""

    equipment_identifier: str = Field(
        ...,
        description="QR code or serial number used to identify the equipment.",
        examples=["EQP-1234-QR", "SN-998877"],
    )
    notes: Optional[str] = Field(
        None, max_length=500, description="Optional notes describing the entry context."
    )


class AccessRecordExit(BaseModel):
    """Schema for registering an equipment exit record."""

    equipment_identifier: str = Field(
        ...,
        description="QR code or serial number of the exiting equipment.",
        examples=["EQP-1234-QR", "SN-998877"],
    )
    notes: Optional[str] = Field(
        None, max_length=500, description="Optional notes describing the exit context."
    )


# Response Schemas


class AccessRecordResponse(BaseModel):
    """Schema for representing an access record in responses."""

    id: int = Field(..., description="Unique identifier of the access record.")
    equipment_id: int = Field(..., description="ID of the associated equipment.")
    user_id: int = Field(
        ..., description="ID of the user who performed the access action."
    )
    access_type: AccessType = Field(..., description="Type of access (ENTRY or EXIT).")
    status: AccessStatus = Field(
        ..., description="Current status of the access record."
    )
    entry_time: Optional[datetime] = Field(
        None, description="Timestamp when the equipment entered."
    )
    exit_time: Optional[datetime] = Field(
        None, description="Timestamp when the equipment exited."
    )
    expected_exit_time: Optional[datetime] = Field(
        None, description="Expected time the equipment should exit."
    )
    notes: Optional[str] = Field(
        None, max_length=500, description="Additional notes or remarks."
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the record was created."
    )

    model_config = ConfigDict(from_attributes=True)


class AccessRecordWithDetails(AccessRecordResponse):
    """Schema extending access record with equipment and user details."""

    equipment_name: str = Field(..., description="Name of the equipment.")
    equipment_qr_code: Optional[str] = Field(
        None, description="QR code assigned to the equipment."
    )
    equipment_serial_number: Optional[str] = Field(
        None, description="Serial number of the equipment."
    )
    user_username: str = Field(
        ..., description="Username of the user who handled the equipment."
    )
    user_full_name: str = Field(..., description="Full name of the responsible user.")
    is_expired: bool = Field(
        False,
        description="Indicates if the equipment's expected exit time has expired.",
    )


# Active Equipment Schema


class ActiveEquipmentResponse(BaseModel):
    """Schema for listing equipment currently inside the hospital."""

    access_record_id: int = Field(..., description="Associated access record ID.")
    equipment_id: int = Field(..., description="Unique ID of the equipment.")
    equipment_name: str = Field(..., description="Name of the equipment.")
    equipment_qr_code: Optional[str] = Field(
        None, description="QR code of the equipment."
    )
    equipment_serial_number: Optional[str] = Field(
        None, description="Serial number of the equipment."
    )
    entry_time: datetime = Field(
        ..., description="Timestamp when the equipment entered."
    )
    expected_exit_time: datetime = Field(
        ..., description="Expected timestamp for the equipment exit."
    )
    user_full_name: str = Field(..., description="Full name of the responsible user.")
    days_inside: int = Field(
        ..., ge=0, description="Number of days the equipment has been inside."
    )
    is_expired: bool = Field(
        ..., description="True if the expected exit time has already passed."
    )
    status: AccessStatus = Field(
        ..., description="Current access status (ACTIVE, EXITED, EXPIRED, etc.)."
    )
