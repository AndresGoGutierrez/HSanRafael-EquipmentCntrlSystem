from datetime import datetime
from app.domain.entities.user import User, UserRole


def test_user_creation_defaults():
    """
    Test that a User object is correctly created with default values.
    """
    user = User(username="Admin", email="ADMIN@Test.com", full_name="Main Admin")

    # Email should be normalized to lowercase
    assert user.username == "Admin"
    assert user.email == "admin@test.com"
    assert user.role == UserRole.ADMINISTRADOR
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)


def test_user_permission_hierarchy():
    """
    Test the role-based permission hierarchy among different user roles.
    """
    admin = User(username="admin", role=UserRole.ADMINISTRADOR)
    it_user = User(username="it_user", role=UserRole.TI)
    security = User(username="security_user", role=UserRole.SEGURIDAD)

    # Admin should have access to all roles
    assert admin.has_permission(UserRole.TI)
    assert admin.has_permission(UserRole.SEGURIDAD)

    # IT should not have admin-level access
    assert not it_user.has_permission(UserRole.ADMINISTRADOR)
    assert it_user.has_permission(UserRole.SEGURIDAD)

    # Security should only have access at their own level
    assert not security.has_permission(UserRole.TI)


def test_user_repr_contains_username():
    """
    Test that the string representation of a User includes the username.
    """
    user = User(username="test")
    representation = repr(user)
    assert "<User" in representation
    assert "test" in representation
