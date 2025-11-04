from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from app.domain.entities.audit_log import AuditAction


# Response Schema


class AuditLogResponse(BaseModel):
    """Schema representing an audit log entry returned by the API."""

    id: int = Field(..., description="Unique identifier for the audit log record.")
    user_id: Optional[int] = Field(
        None, description="ID of the user who performed the action."
    )
    action: AuditAction = Field(
        ..., description="Type of action performed (CREATE, UPDATE, DELETE, etc.)."
    )
    entity_type: str = Field(
        ...,
        description="Type of entity affected by the action (e.g., 'Equipment', 'User').",
    )
    entity_id: Optional[int] = Field(
        None, description="ID of the affected entity, if applicable."
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional contextual details about the action (e.g., changed fields, old/new values).",
        examples=[{"field": "name", "old": "OldName", "new": "NewName"}],
    )
    ip_address: Optional[str] = Field(
        None,
        description="IP address from which the action was performed.",
        examples=["192.168.1.10"],
    )
    user_agent: Optional[str] = Field(
        None,
        description="User agent string of the client making the request.",
        examples=["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"],
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the audit record was created."
    )

    model_config = ConfigDict(from_attributes=True)


# Extended Schema (with user info)


class AuditLogWithUser(AuditLogResponse):
    """Schema extending audit logs with user information."""

    user_username: Optional[str] = Field(
        None,
        description="Username of the user associated with the action.",
        examples=["jdoe"],
    )
    user_full_name: Optional[str] = Field(
        None,
        description="Full name of the user associated with the action.",
        examples=["John Doe"],
    )


# Filter Schema


class AuditLogFilter(BaseModel):
    """Schema for filtering and querying audit logs."""

    user_id: Optional[int] = Field(
        None, description="Filter by the ID of the user who performed the action."
    )
    action: Optional[AuditAction] = Field(
        None, description="Filter by action type (CREATE, UPDATE, DELETE, etc.)."
    )
    entity_type: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Filter by the affected entity type (e.g., 'Equipment', 'AccessRecord').",
        examples=["Equipment"],
    )
    start_date: Optional[datetime] = Field(
        None,
        description="Start of the date range to filter audit logs.",
        examples=["2025-01-01T00:00:00Z"],
    )
    end_date: Optional[datetime] = Field(
        None,
        description="End of the date range to filter audit logs.",
        examples=["2025-12-31T23:59:59Z"],
    )
