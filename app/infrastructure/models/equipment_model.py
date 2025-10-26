from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.domain.entities.equipment import EquipmentType, EquipmentCategory


class EquipmentModel(Base):
    """Model for equipment items in the inventory"""

    __tablename__ = "equipment"
    __table_args__ = {"comment": "Stores equipment items in the inventory"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    equipment_type: Mapped[EquipmentType] = mapped_column(
        SQLEnum(EquipmentType, name="equipment_type_enum"),
        nullable=False,
    )
    category: Mapped[EquipmentCategory] = mapped_column(
        SQLEnum(EquipmentCategory, name="equipment_category_enum"),
        nullable=False,
    )
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    qr_code: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    image_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    access_records = relationship(
        "AccessRecordModel",
        back_populates="equipment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Representation of the EquipmentModel"""
        return (
            f"<EquipmentModel(id={self.id}, name='{self.name}', "
            f"type='{self.equipment_type.value}', active={self.is_active})>"
        )
