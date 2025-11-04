from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    """User roles in the system"""

    SEGURIDAD = "seguridad"
    TI = "ti"
    ADMINISTRADOR = "administrador"

    def __srt__(self) -> str:
        return self.value


class User:
    """User domain entity"""

    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        email: str = "",
        full_name: str = "",
        role: UserRole = UserRole.ADMINISTRADOR,
        hashed_password: str = "",
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.username = username.strip()
        self.email = email.strip().lower()
        self.full_name = full_name.strip()
        self.role = role
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def has_permission(self, required_role: UserRole) -> bool:
        """Check if the user has the required role or higher"""

        role_hierarchy = {
            UserRole.ADMINISTRADOR: 3,
            UserRole.TI: 2,
            UserRole.SEGUIDAD: 1,
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', role='{self.role}')>"
