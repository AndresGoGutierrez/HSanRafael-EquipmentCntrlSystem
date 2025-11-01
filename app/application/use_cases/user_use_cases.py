from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.entities.user import User, UserRole
from app.domain.ports.user_repository import UserRepository
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


class UserUseCases:
    """
    Application service (Use Case Layer) responsible for managing user operations.

    This class encapsulates the business logic for user-related actions,
    coordinating between repositories and domain entities while enforcing
    application-level rules and validations.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the use case with the required repository.

        Args:
            user_repository (UserRepository): Repository interface for User persistence.
        """
        self.user_repository = user_repository

    # User Retrieval

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by their unique ID.

        Args:
            user_id (int): The ID of the user.

        Raises:
            HTTPException: If the user is not found.

        Returns:
            User: The corresponding User entity.
        """
        logger.debug(f"Fetching user with ID={user_id}")
        user = self.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User with ID={user_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID={user_id} not found.",
            )
        return user

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieve all users with optional pagination.

        Args:
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to retrieve.

        Returns:
            List[User]: A list of User entities.
        """
        logger.debug(f"Retrieving all users (skip={skip}, limit={limit})")
        users = self.user_repository.get_all(skip=skip, limit=limit)
        logger.info(f"Retrieved {len(users)} users.")
        return users

    # User Update

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
    ) -> User:
        """
        Update user information and persist the changes.

        Args:
            user_id (int): User ID to update.
            email (Optional[str]): New email address.
            full_name (Optional[str]): Updated full name.
            role (Optional[UserRole]): Updated role.
            is_active (Optional[bool]): Updated activation status.

        Raises:
            HTTPException: If email is already in use or user not found.

        Returns:
            User: Updated User entity.
        """
        user = self.get_user_by_id(user_id)
        logger.debug(f"Updating user ID={user_id}")

        if email:
            existing_user = self.user_repository.get_by_email(email)
            if existing_user and existing_user.id != user_id:
                logger.error(f"Email '{email}' already registered by another user.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered by another user.",
                )
            user.email = email

        if full_name:
            user.full_name = full_name

        if role:
            user.role = role

        if is_active is not None:
            user.is_active = is_active

        updated_user = self.user_repository.update(user)
        logger.info(f"User ID={user_id} updated successfully.")
        return updated_user

    # User Deletion

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id (int): ID of the user to delete.

        Raises:
            HTTPException: If the user does not exist.

        Returns:
            bool: True if deletion was successful.
        """
        user = self.get_user_by_id(user_id)
        logger.debug(f"Deleting user ID={user.id}")
        result = self.user_repository.delete(user.id)

        if not result:
            logger.error(f"Failed to delete user ID={user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user.",
            )

        logger.info(f"User ID={user_id} deleted successfully.")
        return True
