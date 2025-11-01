from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User


class UserRepository(ABC):
    """ Port interface for User repository operations.
    
    This abstract base class defines the contract for user persistence and retrieval.
    Concrete implementations (e.g., SQLAlchemy, MongoDB, etc.) must adhere to this interface.
    """

    # ───────────────────────────────────────────────
    # CRUD OPERATIONS
    # ───────────────────────────────────────────────

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user in the data source.
        
        Args:
            user: User domain entity to persist.
        
        Returns:
            User: The created user with its assigned ID.
        """
        raise NotImplementedError("UserRepository.create() must be implemented by subclass.")

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by its unique ID.
        
        Args:
            user_id: The database ID of the user.
        
        Returns:
            User or None: The user entity if found, otherwise None.
        """
        raise NotImplementedError("UserRepository.get_by_id() must be implemented by subclass.")

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username.
        
        Args:
            username: The username to search for.
        
        Returns:
            User or None: The corresponding user entity, if found.
        """
        raise NotImplementedError("UserRepository.get_by_username() must be implemented by subclass.")

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.
        
        Args:
            email: The user's email to search for.
        
        Returns:
            User or None: The user entity if found.
        """
        raise NotImplementedError("UserRepository.get_by_email() must be implemented by subclass.")

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve a list of users with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of users to return.
        
        Returns:
            List[User]: A list of user entities.
        """
        raise NotImplementedError("UserRepository.get_all() must be implemented by subclass.")

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user.
        
        Args:
            user: The user entity with updated fields.
        
        Returns:
            User: The updated user entity.
        """
        raise NotImplementedError("UserRepository.update() must be implemented by subclass.")

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        Args:
            user_id: The ID of the user to delete.
        
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        raise NotImplementedError("UserRepository.delete() must be implemented by subclass.")
