"""
Unit tests for the Authentication use cases.

This module tests the business logic implemented in the `AuthUseCases` class,
covering authentication, registration, token generation, and password changes.

All external dependencies, such as the user repository, are mocked using
`unittest.mock.Mock` to ensure isolated and deterministic tests.

Framework: unittest (Python Standard Library)
"""

import unittest
from unittest.mock import Mock
from fastapi import HTTPException
from app.domain.entities.user import User, UserRole
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.core.security import get_password_hash


def build_test_user(**overrides) -> User:
    """
    Factory helper to build a test `User` entity with default values.

    This function provides a convenient way to create user instances for testing,
    while allowing specific fields to be overridden as needed.

    Args:
        **overrides: Key-value pairs to override default user attributes.

    Returns:
        User: A fully initialized user entity for testing.
    """
    """Factory helper to build test user with default fields."""
    defaults = {
        "id": overrides.get("id", 1),
        "username": overrides.get("username", "testuser"),
        "email": overrides.get("email", "test@example.com"),
        "full_name": overrides.get("full_name", "Test User"),
        "role": overrides.get("role", UserRole.TI),
        "hashed_password": overrides.get(
            "hashed_password", get_password_hash("password123")
        ),
        "is_active": overrides.get("is_active", True),
    }
    return User(**defaults)


class TestAuthUseCases(unittest.TestCase):
    """
    Unit tests for the `AuthUseCases` class.

    These tests validate core authentication workflows, including:
    - User login validation (authenticate_user)
    - JWT token creation (create_user_token)
    - User registration (register_user)
    - Password updates (change_password)

    All repository interactions are mocked to isolate business logic.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.

        Creates a mock user repository and initializes the `AuthUseCases`
        instance under test. Also prepares a reusable `test_user` entity.
        """
        self.mock_user_repository = Mock()
        self.auth_use_cases = AuthUseCases(self.mock_user_repository)
        self.test_user = build_test_user()

    # -----------------------------
    # Authentication tests
    # -----------------------------
    def test_authenticate_user_success(self):
        """
        Test successful user authentication.

        Scenario:
            - User exists in the repository.
            - Correct password is provided.

        Expected result:
            - Returns a valid `User` object.
            - Repository is queried exactly once.
        """
        """User exists and correct password → authentication success"""
        self.mock_user_repository.get_by_username.return_value = self.test_user

        result = self.auth_use_cases.authenticate_user("testuser", "password123")

        self.assertIsNotNone(result)
        self.assertEqual(result.username, "testuser")
        self.mock_user_repository.get_by_username.assert_called_once_with("testuser")

    def test_authenticate_user_wrong_password(self):
        """
        Test authentication failure when the provided password is incorrect.

        Expected result:
            - Returns None (authentication fails).
        """
        self.mock_user_repository.get_by_username.return_value = self.test_user

        result = self.auth_use_cases.authenticate_user("testuser", "wrongpassword")

        self.assertIsNone(result)

    def test_authenticate_user_not_found(self):
        """
        Test authentication failure when the user does not exist.

        Expected result:
            - Returns None (no user found in repository).
        """
        self.mock_user_repository.get_by_username.return_value = None

        result = self.auth_use_cases.authenticate_user("nonexistent", "password123")

        self.assertIsNone(result)

    def test_authenticate_inactive_user(self):
        """
        Test authentication prevention for inactive users.

        Expected result:
            - Returns None, even if credentials are correct.
        """
        inactive_user = build_test_user(id=2, username="inactive", is_active=False)
        self.mock_user_repository.get_by_username.return_value = inactive_user

        result = self.auth_use_cases.authenticate_user("inactive", "password123")

        self.assertIsNone(result)

    # -----------------------------
    # Token generation test
    # -----------------------------
    def test_create_user_token(self):
        """
        Test successful JWT token generation for a valid user.

        Expected result:
            - Returns a non-empty JWT token string.
            - Token length should be greater than 10 characters.
        """
        token = self.auth_use_cases.create_user_token(self.test_user)

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)

    # -----------------------------
    # Registration tests
    # -----------------------------
    def test_register_user_success(self):
        """
        Test successful registration of a new user.

        Scenario:
            - Username and email are unique.
            - Valid data is provided.

        Expected result:
            - User is created and returned.
            - Repository `create` method is called exactly once.
        """
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
        """
        Test failure when attempting to register a username that already exists.

        Expected result:
            - Raises HTTPException (status code 400).
            - Error message includes 'Username is already registered.'
        """
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
        """
        Test failure when attempting to register with an email already in use.

        Expected result:
            - Raises HTTPException (status code 400).
            - Error message includes 'Email is already registered.'
        """
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
        """
        Test successful password change when the current password is correct.

        Expected result:
            - Returns updated user entity.
            - Repository `update` method is called once.
        """
        self.mock_user_repository.update.return_value = self.test_user

        result = self.auth_use_cases.change_password(
            self.test_user, "password123", "newpassword456"
        )

        self.assertIsNotNone(result)
        self.mock_user_repository.update.assert_called_once()

    def test_change_password_wrong_current(self):
        """
        Test failure when attempting to change the password with an incorrect current password.

        Expected result:
            - Raises HTTPException (status code 400).
            - Error message includes 'Current password is incorrect'.
        """
        with self.assertRaises(HTTPException) as context:
            self.auth_use_cases.change_password(
                self.test_user, "wrongpassword", "newpassword456"
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Current password is incorrect", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
