from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.domain.entities.user import User, UserRole
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Dependencies for repositories


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Provide an instance of the UserRepository implementation."""
    return UserRepositoryImpl(db)


# Authentication dependencies


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
) -> User:
    """
    Extract and validate the current authenticated user from the JWT token.
    Raises HTTP 401 if invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except JWTError:
        # Handles token decode or signature validation errors
        raise credentials_exception

    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    user_id: int = payload.get("user_id")

    if not username or not user_id:
        raise credentials_exception

    user = user_repository.get_by_id(user_id)
    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive."
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure the authenticated user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user account."
        )
    return current_user


# Role-based access control


class RoleChecker:
    """
    Dependency class that ensures the current user has one of the allowed roles.

    Usage:
        @router.get("/admin")
        async def admin_only_route(current_user: User = Depends(require_admin)):
            ...
    """

    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """Raise 403 if the user's role is not permitted."""
        if current_user.role not in self.allowed_roles:
            allowed_roles_str = ", ".join(role.value for role in self.allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles_str}",
            )
        return current_user


# Predefined role-based dependencies

require_admin = RoleChecker([UserRole.ADMINISTRADOR])
require_ti_or_admin = RoleChecker([UserRole.TI, UserRole.ADMINISTRADOR])
require_any_role = RoleChecker(
    [UserRole.SEGURIDAD, UserRole.TI, UserRole.ADMINISTRADOR]
)
