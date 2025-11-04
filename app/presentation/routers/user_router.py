from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.user_use_cases import UserUseCases
from app.presentation.schemas.user_schema import UserResponse, UserUpdate
from app.presentation.dependencies.auth_dependencies import require_admin, require_ti_or_admin
from app.domain.entities.user import User

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_use_cases(db: Session = Depends(get_db)) -> UserUseCases:
    """
    Dependency provider for user-related use cases.
    """
    return UserUseCases(UserRepositoryImpl(db))


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Number of records to skip (pagination)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """
    Retrieve all users — Requires TI or Administrator role.
    """
    users = user_use_cases.get_all_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """
    Retrieve a user by their ID — Requires TI or Administrator role.
    """
    user = user_use_cases.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(require_admin),
):
    """
    Update an existing user — Only administrators can perform this action.
    """
    updated_user = user_use_cases.update_user(
        user_id=user_id,
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active,
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(require_admin),
):
    """
    Delete a user — Only administrators can delete users.
    """
    deleted = user_use_cases.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
