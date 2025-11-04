from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.presentation.schemas.user_schema import (
    Token,
    UserCreate,
    UserResponse,
    ChangePassword,
)
from app.presentation.dependencies.auth_dependencies import (
    get_current_active_user,
    require_admin,
)
from app.domain.entities.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Dependencies


def get_auth_use_cases(db: Session = Depends(get_db)) -> AuthUseCases:
    """
    Dependency that provides an instance of AuthUseCases.
    """
    user_repository = UserRepositoryImpl(db)
    return AuthUseCases(user_repository)


# Authentication Endpoints


@router.post(
    "/login", response_model=Token, summary="Authenticate user and obtain JWT token"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    """
    Authenticate a user and return a JWT token.

    - **username**: Username
    - **password**: Password
    """
    user = auth_use_cases.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_use_cases.create_user_token(user)
    return Token(access_token=access_token, token_type="bearer")


# User Management Endpoints


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user (Admin only)",
)
async def register_user(
    user_data: UserCreate,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
    current_user: User = Depends(require_admin),
):
    """
    Register a new user — Only administrators can create users.

    - **username**: Unique username (3–50 characters)
    - **email**: Valid email address
    - **full_name**: Full name
    - **password**: Minimum 8 characters
    - **role**: User role (e.g., seguridad, ti, administrador)
    """
    return auth_use_cases.register_user(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password=user_data.password,
        role=user_data.role,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user information",
)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve the authenticated user's information.
    """
    return current_user


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change current user's password",
)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    """
    Change the authenticated user's password.

    - **current_password**: Current password
    - **new_password**: New password (minimum 8 characters)
    """
    auth_use_cases.change_password(
        user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password,
    )
    return {"message": "Password changed successfully"}
