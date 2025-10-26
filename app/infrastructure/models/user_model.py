from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.domain.entities.user import UserRole


class UserModel(Base):
    """Model for registered system users"""

    __tablename__ = "users"
    __table_args__ = {"comment": "Stores registered system users"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role_enum"), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    access_records = relationship(
        "AccessRecordModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    audit_logs = relationship(
        "AuditLogModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """Representation of the UserModel"""
        return (
            f"<UserModel(id={self.id}, username='{self.username}', email='{self.email}', "
            f"role='{self.role.value}', active={self.is_active})>"
        )
