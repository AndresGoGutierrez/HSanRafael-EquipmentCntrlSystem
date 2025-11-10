"""
Unit tests for Authentication use cases
"""
import unittest
from unittest.mock import Mock
from fastapi import HTTPException
from app.domain.entities.user import User, UserRole
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.core.security import get_password_hash


def build_test_user(**overrides) -> User:
    """Factory helper to build test user with default fields."""
    defaults = {
        "id": overrides.get("id", 1),
        "username": overrides.get("username", "testuser"),
        "email": overrides.get("email", "test@example.com"),
        "full_name": overrides.get("full_name", "Test User"),
        "role": overrides.get("role", UserRole.TI),
        "hashed_password": overrides.get("hashed_password", get_password_hash("password123")),
        "is_active": overrides.get("is_active", True),
    }
    return User(**defaults)


class TestAuthUseCases(unittest.TestCase):
    """Test authentication use cases"""

    def setUp(self):
        self.mock_user_repository = Mock()
        self.auth_use_cases = AuthUseCases(self.mock_user_repository)
        self.test_user = build_test_user()

    # -----------------------------
    # Authentication tests
    # -----------------------------
    def test_authenticate_user_success(self):
        """User exists and correct password → authentication success"""
        self.mock_user_repository.get_by_username.return_value = self.test_user

        result = self.auth_use_cases.authenticate_user("testuser", "password123")

        self.assertIsNotNone(result)
        self.assertEqual(result.username, "testuser")
        self.mock_user_repository.get_by_username.assert_called_once_with("testuser")

    def test_authenticate_user_wrong_password(self):
        """Incorrect password → authentication fails"""
        self.mock_user_repository.get_by_username.return_value = self.test_user

        result = self.auth_use_cases.authenticate_user("testuser", "wrongpassword")

        self.assertIsNone(result)

    def test_authenticate_user_not_found(self):
        """Username does not exist → authentication fails"""
        self.mock_user_repository.get_by_username.return_value = None

        result = self.auth_use_cases.authenticate_user("nonexistent", "password123")

        self.assertIsNone(result)

    def test_authenticate_inactive_user(self):
        """Inactive users cannot be authenticated"""
        inactive_user = build_test_user(id=2, username="inactive", is_active=False)
        self.mock_user_repository.get_by_username.return_value = inactive_user

        result = self.auth_use_cases.authenticate_user("inactive", "password123")

        self.assertIsNone(result)

    # -----------------------------
    # Token generation test
    # -----------------------------
    def test_create_user_token(self):
        """Ensure generated JWT token string is returned"""
        token = self.auth_use_cases.create_user_token(self.test_user)

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)

    # -----------------------------
    # Registration tests
    # -----------------------------
    def test_register_user_success(self):
        """New user registration should be successful"""
        self.mock_user_repository.get_by_username.return_value = None
        self.mock_user_repository.get_by_email.return_value = None
        self.mock_user_repository.create.return_value = self.test_user

        result = self.auth_use_cases.register_user(
            username="newuser",
            email="newuser@example.com",
            full_name="New User",
            password="password123",
            role=UserRole.SEGURIDAD,
        )

        self.assertIsNotNone(result)
        self.mock_user_repository.create.assert_called_once()

    def test_register_user_duplicate_username(self):
        """User registration fails when username already exists"""
        self.mock_user_repository.get_by_username.return_value = self.test_user

        with self.assertRaises(HTTPException) as context:
            self.auth_use_cases.register_user(
                username="testuser",
                email="another@example.com",
                full_name="Another User",
                password="password123",
                role=UserRole.SEGURIDAD,
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Username is already registered.", context.exception.detail)

    def test_register_user_duplicate_email(self):
        """User registration fails when email already exists"""
        self.mock_user_repository.get_by_username.return_value = None
        self.mock_user_repository.get_by_email.return_value = self.test_user

        with self.assertRaises(HTTPException) as context:
            self.auth_use_cases.register_user(
                username="newuser",
                email="test@example.com",
                full_name="New User",
                password="password123",
                role=UserRole.SEGURIDAD,
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Email is already registered.", context.exception.detail)

    # -----------------------------
    # Change password tests
    # -----------------------------
    def test_change_password_success(self):
        """Password change succeeds when current password is correct"""
        self.mock_user_repository.update.return_value = self.test_user

        result = self.auth_use_cases.change_password(
            self.test_user, "password123", "newpassword456"
        )

        self.assertIsNotNone(result)
        self.mock_user_repository.update.assert_called_once()

    def test_change_password_wrong_current(self):
        """Password change fails with incorrect current password"""
        with self.assertRaises(HTTPException) as context:
            self.auth_use_cases.change_password(
                self.test_user, "wrongpassword", "newpassword456"
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Current password is incorrect", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
