from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """SQLAlchemy implementation of the UserRepository interface."""

    def __init__(self, db: Session):
        self.db = db

    # Mappers

    def _to_entity(self, model: UserModel) -> User:
        """Convert ORM model to domain entity."""
        if not model:
            return None
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            full_name=model.full_name,
            role=model.role,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to ORM model."""
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            full_name=entity.full_name,
            role=entity.role,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    # CRUD Operations

    def create(self, user: User) -> User:
        """Create and persist a new user."""
        try:
            db_user = self._to_model(user)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_entity(db_user)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user)

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by username."""
        db_user = (
            self.db.query(UserModel).filter(UserModel.username == username).first()
        )
        return self._to_entity(db_user)

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email."""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve a paginated list of all users."""
        db_users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_entity(user) for user in db_users]

    def update(self, user: User) -> Optional[User]:
        """Update an existing user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            return None

        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.role = user.role
        db_user.hashed_password = user.hashed_password
        db_user.is_active = user.is_active

        try:
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_entity(db_user)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        try:
            self.db.delete(db_user)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise
