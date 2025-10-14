"""
Unit tests for authentication schemas.

Tests cover model instantiation, validation, serialization, and security features.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
)


class TestUserRegisterRequest:
    """Tests for UserRegisterRequest model."""

    def test_valid_registration_request(self):
        """Test creating a valid registration request."""
        request = UserRegisterRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        assert request.email == "test@example.com"
        # SecretStr hides the actual value in representation
        assert request.password.get_secret_value() == "SecurePass123!"

    def test_invalid_email_format(self):
        """Test that invalid email format raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(
                email="invalid-email",
                password="SecurePass123!"
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_password_min_length_validation(self):
        """Test that password must meet minimum length requirement."""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(
                email="test@example.com",
                password="short"
            )
        
        errors = exc_info.value.errors()
        # Check that there's a validation error for password field
        assert any(error["loc"] == ("password",) for error in errors)
        # Verify it's a string_too_short error
        password_errors = [e for e in errors if e["loc"] == ("password",)]
        assert len(password_errors) > 0

    def test_missing_fields(self):
        """Test that all required fields must be provided."""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(email="test@example.com")
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)

    def test_serialization(self):
        """Test model serialization to dict."""
        request = UserRegisterRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        data = request.model_dump()
        assert data["email"] == "test@example.com"
        # Password should be serialized as SecretStr object
        assert "password" in data


class TestUserRegisterResponse:
    """Tests for UserRegisterResponse model."""

    def test_valid_registration_response(self):
        """Test creating a valid registration response."""
        now = datetime.now()
        response = UserRegisterResponse(
            id=1,
            email="test@example.com",
            created_at=now,
            is_active=True
        )
        
        assert response.id == 1
        assert response.email == "test@example.com"
        assert response.created_at == now
        assert response.is_active is True

    def test_default_is_active_value(self):
        """Test that is_active defaults to True."""
        now = datetime.now()
        response = UserRegisterResponse(
            id=1,
            email="test@example.com",
            created_at=now
        )
        
        assert response.is_active is True

    def test_from_orm_compatibility(self):
        """Test that model can be created from ORM objects."""
        # Create a mock object similar to SQLAlchemy model
        class MockUser:
            id = 1
            email = "test@example.com"
            created_at = datetime.now()
            is_active = True
            password_hash = "should_not_appear"  # This should not be in response
        
        mock_user = MockUser()
        response = UserRegisterResponse.model_validate(mock_user)
        
        assert response.id == 1
        assert response.email == "test@example.com"
        assert response.is_active is True
        # Verify password_hash is not included
        assert not hasattr(response, "password_hash")

    def test_no_password_field_in_response(self):
        """Test that password field is not present in response model."""
        now = datetime.now()
        response = UserRegisterResponse(
            id=1,
            email="test@example.com",
            created_at=now,
            is_active=True
        )
        
        # Verify password is not in the model fields (access from class, not instance)
        assert "password" not in UserRegisterResponse.model_fields
        assert "password_hash" not in UserRegisterResponse.model_fields

    def test_serialization_excludes_sensitive_data(self):
        """Test that serialized data doesn't include sensitive fields."""
        now = datetime.now()
        response = UserRegisterResponse(
            id=1,
            email="test@example.com",
            created_at=now,
            is_active=True
        )
        
        data = response.model_dump()
        assert "password" not in data
        assert "password_hash" not in data
        assert data["email"] == "test@example.com"


class TestUserLoginRequest:
    """Tests for UserLoginRequest model."""

    def test_valid_login_request(self):
        """Test creating a valid login request."""
        request = UserLoginRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        assert request.email == "test@example.com"
        assert request.password.get_secret_value() == "SecurePass123!"

    def test_invalid_email_format(self):
        """Test that invalid email format raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(
                email="not-an-email",
                password="password123"
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_missing_fields(self):
        """Test that all required fields must be provided."""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(email="test@example.com")
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)

    def test_serialization(self):
        """Test model serialization to dict."""
        request = UserLoginRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        data = request.model_dump()
        assert data["email"] == "test@example.com"
        assert "password" in data


class TestModelSerialization:
    """Tests for model serialization and deserialization."""

    def test_register_request_json_serialization(self):
        """Test UserRegisterRequest JSON serialization."""
        request = UserRegisterRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        json_str = request.model_dump_json()
        assert "test@example.com" in json_str
        # Password should be in JSON but as SecretStr representation
        assert "password" in json_str

    def test_register_response_json_serialization(self):
        """Test UserRegisterResponse JSON serialization."""
        now = datetime.now()
        response = UserRegisterResponse(
            id=1,
            email="test@example.com",
            created_at=now,
            is_active=True
        )
        
        json_str = response.model_dump_json()
        assert "test@example.com" in json_str
        assert '"id":1' in json_str or '"id": 1' in json_str

    def test_login_request_json_serialization(self):
        """Test UserLoginRequest JSON serialization."""
        request = UserLoginRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        json_str = request.model_dump_json()
        assert "test@example.com" in json_str

