from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from app.domain.entities.audit_log import AuditAction


class AuditLogModel(Base):
    """Audit Log database model"""

    __tablename__ = "audit_logs"
    __tableargs__ = {"comment": "Stores audit Log entries for system actions"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # Relationships
    user = relationship("UserModel", back_populates="audit_logs")

    def __repr__(self) -> str:
        """Representation of the AuditLogModel"""
        return (
            f"<AuditLogModel id={self.id} action={self.action.value} "
            f"user_id={self.user_id} entity_type={self.entity_type} entity_id={self.entity_id}>"
        )
