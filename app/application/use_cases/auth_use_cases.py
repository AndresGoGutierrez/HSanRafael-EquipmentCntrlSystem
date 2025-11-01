from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status

from app.domain.entities.user import User, UserRole
from app.domain.ports.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class AuthUseCases:
    """Application service for handling user authentication and registration logic."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    # === AUTHENTICATION ===
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Verify user credentials and return user if authentication succeeds.

        Args:
            username: User's username.
            password: User's plain password.

        Returns:
            User instance if valid credentials, otherwise None.
        """
        user = self._user_repository.get_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    # === TOKEN CREATION ===
    def create_user_token(self, user: User) -> str:
        """
        Create a JWT access token for the given user.

        Args:
            user: Authenticated user entity.

        Returns:
            Encoded JWT token as string.
        """
        try:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        except AttributeError:
            # Fallback in case config is missing the setting
            expires_delta = timedelta(minutes=30)

        payload = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
        }

        return create_access_token(data=payload, expires_delta=expires_delta)

    # === USER REGISTRATION ===
    def register_user(
        self,
        username: str,
        email: str,
        full_name: str,
        password: str,
        role: UserRole,
    ) -> User:
        """
        Register a new user after validating unique username and email.

        Args:
            username: Unique username.
            email: User email.
            full_name: Full name.
            password: Plain password to hash.
            role: Role of the new user.

        Returns:
            Created user entity.
        """
        if self._user_repository.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already registered.",
            )

        if self._user_repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered.",
            )

        hashed_password = get_password_hash(password)
        new_user = User(
            id=None,
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            hashed_password=hashed_password,
            is_active=True,
        )

        return self._user_repository.create(new_user)

    # === PASSWORD MANAGEMENT ===
    def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> User:
        """
        Change the user's password after verifying the current one.

        Args:
            user: User entity.
            current_password: Current password in plain text.
            new_password: New password in plain text.

        Returns:
            Updated user entity.
        """
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )

        if verify_password(new_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password cannot be the same as the current one.",
            )

        user.hashed_password = get_password_hash(new_password)
        return self._user_repository.update(user)
