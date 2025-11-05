from app.domain.entities.user import User, UserRole
from datetime import datetime, timezone

def test_user_creation_defaults():
    user = User(username="Admin", email="ADMIN@Test.com", full_name="Main Admin")

    assert user.username == "Admin"
    assert user.email == "admin@test.com"  # debe normalizar a minúsculas
    assert user.role == UserRole.ADMINISTRADOR
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)

def test_user_permission_hierarchy():
    admin = User(username="admin", role=UserRole.ADMINISTRADOR)
    ti = User(username="ti_user", role=UserRole.TI)
    guard = User(username="guard", role=UserRole.SEGURIDAD)

    # Admin tiene acceso a todo
    assert admin.has_permission(UserRole.TI)
    assert admin.has_permission(UserRole.SEGURIDAD)

    # TI no puede acceder a nivel admin
    assert not ti.has_permission(UserRole.ADMINISTRADOR)
    assert ti.has_permission(UserRole.SEGURIDAD)

    # Seguridad solo a su nivel
    assert not guard.has_permission(UserRole.TI)

def test_user_repr():
    user = User(username="test")
    assert "<User" in repr(user)
    assert "test" in repr(user)
