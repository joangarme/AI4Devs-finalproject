"""
Unit tests for password validation service.

Tests all password validation rules and edge cases to ensure
password security requirements are properly enforced.
"""

import pytest
from app.services.password_validator import PasswordValidator, PasswordValidationError


class TestPasswordValidationError:
    """Tests for PasswordValidationError class."""
    
    def test_error_initialization(self):
        """Test that PasswordValidationError initializes correctly."""
        error = PasswordValidationError("test_code", "Test message")
        assert error.code == "test_code"
        assert error.message == "Test message"
    
    def test_error_equality(self):
        """Test that two errors with same code and message are equal."""
        error1 = PasswordValidationError("code1", "Message 1")
        error2 = PasswordValidationError("code1", "Message 1")
        error3 = PasswordValidationError("code2", "Message 2")
        
        assert error1 == error2
        assert error1 != error3
    
    def test_error_equality_with_non_error(self):
        """Test that comparing error with non-error returns False."""
        error = PasswordValidationError("code", "message")
        assert error != "string"
        assert error != 123
        assert error != None
    
    def test_error_repr(self):
        """Test string representation of error."""
        error = PasswordValidationError("test_code", "Test message")
        repr_str = repr(error)
        assert "test_code" in repr_str
        assert "Test message" in repr_str


class TestPasswordValidator:
    """Tests for PasswordValidator class."""
    
    # Tests for minimum length requirement
    
    def test_validate_minimum_length_too_short(self):
        """Test that passwords shorter than 8 characters fail validation."""
        passwords = ["", "a", "ab", "abc", "abcd", "abcde", "abcdef", "abcdefg"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            min_length_errors = [e for e in errors if e.code == "min_length"]
            assert len(min_length_errors) == 1
            assert min_length_errors[0].message == PasswordValidator.ERROR_MIN_LENGTH
    
    def test_validate_minimum_length_exactly_8_chars(self):
        """Test that password with exactly 8 characters passes length check."""
        # This password has 8 chars but may fail other requirements
        password = "abcdefgh"
        errors = PasswordValidator.validate(password)
        min_length_errors = [e for e in errors if e.code == "min_length"]
        assert len(min_length_errors) == 0
    
    def test_validate_minimum_length_more_than_8_chars(self):
        """Test that password with more than 8 characters passes length check."""
        password = "abcdefghijk"
        errors = PasswordValidator.validate(password)
        min_length_errors = [e for e in errors if e.code == "min_length"]
        assert len(min_length_errors) == 0
    
    # Tests for uppercase letter requirement
    
    def test_validate_no_uppercase_letter(self):
        """Test that password without uppercase letter fails validation."""
        passwords = ["alllowercase", "lowercase123", "lowercase123!", "12345678!"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            uppercase_errors = [e for e in errors if e.code == "no_uppercase"]
            assert len(uppercase_errors) == 1
            assert uppercase_errors[0].message == PasswordValidator.ERROR_NO_UPPERCASE
    
    def test_validate_with_uppercase_letter(self):
        """Test that password with uppercase letter passes uppercase check."""
        passwords = ["Uppercase", "UpperCase123", "ALLUPPERCASE", "miXedCase"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            uppercase_errors = [e for e in errors if e.code == "no_uppercase"]
            assert len(uppercase_errors) == 0
    
    def test_validate_multiple_uppercase_letters(self):
        """Test that password with multiple uppercase letters passes."""
        password = "MULTIPLE"
        errors = PasswordValidator.validate(password)
        uppercase_errors = [e for e in errors if e.code == "no_uppercase"]
        assert len(uppercase_errors) == 0
    
    # Tests for number requirement
    
    def test_validate_no_number(self):
        """Test that password without number fails validation."""
        passwords = ["NoNumbers", "NoNumbersHere!", "ALLUPPERCASE", "lowercase"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            number_errors = [e for e in errors if e.code == "no_number"]
            assert len(number_errors) == 1
            assert number_errors[0].message == PasswordValidator.ERROR_NO_NUMBER
    
    def test_validate_with_number(self):
        """Test that password with number passes number check."""
        passwords = ["Password1", "123456789", "Pass0word", "0ne2three"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            number_errors = [e for e in errors if e.code == "no_number"]
            assert len(number_errors) == 0
    
    def test_validate_multiple_numbers(self):
        """Test that password with multiple numbers passes."""
        password = "12345678"
        errors = PasswordValidator.validate(password)
        number_errors = [e for e in errors if e.code == "no_number"]
        assert len(number_errors) == 0
    
    # Tests for special character requirement
    
    def test_validate_no_special_character(self):
        """Test that password without special character fails validation."""
        passwords = ["NoSpecial1", "Password123", "UPPERCASE123", "lowercase123"]
        
        for password in passwords:
            errors = PasswordValidator.validate(password)
            special_errors = [e for e in errors if e.code == "no_special_char"]
            assert len(special_errors) == 1
            assert special_errors[0].message == PasswordValidator.ERROR_NO_SPECIAL_CHAR
    
    def test_validate_with_special_characters(self):
        """Test that password with various special characters passes."""
        special_chars = r"!@#$%^&*(),.?\":{}|<>_-+=[]\/;~`"
        
        for char in special_chars:
            password = f"Password1{char}"
            errors = PasswordValidator.validate(password)
            special_errors = [e for e in errors if e.code == "no_special_char"]
            assert len(special_errors) == 0, f"Failed for special char: {char}"
    
    def test_validate_multiple_special_characters(self):
        """Test that password with multiple special characters passes."""
        password = "Pass!@#$123"
        errors = PasswordValidator.validate(password)
        special_errors = [e for e in errors if e.code == "no_special_char"]
        assert len(special_errors) == 0
    
    # Tests for valid passwords
    
    def test_validate_valid_password_passes_all_checks(self):
        """Test that a valid password passes all validation checks."""
        valid_passwords = [
            "Password1!",
            "Strong1@",
            "Secure#2",
            "MyP@ssw0rd",
            "C0mplex!Pass",
            "Test123!@#",
            "Abcdef1!",  # Exactly 8 chars
            "VeryLongPassword123!@#$%"
        ]
        
        for password in valid_passwords:
            errors = PasswordValidator.validate(password)
            assert len(errors) == 0, f"Valid password '{password}' failed validation: {errors}"
    
    def test_is_valid_returns_true_for_valid_password(self):
        """Test that is_valid returns True for valid passwords."""
        valid_passwords = [
            "Password1!",
            "Strong1@",
            "Secure#2"
        ]
        
        for password in valid_passwords:
            assert PasswordValidator.is_valid(password) is True
    
    def test_is_valid_returns_false_for_invalid_password(self):
        """Test that is_valid returns False for invalid passwords."""
        invalid_passwords = [
            "weak",
            "NoNumber!",
            "nouppercas1!",
            "NoSpecial1",
            "Short1!"  # Only 7 chars
        ]
        
        for password in invalid_passwords:
            assert PasswordValidator.is_valid(password) is False
    
    # Tests for multiple validation failures
    
    def test_validate_returns_all_errors_for_weak_password(self):
        """Test that all validation errors are returned for a weak password."""
        password = "weak"
        errors = PasswordValidator.validate(password)
        
        # Should fail all checks except length might vary
        error_codes = [e.code for e in errors]
        
        # Should have at least these errors
        assert "no_uppercase" in error_codes
        assert "no_number" in error_codes
        assert "no_special_char" in error_codes
    
    def test_validate_empty_password_returns_all_errors(self):
        """Test that empty password returns all validation errors."""
        password = ""
        errors = PasswordValidator.validate(password)
        
        # Should fail all 4 checks
        assert len(errors) == 4
        error_codes = [e.code for e in errors]
        assert "min_length" in error_codes
        assert "no_uppercase" in error_codes
        assert "no_number" in error_codes
        assert "no_special_char" in error_codes
    
    # Boundary cases
    
    def test_validate_exactly_8_characters_all_requirements(self):
        """Test boundary case: exactly 8 characters meeting all requirements."""
        password = "Abcdef1!"
        errors = PasswordValidator.validate(password)
        assert len(errors) == 0
    
    def test_validate_7_characters_all_other_requirements(self):
        """Test boundary case: 7 characters but meets all other requirements."""
        password = "Abcd1!x"
        errors = PasswordValidator.validate(password)
        
        # Should only fail minimum length
        assert len(errors) == 1
        assert errors[0].code == "min_length"
    
    def test_validate_whitespace_in_password(self):
        """Test that whitespace in password is handled correctly."""
        # Whitespace is not considered a special character
        password = "Pass word1"
        errors = PasswordValidator.validate(password)
        special_errors = [e for e in errors if e.code == "no_special_char"]
        assert len(special_errors) == 1
    
    def test_validate_unicode_characters(self):
        """Test that unicode characters don't satisfy requirements."""
        password = "Pässwörd1"
        errors = PasswordValidator.validate(password)
        # Should fail special char requirement
        special_errors = [e for e in errors if e.code == "no_special_char"]
        assert len(special_errors) == 1
    
    # Error message accuracy tests
    
    def test_error_messages_are_user_friendly(self):
        """Test that error messages are clear and user-friendly."""
        password = "weak"
        errors = PasswordValidator.validate(password)
        
        for error in errors:
            # Each error should have a non-empty message
            assert error.message
            assert len(error.message) > 0
            # Message should be descriptive
            assert len(error.message) > 20
    
    def test_error_messages_match_constants(self):
        """Test that error messages match the defined constants."""
        test_cases = [
            ("short", "min_length", PasswordValidator.ERROR_MIN_LENGTH),
            ("nouppercase1!", "no_uppercase", PasswordValidator.ERROR_NO_UPPERCASE),
            ("NoNumber!", "no_number", PasswordValidator.ERROR_NO_NUMBER),
            ("NoSpecial1", "no_special_char", PasswordValidator.ERROR_NO_SPECIAL_CHAR),
        ]
        
        for password, expected_code, expected_message in test_cases:
            errors = PasswordValidator.validate(password)
            matching_errors = [e for e in errors if e.code == expected_code]
            assert len(matching_errors) == 1
            assert matching_errors[0].message == expected_message
    
    # Edge cases
    
    def test_validate_very_long_password(self):
        """Test that very long passwords are handled correctly."""
        password = "A1!" + "a" * 1000
        errors = PasswordValidator.validate(password)
        assert len(errors) == 0
    
    def test_validate_only_special_characters(self):
        """Test password with only special characters."""
        password = "!@#$%^&*"
        errors = PasswordValidator.validate(password)
        
        # Should fail uppercase and number requirements
        error_codes = [e.code for e in errors]
        assert "no_uppercase" in error_codes
        assert "no_number" in error_codes
        assert "no_special_char" not in error_codes
    
    def test_validate_password_with_all_character_types(self):
        """Test password that includes all required character types."""
        password = "Abc123!@#def"
        errors = PasswordValidator.validate(password)
        assert len(errors) == 0

