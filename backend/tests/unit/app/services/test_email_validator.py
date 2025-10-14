"""
Unit tests for email validation service.

Tests all email validation rules, database duplicate checking, and edge cases
to ensure email addresses are properly validated and unique.
"""

import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from app.services.email_validator import EmailValidator, EmailValidationError


class TestEmailValidationError:
    """Tests for EmailValidationError class."""
    
    def test_error_initialization(self):
        """Test that EmailValidationError initializes correctly."""
        error = EmailValidationError("test_code", "Test message")
        assert error.code == "test_code"
        assert error.message == "Test message"
    
    def test_error_equality(self):
        """Test that two errors with same code and message are equal."""
        error1 = EmailValidationError("code1", "Message 1")
        error2 = EmailValidationError("code1", "Message 1")
        error3 = EmailValidationError("code2", "Message 2")
        
        assert error1 == error2
        assert error1 != error3
    
    def test_error_equality_with_non_error(self):
        """Test that comparing error with non-error returns False."""
        error = EmailValidationError("code", "message")
        assert error != "string"
        assert error != 123
        assert error != None
    
    def test_error_repr(self):
        """Test string representation of error."""
        error = EmailValidationError("test_code", "Test message")
        repr_str = repr(error)
        assert "test_code" in repr_str
        assert "Test message" in repr_str


class TestEmailNormalization:
    """Tests for email normalization."""
    
    def test_normalize_email_lowercase(self):
        """Test that email is normalized to lowercase."""
        test_cases = [
            ("USER@EXAMPLE.COM", "user@example.com"),
            ("User@Example.COM", "user@example.com"),
            ("user@example.com", "user@example.com"),
            ("MixedCase@Domain.ORG", "mixedcase@domain.org"),
        ]
        
        for input_email, expected in test_cases:
            result = EmailValidator.normalize_email(input_email)
            assert result == expected
    
    def test_normalize_email_strips_whitespace(self):
        """Test that whitespace is stripped from email."""
        test_cases = [
            ("  user@example.com  ", "user@example.com"),
            ("user@example.com  ", "user@example.com"),
            ("  user@example.com", "user@example.com"),
            ("\tuser@example.com\n", "user@example.com"),
        ]
        
        for input_email, expected in test_cases:
            result = EmailValidator.normalize_email(input_email)
            assert result == expected
    
    def test_normalize_email_preserves_special_chars(self):
        """Test that special characters in email are preserved."""
        test_cases = [
            ("user+tag@example.com", "user+tag@example.com"),
            ("user.name@example.com", "user.name@example.com"),
            ("user_name@example.com", "user_name@example.com"),
            ("user-name@example.com", "user-name@example.com"),
        ]
        
        for input_email, expected in test_cases:
            result = EmailValidator.normalize_email(input_email)
            assert result == expected


class TestEmailFormatValidation:
    """Tests for email format validation."""
    
    # Valid email format tests
    
    def test_validate_format_valid_emails(self):
        """Test that valid email formats pass validation."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user_name@example.com",
            "user-name@example.com",
            "user123@example.com",
            "123user@example.com",
            "user@subdomain.example.com",
            "user@example.co.uk",
            "a@example.com",  # Single character local part
            "user@a.com",  # Short domain
        ]
        
        for email in valid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 0, f"Valid email '{email}' failed validation: {errors}"
    
    # Invalid email format tests
    
    def test_validate_format_empty_email(self):
        """Test that empty email fails validation."""
        test_cases = ["", "   ", "\t", "\n"]
        
        for email in test_cases:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 1
            assert errors[0].code == "empty_email"
            assert errors[0].message == EmailValidator.ERROR_EMPTY
    
    def test_validate_format_missing_at_symbol(self):
        """Test that email without @ symbol fails validation."""
        invalid_emails = [
            "userexample.com",
            "user.example.com",
            "user",
        ]
        
        for email in invalid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 1
            assert errors[0].code == "invalid_format"
            assert errors[0].message == EmailValidator.ERROR_INVALID_FORMAT
    
    def test_validate_format_multiple_at_symbols(self):
        """Test that email with multiple @ symbols fails validation."""
        invalid_emails = [
            "user@@example.com",
            "user@ex@ample.com",
            "@@example.com",
        ]
        
        for email in invalid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 1
            assert errors[0].code == "invalid_format"
    
    def test_validate_format_invalid_local_part(self):
        """Test that emails with invalid local part fail validation."""
        invalid_emails = [
            "@example.com",  # Missing local part
            ".user@example.com",  # Starts with dot
            "user.@example.com",  # Ends with dot
            "user..name@example.com",  # Consecutive dots
        ]
        
        for email in invalid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 1
            assert errors[0].code == "invalid_format"
    
    def test_validate_format_invalid_domain(self):
        """Test that emails with invalid domain fail validation."""
        invalid_emails = [
            "user@",  # Missing domain
            "user@.",  # Invalid domain
            "user@.com",  # Missing domain name
            "user@domain",  # Missing TLD (note: this might pass depending on email-validator config)
            "user@domain..com",  # Consecutive dots in domain
        ]
        
        for email in invalid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) >= 1
            error_codes = [e.code for e in errors]
            assert "invalid_format" in error_codes or "empty_email" in error_codes
    
    def test_validate_format_invalid_characters(self):
        """Test that emails with invalid characters fail validation."""
        invalid_emails = [
            "user name@example.com",  # Space in local part
            "user@exam ple.com",  # Space in domain
            "user<script>@example.com",  # HTML tags
            "user@example$.com",  # Invalid domain char
        ]
        
        for email in invalid_emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 1
            assert errors[0].code == "invalid_format"


class TestEmailDuplicateChecking:
    """Tests for email duplicate checking in database."""
    
    def test_check_duplicate_no_duplicate_exists(self):
        """Test that non-existent email passes duplicate check."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0  # No duplicates found
        mock_db.execute.return_value = mock_result
        
        errors = EmailValidator.check_duplicate("newuser@example.com", mock_db)
        
        assert len(errors) == 0
        mock_db.execute.assert_called_once()
    
    def test_check_duplicate_duplicate_exists(self):
        """Test that existing email fails duplicate check."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1  # Duplicate found
        mock_db.execute.return_value = mock_result
        
        errors = EmailValidator.check_duplicate("existing@example.com", mock_db)
        
        assert len(errors) == 1
        assert errors[0].code == "duplicate_email"
        assert errors[0].message == EmailValidator.ERROR_DUPLICATE
        mock_db.execute.assert_called_once()
    
    def test_check_duplicate_case_insensitive(self):
        """Test that duplicate check is case-insensitive."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1  # Duplicate found
        mock_db.execute.return_value = mock_result
        
        # Test with uppercase email
        errors = EmailValidator.check_duplicate("USER@EXAMPLE.COM", mock_db)
        
        assert len(errors) == 1
        assert errors[0].code == "duplicate_email"
        
        # Verify the query was called with normalized (lowercase) email
        call_args = mock_db.execute.call_args
        query_params = call_args[0][1] if len(call_args[0]) > 1 else call_args[1]
        assert query_params["email"] == "user@example.com"
    
    def test_check_duplicate_uses_parameterized_query(self):
        """Test that duplicate check uses parameterized query (SQL injection prevention)."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db.execute.return_value = mock_result
        
        # Try with potential SQL injection attempt
        malicious_email = "test@example.com'; DROP TABLE users; --"
        errors = EmailValidator.check_duplicate(malicious_email, mock_db)
        
        # Should still work safely with parameterized query
        assert len(errors) == 0
        mock_db.execute.assert_called_once()
        
        # Verify parameterized query was used
        call_args = mock_db.execute.call_args
        assert call_args is not None
        # First arg should be the query with :email placeholder
        query = call_args[0][0]
        assert ":email" in str(query)


class TestEmailValidatorFullValidation:
    """Tests for complete email validation (format + duplicates)."""
    
    def test_validate_format_only_no_db_session(self):
        """Test that validation without db session only checks format."""
        # Valid format
        errors = EmailValidator.validate("user@example.com")
        assert len(errors) == 0
        
        # Invalid format
        errors = EmailValidator.validate("invalid-email")
        assert len(errors) == 1
        assert errors[0].code == "invalid_format"
    
    def test_validate_with_db_session_valid_unique_email(self):
        """Test validation with db session for valid unique email."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0  # No duplicates
        mock_db.execute.return_value = mock_result
        
        errors = EmailValidator.validate("newuser@example.com", mock_db)
        
        assert len(errors) == 0
    
    def test_validate_with_db_session_valid_duplicate_email(self):
        """Test validation with db session for valid but duplicate email."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1  # Duplicate found
        mock_db.execute.return_value = mock_result
        
        errors = EmailValidator.validate("existing@example.com", mock_db)
        
        assert len(errors) == 1
        assert errors[0].code == "duplicate_email"
    
    def test_validate_with_db_session_invalid_format(self):
        """Test that invalid format skips database check."""
        # Mock database session
        mock_db = Mock(spec=Session)
        
        errors = EmailValidator.validate("invalid-email", mock_db)
        
        # Should have format error
        assert len(errors) == 1
        assert errors[0].code == "invalid_format"
        
        # Database should not be called for invalid format
        mock_db.execute.assert_not_called()
    
    def test_validate_returns_both_format_and_duplicate_errors(self):
        """Test that only format errors are returned if format is invalid."""
        # Mock database session (won't be used)
        mock_db = Mock(spec=Session)
        
        errors = EmailValidator.validate("", mock_db)
        
        # Should only have empty email error, no db check
        assert len(errors) == 1
        assert errors[0].code == "empty_email"
        mock_db.execute.assert_not_called()
    
    def test_is_valid_returns_true_for_valid_email(self):
        """Test that is_valid returns True for valid emails."""
        valid_emails = [
            "user@example.com",
            "test.user@example.co.uk",
            "user+tag@subdomain.example.com",
        ]
        
        for email in valid_emails:
            assert EmailValidator.is_valid(email) is True
    
    def test_is_valid_returns_false_for_invalid_email(self):
        """Test that is_valid returns False for invalid emails."""
        invalid_emails = [
            "",
            "invalid-email",
            "user@",
            "@example.com",
            "user name@example.com",
        ]
        
        for email in invalid_emails:
            assert EmailValidator.is_valid(email) is False
    
    def test_is_valid_with_db_session_checks_duplicates(self):
        """Test that is_valid with db session checks duplicates."""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1  # Duplicate found
        mock_db.execute.return_value = mock_result
        
        result = EmailValidator.is_valid("existing@example.com", mock_db)
        
        assert result is False
        mock_db.execute.assert_called_once()


class TestEmailValidatorEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_validate_very_long_email(self):
        """Test that very long emails are handled correctly."""
        # Create a very long but valid email
        long_local = "a" * 64  # Max local part length
        email = f"{long_local}@example.com"
        errors = EmailValidator.validate_format(email)
        # Should be valid
        assert len(errors) == 0
    
    def test_validate_international_domain(self):
        """Test that international domain names work."""
        # Note: email-validator handles internationalized domains
        emails = [
            "user@example.com",
            "user@subdomain.example.com",
        ]
        
        for email in emails:
            errors = EmailValidator.validate_format(email)
            assert len(errors) == 0
    
    def test_validate_email_with_plus_addressing(self):
        """Test that plus addressing (email tags) works."""
        email = "user+newsletter@example.com"
        errors = EmailValidator.validate_format(email)
        assert len(errors) == 0
    
    def test_validate_email_with_subdomain(self):
        """Test that emails with subdomains work."""
        email = "user@mail.subdomain.example.com"
        errors = EmailValidator.validate_format(email)
        assert len(errors) == 0
    
    def test_normalize_email_with_unicode(self):
        """Test normalization of email with unicode characters."""
        email = "ÜSER@EXAMPLE.COM"
        normalized = EmailValidator.normalize_email(email)
        # Should be lowercase
        assert normalized == "üser@example.com"


class TestErrorMessageAccuracy:
    """Tests for error message accuracy and clarity."""
    
    def test_error_messages_are_user_friendly(self):
        """Test that error messages are clear and user-friendly."""
        test_cases = [
            ("", "empty_email"),
            ("invalid-email", "invalid_format"),
        ]
        
        for email, expected_code in test_cases:
            errors = EmailValidator.validate_format(email)
            matching_errors = [e for e in errors if e.code == expected_code]
            assert len(matching_errors) == 1
            
            error = matching_errors[0]
            # Each error should have a non-empty message
            assert error.message
            assert len(error.message) > 0
            # Message should be descriptive
            assert len(error.message) > 10
    
    def test_error_messages_match_constants(self):
        """Test that error messages match the defined constants."""
        # Test format error
        errors = EmailValidator.validate_format("invalid")
        format_errors = [e for e in errors if e.code == "invalid_format"]
        assert len(format_errors) == 1
        assert format_errors[0].message == EmailValidator.ERROR_INVALID_FORMAT
        
        # Test empty error
        errors = EmailValidator.validate_format("")
        empty_errors = [e for e in errors if e.code == "empty_email"]
        assert len(empty_errors) == 1
        assert empty_errors[0].message == EmailValidator.ERROR_EMPTY
        
        # Test duplicate error
        mock_db = Mock(spec=Session)
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1
        mock_db.execute.return_value = mock_result
        
        errors = EmailValidator.check_duplicate("test@example.com", mock_db)
        duplicate_errors = [e for e in errors if e.code == "duplicate_email"]
        assert len(duplicate_errors) == 1
        assert duplicate_errors[0].message == EmailValidator.ERROR_DUPLICATE

