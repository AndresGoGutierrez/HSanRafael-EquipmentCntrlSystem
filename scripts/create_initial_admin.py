"""
Script to create the initial administrator user.
Run this script after setting up the database.
"""

import sys
import traceback
from pathlib import Path

# Add parent directory to path for module imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.domain.entities.user import User, UserRole
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl


def create_admin_user() -> None:
    """Create the initial administrator user if it doesn't exist."""
    print("Starting admin user creation process...\n")

    try:
        with SessionLocal() as db:
            user_repository = UserRepositoryImpl(db)

            existing_admin = user_repository.get_by_username("admin")
            if existing_admin:
                print("Admin user already exists. No changes made.")
                return

            admin_user = User(
                username="admin",
                email="admin@hospitalsanrafael.com",
                full_name="Administrador del Sistema",
                role=UserRole.ADMINISTRADOR,
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
            )

            created_user = user_repository.create(admin_user)

            print("Admin user created successfully!")
            print(f"Username: {created_user.username}")
            print(f"Email: {created_user.email}")
            print(f"Role: {created_user.role.value}")
            print("\n Default password: 'Admin123!' — please change it immediately after first login.")

    except Exception as e:
        print("Error while creating admin user:")
        print(f"   {e}")
        traceback.print_exc()


if __name__ == "__main__":
    print("Creating initial administrator user...")
    create_admin_user()
