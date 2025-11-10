from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime

from app.presentation.routers.auth_router import get_auth_use_cases
from app.presentation.dependencies.auth_dependencies import (
    get_current_user,
    get_current_active_user,
    require_admin,
)
from app.domain.entities.user import UserRole


# ---------------------------------------------------------
# Fake Models (simulate real objects to pass validation)
# ---------------------------------------------------------
class FakeUser:
    def __init__(
        self,
        id=1,
        username="fakeuser",
        role=UserRole.ADMINISTRADOR,
        is_active=True,
        email="fake@example.com",
        full_name="Fake User",
        created_at=None,
        updated_at=None
    ):
        self.id = id
        self.username = username
        self.role = role
        self.is_active = is_active
        self.email = email
        self.full_name = full_name
        now = datetime.utcnow()
        self.created_at = created_at or now
        self.updated_at = updated_at or now


# ---------------------------------------------------------
#                      Fake Use Cases
# ---------------------------------------------------------
class FakeAuthUseCases:
    def authenticate_user(self, username, password):
        if username == "admin" and password == "1234":
            return FakeUser()
        return None

    def create_user_token(self, user):
        return "fake-token"

    def register_user(self, **kwargs):
        now = datetime.utcnow()
        return {
            "id": 1,
            "username": kwargs["username"],
            "email": kwargs["email"],
            "full_name": kwargs["full_name"],
            "role": kwargs["role"],
            "is_active": True,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

    def change_password(self, user, current_password, new_password):
        return True


# ---------------------------------------------------------
#                     Dependency overrides
# ---------------------------------------------------------
def override_get_auth_use_cases():
    return FakeAuthUseCases()


def override_get_current_user():
    return FakeUser()


def override_get_current_active_user():
    return FakeUser(is_active=True)


def override_require_admin():
    return FakeUser(role=UserRole.ADMINISTRADOR)


# ---------------------------------------------------------
#                         Test cases
# ---------------------------------------------------------
def test_login_success(client: TestClient, app):
    app.dependency_overrides[get_auth_use_cases] = override_get_auth_use_cases

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": "fake-token",
        "token_type": "bearer",
    }


def test_login_failure(client: TestClient, app):
    app.dependency_overrides[get_auth_use_cases] = override_get_auth_use_cases

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_user(client: TestClient, app):
    app.dependency_overrides[get_auth_use_cases] = override_get_auth_use_cases
    app.dependency_overrides[require_admin] = override_require_admin

    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "full_name": "Nuevo Usuario",
        "password": "password123",
        "role": UserRole.ADMINISTRADOR,
    }

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "newuser"


def test_get_current_user(client: TestClient, app):
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer fake"})

    assert response.status_code == 200
    assert response.json()["username"] == "fakeuser"


def test_change_password(client: TestClient, app):
    app.dependency_overrides[get_auth_use_cases] = override_get_auth_use_cases
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    payload = {
        "current_password": "1234",
        "new_password": "newpassword123",  # minimum 8 chars
    }

    response = client.post("/api/v1/auth/change-password", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Password changed successfully"}