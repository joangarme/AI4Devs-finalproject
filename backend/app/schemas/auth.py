"""
Authentication schemas for user registration and login.

This module contains Pydantic models for authentication-related API requests
and responses, including user registration and login.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr, ConfigDict


class UserRegisterRequest(BaseModel):
    """
    Request model for user registration.
    
    Attributes:
        email: User's email address (validated format)
        password: User's password (stored as SecretStr for security)
    """
    email: EmailStr = Field(
        ...,
        description="Valid email address for the user account"
    )
    password: SecretStr = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters"
    )


class UserRegisterResponse(BaseModel):
    """
    Response model for successful user registration.
    
    Returns user information without sensitive data like password.
    
    Attributes:
        id: Unique user identifier
        email: User's registered email address
        created_at: Timestamp when the account was created
        is_active: Whether the account is active
    """
    id: int = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(default=True, description="Account active status")
    
    model_config = ConfigDict(from_attributes=True)


class UserLoginRequest(BaseModel):
    """
    Request model for user login.
    
    Attributes:
        email: User's email address
        password: User's password (stored as SecretStr for security)
    """
    email: EmailStr = Field(
        ...,
        description="User's registered email address"
    )
    password: SecretStr = Field(
        ...,
        description="User's password"
    )

