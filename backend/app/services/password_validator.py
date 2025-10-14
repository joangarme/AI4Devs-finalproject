"""
Password validation service for the Personal Finance Tracker.

Validates password requirements for user registration and ensures
password security standards are met.
"""

import re
from typing import List


class PasswordValidationError:
    """Represents a single password validation error."""
    
    def __init__(self, code: str, message: str):
        """
        Initialize a password validation error.
        
        Args:
            code: Error code identifier
            message: Human-readable error message
        """
        self.code = code
        self.message = message
    
    def __eq__(self, other):
        """Compare two validation errors."""
        if not isinstance(other, PasswordValidationError):
            return False
        return self.code == other.code and self.message == other.message
    
    def __repr__(self):
        """String representation of the error."""
        return f"PasswordValidationError(code='{self.code}', message='{self.message}')"


class PasswordValidator:
    """
    Validates passwords against security requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character
    """
    
    # Validation rules
    MIN_LENGTH = 8
    UPPERCASE_PATTERN = re.compile(r'[A-Z]')
    NUMBER_PATTERN = re.compile(r'[0-9]')
    SPECIAL_CHAR_PATTERN = re.compile(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]')
    
    # Error messages
    ERROR_MIN_LENGTH = "Password must be at least 8 characters long"
    ERROR_NO_UPPERCASE = "Password must contain at least 1 uppercase letter"
    ERROR_NO_NUMBER = "Password must contain at least 1 number"
    ERROR_NO_SPECIAL_CHAR = r"Password must contain at least 1 special character (!@#$%^&*(),.?\":{}|<>_-+=[]\/;~`)"
    
    @classmethod
    def validate(cls, password: str) -> List[PasswordValidationError]:
        """
        Validate a password against all requirements.
        
        Args:
            password: The password string to validate
            
        Returns:
            List of PasswordValidationError objects. Empty list if password is valid.
            
        Example:
            >>> errors = PasswordValidator.validate("weak")
            >>> len(errors) > 0
            True
            >>> errors = PasswordValidator.validate("Strong1!")
            >>> len(errors)
            0
        """
        errors = []
        
        # Check minimum length
        if len(password) < cls.MIN_LENGTH:
            errors.append(PasswordValidationError(
                code="min_length",
                message=cls.ERROR_MIN_LENGTH
            ))
        
        # Check for uppercase letter
        if not cls.UPPERCASE_PATTERN.search(password):
            errors.append(PasswordValidationError(
                code="no_uppercase",
                message=cls.ERROR_NO_UPPERCASE
            ))
        
        # Check for number
        if not cls.NUMBER_PATTERN.search(password):
            errors.append(PasswordValidationError(
                code="no_number",
                message=cls.ERROR_NO_NUMBER
            ))
        
        # Check for special character
        if not cls.SPECIAL_CHAR_PATTERN.search(password):
            errors.append(PasswordValidationError(
                code="no_special_char",
                message=cls.ERROR_NO_SPECIAL_CHAR
            ))
        
        return errors
    
    @classmethod
    def is_valid(cls, password: str) -> bool:
        """
        Check if a password is valid.
        
        Args:
            password: The password string to validate
            
        Returns:
            True if password meets all requirements, False otherwise
            
        Example:
            >>> PasswordValidator.is_valid("Strong1!")
            True
            >>> PasswordValidator.is_valid("weak")
            False
        """
        return len(cls.validate(password)) == 0

