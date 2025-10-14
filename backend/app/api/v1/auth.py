"""
Authentication API routes.

This module contains FastAPI routes for user authentication, including
registration and login endpoints.
"""

import uuid
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse
from app.services.user_service import (
    UserService, 
    UserAlreadyExistsError, 
    UserServiceError,
    UserCreationError
)

# Initialize router and logger
router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = get_logger("api.auth")


def get_request_id(request: Request) -> str:
    """
    Get or generate a unique request ID for tracking.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Request ID string (from header or generated)
    """
    # Check if request ID is provided in headers
    request_id = request.headers.get("X-Request-ID")
    
    # If not provided, generate a new one
    if not request_id:
        request_id = str(uuid.uuid4())
    
    return request_id


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="""
    Register a new user account with email and password.
    
    **Requirements:**
    - Email must be a valid email format
    - Email must not already be registered
    - Password must be at least 8 characters
    - Password must contain at least 1 uppercase letter
    - Password must contain at least 1 number
    - Password must contain at least 1 special character
    
    **Returns:**
    - 201: User successfully registered and active immediately (MVP: no email verification)
    - 400: Validation errors (invalid email format, weak password, etc.)
    - 409: Email already registered
    - 500: Internal server error
    """,
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "created_at": "2025-10-14T12:00:00",
                        "is_active": True
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid password: Password must contain at least one uppercase letter, Password must contain at least one number"
                    }
                }
            }
        },
        409: {
            "description": "Email already registered",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with email 'user@example.com' already exists"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to create user"
                    }
                }
            }
        }
    }
)
async def register(
    user_data: UserRegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> UserRegisterResponse:
    """
    Register a new user account.
    
    Creates a new user with the provided email and password. The password is
    validated against security requirements and then hashed using bcrypt before
    storage. The user is immediately active and can log in (MVP: no email verification).
    
    Args:
        user_data: User registration request with email and password
        request: FastAPI request object for logging context
        db: Database session dependency
        
    Returns:
        UserRegisterResponse with created user information (excluding password)
        
    Raises:
        HTTPException: 
            - 400 for validation errors
            - 409 for duplicate email
            - 500 for server errors
    """
    # Get or generate request ID for tracking
    request_id = get_request_id(request)
    
    # Log the registration attempt
    logger.info(
        f"Registration attempt - request_id={request_id}, email={user_data.email}"
    )
    
    try:
        # Create user service instance
        user_service = UserService(db)
        
        # Extract password from SecretStr
        password = user_data.password.get_secret_value()
        
        # Register the user (validation happens inside the service)
        user = user_service.register_user(
            email=user_data.email,
            password=password
        )
        
        # Log successful registration
        logger.info(
            f"User registered successfully - request_id={request_id}, "
            f"user_id={user.id}, email={user.email}"
        )
        
        # Return user response (Pydantic will automatically convert from User model)
        return UserRegisterResponse.model_validate(user)
        
    except UserAlreadyExistsError as e:
        # Email already exists - return 409 Conflict
        logger.warning(
            f"Registration failed: duplicate email - request_id={request_id}, "
            f"email={user_data.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
        
    except UserCreationError as e:
        # Database/system error - return 500 Internal Server Error
        # Must come before UserServiceError since UserCreationError inherits from it
        logger.error(
            f"Registration failed: system error - request_id={request_id}, "
            f"email={user_data.email}, error={e.message}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
        
    except UserServiceError as e:
        # Validation error - return 400 Bad Request
        logger.warning(
            f"Registration failed: validation error - request_id={request_id}, "
            f"email={user_data.email}, error={e.message}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
        
    except Exception as e:
        # Unexpected error - return 500 Internal Server Error
        logger.error(
            f"Registration failed: unexpected error - request_id={request_id}, "
            f"email={user_data.email}, error={str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )

