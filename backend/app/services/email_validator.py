"""
Email validation service for the Personal Finance Tracker.

Validates email format and checks for duplicates in the database.
Ensures email addresses are properly formatted and unique.
"""

from typing import List, Optional
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session
from sqlalchemy import text


class EmailValidationError:
    """Represents a single email validation error."""
    
    def __init__(self, code: str, message: str):
        """
        Initialize an email validation error.
        
        Args:
            code: Error code identifier
            message: Human-readable error message
        """
        self.code = code
        self.message = message
    
    def __eq__(self, other):
        """Compare two validation errors."""
        if not isinstance(other, EmailValidationError):
            return False
        return self.code == other.code and self.message == other.message
    
    def __repr__(self):
        """String representation of the error."""
        return f"EmailValidationError(code='{self.code}', message='{self.message}')"


class EmailValidator:
    """
    Validates email addresses against format requirements and database constraints.
    
    Features:
    - RFC-compliant email format validation
    - Case-insensitive duplicate checking
    - Email normalization to lowercase
    - SQL injection prevention through parameterized queries
    """
    
    # Error messages
    ERROR_INVALID_FORMAT = "Email address is not valid"
    ERROR_DUPLICATE = "An account with this email already exists"
    ERROR_EMPTY = "Email address cannot be empty"
    
    @classmethod
    def normalize_email(cls, email: str) -> str:
        """
        Normalize an email address to lowercase for consistent storage.
        
        Args:
            email: The email address to normalize
            
        Returns:
            Normalized email address in lowercase
            
        Example:
            >>> EmailValidator.normalize_email("User@Example.COM")
            'user@example.com'
        """
        return email.lower().strip()
    
    @classmethod
    def validate_format(cls, email: str) -> List[EmailValidationError]:
        """
        Validate email format using RFC-compliant validation.
        
        Args:
            email: The email address to validate
            
        Returns:
            List of EmailValidationError objects. Empty list if format is valid.
            
        Example:
            >>> errors = EmailValidator.validate_format("invalid-email")
            >>> len(errors) > 0
            True
            >>> errors = EmailValidator.validate_format("user@example.com")
            >>> len(errors)
            0
        """
        errors = []
        
        # Check for empty email
        if not email or not email.strip():
            errors.append(EmailValidationError(
                code="empty_email",
                message=cls.ERROR_EMPTY
            ))
            return errors
        
        # Validate email format using RFC-compliant library
        try:
            # validate_email performs comprehensive checks including:
            # - Proper @ symbol placement
            # - Valid characters in local and domain parts
            # - Domain name structure
            # - TLD existence (can be disabled with check_deliverability=False)
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            errors.append(EmailValidationError(
                code="invalid_format",
                message=cls.ERROR_INVALID_FORMAT
            ))
        
        return errors
    
    @classmethod
    def check_duplicate(cls, email: str, db: Session) -> List[EmailValidationError]:
        """
        Check if email already exists in database (case-insensitive).
        
        Args:
            email: The email address to check
            db: Database session for querying
            
        Returns:
            List of EmailValidationError objects. Empty list if email is unique.
            
        Example:
            >>> errors = EmailValidator.check_duplicate("new@example.com", db)
            >>> len(errors)
            0
        """
        errors = []
        
        # Normalize email for case-insensitive comparison
        normalized_email = cls.normalize_email(email)
        
        # Use parameterized query to prevent SQL injection
        # LOWER() ensures case-insensitive comparison
        query = text("SELECT COUNT(*) as count FROM users WHERE LOWER(email) = :email")
        result = db.execute(query, {"email": normalized_email})
        count = result.scalar()
        
        if count > 0:
            errors.append(EmailValidationError(
                code="duplicate_email",
                message=cls.ERROR_DUPLICATE
            ))
        
        return errors
    
    @classmethod
    def validate(cls, email: str, db: Optional[Session] = None) -> List[EmailValidationError]:
        """
        Validate email format and optionally check for duplicates.
        
        Args:
            email: The email address to validate
            db: Optional database session for duplicate checking
            
        Returns:
            List of EmailValidationError objects. Empty list if email is valid.
            
        Example:
            >>> errors = EmailValidator.validate("user@example.com")
            >>> len(errors)
            0
            >>> errors = EmailValidator.validate("user@example.com", db_session)
            >>> # Will check both format and duplicates
        """
        errors = []
        
        # First validate format
        format_errors = cls.validate_format(email)
        errors.extend(format_errors)
        
        # Only check duplicates if format is valid and db session is provided
        if not format_errors and db is not None:
            duplicate_errors = cls.check_duplicate(email, db)
            errors.extend(duplicate_errors)
        
        return errors
    
    @classmethod
    def is_valid(cls, email: str, db: Optional[Session] = None) -> bool:
        """
        Check if an email is valid.
        
        Args:
            email: The email address to validate
            db: Optional database session for duplicate checking
            
        Returns:
            True if email meets all requirements, False otherwise
            
        Example:
            >>> EmailValidator.is_valid("user@example.com")
            True
            >>> EmailValidator.is_valid("invalid-email")
            False
        """
        return len(cls.validate(email, db)) == 0

