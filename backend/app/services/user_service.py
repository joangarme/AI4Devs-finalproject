"""
User service for registration and user management.

Handles user creation, password hashing, and user-related business logic.
"""

import bcrypt
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.user import User
from app.services.password_validator import PasswordValidator, PasswordValidationError
from app.services.email_validator import EmailValidator, EmailValidationError


class UserServiceError(Exception):
    """Base exception for user service errors."""
    
    def __init__(self, message: str, code: str = "user_service_error"):
        """
        Initialize a user service error.
        
        Args:
            message: Human-readable error message
            code: Error code identifier
        """
        self.message = message
        self.code = code
        super().__init__(self.message)


class UserAlreadyExistsError(UserServiceError):
    """Raised when attempting to create a user with an email that already exists."""
    
    def __init__(self, email: str):
        """
        Initialize a user already exists error.
        
        Args:
            email: The duplicate email address
        """
        super().__init__(
            message=f"User with email '{email}' already exists",
            code="user_already_exists"
        )
        self.email = email


class UserCreationError(UserServiceError):
    """Raised when user creation fails due to database or system errors."""
    
    def __init__(self, message: str = "Failed to create user"):
        """
        Initialize a user creation error.
        
        Args:
            message: Human-readable error message
        """
        super().__init__(message=message, code="user_creation_failed")


class UserService:
    """
    Service for user management operations.
    
    Handles user registration with password hashing, validation, and database operations.
    All database operations are wrapped in transactions with proper error handling.
    """
    
    # Bcrypt cost factor (number of rounds) - higher is more secure but slower
    # 12 rounds provides good security while maintaining reasonable performance
    BCRYPT_ROUNDS = 12
    
    def __init__(self, db: Session):
        """
        Initialize the user service.
        
        Args:
            db: SQLAlchemy database session for database operations
        """
        self.db = db
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Bcrypt hashed password as a string
            
        Note:
            Uses cost factor of 12 rounds for security.
            The resulting hash includes the salt and is safe to store directly.
        """
        # Generate salt and hash password
        # bcrypt.hashpw returns bytes, so we decode to string for storage
        salt = bcrypt.gensalt(rounds=UserService.BCRYPT_ROUNDS)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Bcrypt hash to verify against
            
        Returns:
            True if password matches the hash, False otherwise
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        
        This method:
        1. Validates the email format and checks for duplicates
        2. Validates the password against security requirements
        3. Hashes the password using bcrypt
        4. Creates the user record in the database
        5. Sets the user as active by default (MVP: no email verification)
        
        Args:
            email: User's email address
            password: User's plain text password
            
        Returns:
            Created User object (without password hash)
            
        Raises:
            UserServiceError: For validation errors (invalid email/password)
            UserAlreadyExistsError: If email already exists in database
            UserCreationError: If database operation fails
            
        Example:
            >>> service = UserService(db)
            >>> user = service.register_user("user@example.com", "SecurePass1!")
            >>> user.email
            'user@example.com'
            >>> user.is_active
            True
        """
        # Validate email format
        email_errors = EmailValidator.validate_format(email)
        if email_errors:
            error_messages = [err.message for err in email_errors]
            raise UserServiceError(
                message=f"Invalid email: {', '.join(error_messages)}",
                code="invalid_email"
            )
        
        # Normalize email to lowercase
        normalized_email = EmailValidator.normalize_email(email)
        
        # Check for duplicate email
        duplicate_errors = EmailValidator.check_duplicate(normalized_email, self.db)
        if duplicate_errors:
            raise UserAlreadyExistsError(normalized_email)
        
        # Validate password
        password_errors = PasswordValidator.validate(password)
        if password_errors:
            error_messages = [err.message for err in password_errors]
            raise UserServiceError(
                message=f"Invalid password: {', '.join(error_messages)}",
                code="invalid_password"
            )
        
        # Hash the password
        password_hash = self._hash_password(password)
        
        # Create user record wrapped in transaction
        try:
            user = User(
                email=normalized_email,
                password_hash=password_hash,
                is_active=True  # MVP: Users are active immediately upon registration
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return user
            
        except IntegrityError as e:
            # This should be caught by duplicate check above, but handle it just in case
            self.db.rollback()
            raise UserAlreadyExistsError(normalized_email) from e
            
        except SQLAlchemyError as e:
            # Handle any other database errors
            self.db.rollback()
            raise UserCreationError(f"Database error occurred: {str(e)}") from e
            
        except Exception as e:
            # Handle any unexpected errors
            self.db.rollback()
            raise UserCreationError(f"Unexpected error occurred: {str(e)}") from e
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: User's email address (case-insensitive)
            
        Returns:
            User object if found, None otherwise
        """
        normalized_email = EmailValidator.normalize_email(email)
        return self.db.query(User).filter(User.email == normalized_email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()

