from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.domain.entities.access_record import AccessType, AccessStatus


class AccessRecordModel(Base):
    """Access record database model"""

    __tablename__ = "access_records"
    __table_args__ = {"comment": "Stores access logs of equipment by users"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    access_type: Mapped[AccessType] = mapped_column(
        SQLEnum(AccessType, name="access_type_enum"), nullable=False
    )
    status: Mapped[AccessStatus] = mapped_column(
        SQLEnum(AccessStatus, name="access_status_enum"), nullable=False
    )

    entry_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expected_exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # Relationships
    equipment = relationship(
        "EquipmentModel",
        back_populates="access_records",
        lazy="joined",
    )
    user = relationship(
        "UserModel",
        back_populates="access_records",
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Readable representation for debugging."""
        return (
            f"<AccessRecordModel(id={self.id}, type={self.access_type.value}, "
            f"status={self.status.value}, user_id={self.user_id}, equipment_id={self.equipment_id})>"
        )
