from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.entities.access_record import AccessStatus

# Report Filters


class ReportFilter(BaseModel):
    """Schema defining filters for generating reports."""

    start_date: datetime = Field(
        ...,
        description="Start date of the report period.",
        examples=["2025-01-01T00:00:00Z"],
    )
    end_date: datetime = Field(
        ...,
        description="End date of the report period.",
        examples=["2025-01-31T23:59:59Z"],
    )
    equipment_type: Optional[str] = Field(
        None, description="Filter by equipment type (e.g., monitor, ventilator)."
    )
    category: Optional[str] = Field(
        None, description="Filter by equipment category (e.g., diagnostic, surgical)."
    )
    user_id: Optional[int] = Field(
        None, description="Filter by user ID related to the access record."
    )


# Equipment Report Item


class EquipmentReportItem(BaseModel):
    """Schema representing a summarized equipment report entry."""

    equipment_id: int = Field(..., description="Unique equipment ID.")
    equipment_name: str = Field(..., description="Name of the equipment.")
    equipment_type: str = Field(
        ..., description="Type or classification of the equipment."
    )
    category: str = Field(..., description="Category the equipment belongs to.")
    qr_code: Optional[str] = Field(
        None, description="QR code assigned to the equipment."
    )
    serial_number: Optional[str] = Field(None, description="Equipment serial number.")
    entry_count: int = Field(..., ge=0, description="Total number of entry records.")
    exit_count: int = Field(..., ge=0, description="Total number of exit records.")
    total_days_inside: int = Field(
        ..., ge=0, description="Total number of days the equipment remained inside."
    )
    last_entry: Optional[datetime] = Field(
        None, description="Date and time of the last entry."
    )
    last_exit: Optional[datetime] = Field(
        None, description="Date and time of the last exit."
    )

    model_config = ConfigDict(from_attributes=True)


# Access Report Item


class AccessReportItem(BaseModel):
    """Schema representing an individual access record in a report."""

    record_id: int = Field(..., description="Unique ID of the access record.")
    equipment_name: str = Field(..., description="Name of the equipment involved.")
    equipment_qr_code: Optional[str] = Field(
        None, description="QR code of the equipment."
    )
    equipment_serial_number: Optional[str] = Field(
        None, description="Serial number of the equipment."
    )
    user_full_name: str = Field(
        ..., description="Full name of the user who performed the access."
    )
    entry_time: datetime = Field(..., description="Date and time of entry.")
    exit_time: Optional[datetime] = Field(
        None, description="Date and time of exit (if available)."
    )
    expected_exit_time: datetime = Field(
        ..., description="Expected exit time based on maximum allowed duration."
    )
    status: AccessStatus = Field(
        ..., description="Current access status (e.g., ACTIVE, EXPIRED)."
    )
    days_inside: int = Field(
        ..., ge=0, description="Number of days the equipment has been inside."
    )
    is_expired: bool = Field(
        ..., description="Indicates whether the equipment is currently expired."
    )

    model_config = ConfigDict(from_attributes=True)


# Report Summary


class ReportSummary(BaseModel):
    """Schema summarizing global report statistics for a given period."""

    total_entries: int = Field(
        ..., ge=0, description="Total number of equipment entries during the period."
    )
    total_exits: int = Field(
        ..., ge=0, description="Total number of equipment exits during the period."
    )
    currently_inside: int = Field(
        ..., ge=0, description="Number of equipment items currently inside."
    )
    expired_equipment: int = Field(
        ..., ge=0, description="Number of equipment items past their allowed stay time."
    )
    total_equipment: int = Field(
        ..., ge=0, description="Total number of equipment registered."
    )
    total_users: int = Field(
        ..., ge=0, description="Total number of users included in the report."
    )
    period_start: datetime = Field(
        ..., description="Start date of the reporting period."
    )
    period_end: datetime = Field(..., description="End date of the reporting period.")

    model_config = ConfigDict(from_attributes=True)
