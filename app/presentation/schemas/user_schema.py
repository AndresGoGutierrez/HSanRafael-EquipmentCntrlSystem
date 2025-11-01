from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.entities.user import UserRole

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username used for login",
        examples=["andesgomez"],
    )

    email: EmailStr = Field(
        ...,
        description="User's valid email address.",
        examples=["andesgomez@gmail.com"],
    )

    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name",
        examples=["Andrés Gómez"],
    )

    role: UserRole = Field(
        ...,
        description="Role assigned to the user",
        examples=["ADMIN"],
    )

    # Create & Update Schemas


class UserCreate(UserBase):
    """Schema for creating a new user (registration or admin creation)."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password. Must be at least 8 characters.",
        examples=["SecurePass123"],
    )


class UserUpdate(BaseModel):
    """Schema for updating existing user details."""

    email: Optional[EmailStr] = Field(None, description="Updated email address")
    full_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Updated full name"
    )
    role: Optional[UserRole] = Field(None, description="Updated role of the user")
    is_active: Optional[bool] = Field(
        None, description="Indicates whether the user is active"
    )


# Response Schemas


class UserResponse(UserBase):
    """Schema for returning user data in responses."""

    id: int = Field(..., description="Unique user ID")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(..., description="Timestamp of the last user update")

    model_config = ConfigDict(from_attributes=True)


# Authentication Schemas


class UserLogin(BaseModel):
    """Schema for user login requests."""

    username: str = Field(..., description="Username used for authentication.")
    password: str = Field(..., description="User password.")


class Token(BaseModel):
    """Schema for JWT token responses."""

    access_token: str = Field(..., description="JWT access token string.")
    token_type: str = Field("bearer", description="Type of token returned.")


class TokenData(BaseModel):
    """Schema for decoded token data (used internally)."""

    username: Optional[str] = Field(None, description="Username encoded in the token.")
    user_id: Optional[int] = Field(None, description="User ID encoded in the token.")
    role: Optional[UserRole] = Field(
        None, description="User role encoded in the token."
    )


# Password Management


class ChangePassword(BaseModel):
    """Schema for changing an existing user's password."""

    current_password: str = Field(..., description="Current password of the user.")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="New password. Must differ from current password.",
        examples=["NewSecurePass456"],
    )
