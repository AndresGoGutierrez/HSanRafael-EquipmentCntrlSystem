"""
Unit tests for the User domain entity and UserRole permissions.
"""

import unittest
from datetime import datetime
from app.domain.entities.user import User, UserRole


class TestUserEntity(unittest.TestCase):
    """Tests related to creation and basic behavior of User entity."""

    def test_create_user(self):
        """User creation initializes all fields correctly."""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            role=UserRole.SEGURIDAD,
            hashed_password="hashed_password_here"
        )

        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertEqual(user.role, UserRole.SEGURIDAD)
        self.assertTrue(user.is_active)
        self.assertIsInstance(user.created_at, datetime)

    def test_user_role_enum_values(self):
        """UserRole enum must expose correct values."""
        self.assertEqual(UserRole.SEGURIDAD.value, "seguridad")
        self.assertEqual(UserRole.TI.value, "ti")
        self.assertEqual(UserRole.ADMINISTRADOR.value, "administrador")

    def test_inactive_user(self):
        """User should allow marking as inactive."""
        user = User(
            id=1,
            username="inactive",
            email="inactive@example.com",
            full_name="Inactive User",
            role=UserRole.SEGURIDAD,
            hashed_password="hashed",
            is_active=False
        )

        self.assertFalse(user.is_active)


class TestUserRolePermissions(unittest.TestCase):
    """Tests related to role hierarchy and permission rules."""

    def setUp(self):
        """Creates users for re-use across all tests."""
        self.admin_user = User(
            id=1, username="admin", email="admin@test.com",
            full_name="Admin User", role=UserRole.ADMINISTRADOR,
            hashed_password="hash"
        )
        self.ti_user = User(
            id=2, username="ti", email="ti@test.com",
            full_name="TI User", role=UserRole.TI,
            hashed_password="hash"
        )
        self.security_user = User(
            id=3, username="security", email="security@test.com",
            full_name="Security User", role=UserRole.SEGURIDAD,
            hashed_password="hash"
        )

    def test_permissions_same_role(self):
        """Users should always be able to perform actions of their own role."""
        self.assertTrue(self.ti_user.has_permission(UserRole.TI))

    def test_permissions_admin_can_access_all(self):
        """Admin should have permissions for all roles."""
        self.assertTrue(self.admin_user.has_permission(UserRole.ADMINISTRADOR))
        self.assertTrue(self.admin_user.has_permission(UserRole.TI))
        self.assertTrue(self.admin_user.has_permission(UserRole.SEGURIDAD))

    def test_permissions_ti_has_limited_access(self):
        """TI should have permission for TI and SEGURIDAD, not ADMINISTRADOR."""
        self.assertFalse(self.ti_user.has_permission(UserRole.ADMINISTRADOR))
        self.assertTrue(self.ti_user.has_permission(UserRole.TI))
        self.assertTrue(self.ti_user.has_permission(UserRole.SEGURIDAD))

    def test_permissions_security_only_self(self):
        """Security role should only have permissions for its own level."""
        self.assertFalse(self.security_user.has_permission(UserRole.ADMINISTRADOR))
        self.assertFalse(self.security_user.has_permission(UserRole.TI))
        self.assertTrue(self.security_user.has_permission(UserRole.SEGURIDAD))


if __name__ == "__main__":
    unittest.main()
