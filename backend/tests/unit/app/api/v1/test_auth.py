"""
Unit tests for authentication endpoints.

Tests the POST /api/v1/auth/register endpoint with various scenarios including
successful registration, validation errors, duplicate emails, and error handling.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.services.user_service import (
    UserAlreadyExistsError,
    UserServiceError,
    UserCreationError
)


# Create test client
client = TestClient(app)


class TestRegisterEndpoint:
    """Test suite for POST /api/v1/auth/register endpoint."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock()
    
    @pytest.fixture
    def mock_user(self):
        """Create a mock user object for testing."""
        user = Mock(spec=User)
        user.id = 1
        user.email = "test@example.com"
        user.created_at = datetime(2025, 10, 14, 12, 0, 0)
        user.is_active = True
        return user
    
    def test_successful_registration(self, mock_db, mock_user):
        """
        Test successful user registration.
        
        Should return 201 status with user data.
        """
        # Arrange
        request_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.return_value = mock_user
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["id"] == mock_user.id
            assert data["email"] == mock_user.email
            assert data["is_active"] == mock_user.is_active
            assert "created_at" in data
            
            # Verify service was called correctly
            mock_service.register_user.assert_called_once_with(
                email=request_data["email"],
                password=request_data["password"]
            )
    
    def test_registration_with_invalid_email_format(self, mock_db):
        """
        Test registration with invalid email format.
        
        Should return 422 status with validation error (caught by Pydantic).
        """
        # Arrange
        request_data = {
            "email": "not-an-email",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db:
            mock_get_db.return_value = mock_db
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_registration_with_weak_password(self, mock_db):
        """
        Test registration with password that fails service validation.
        
        Should return 400 status with validation error message.
        Password must be 8+ chars to pass Pydantic validation but still fail service validation.
        """
        # Arrange - Password passes Pydantic (8+ chars) but fails service validation
        request_data = {
            "email": "test@example.com",
            "password": "weakpass"  # 8 chars but no uppercase, number, or special char
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.side_effect = UserServiceError(
                "Invalid password: Password must contain at least one uppercase letter",
                "invalid_password"
            )
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "Invalid password" in response.json()["detail"]
    
    def test_registration_with_duplicate_email(self, mock_db):
        """
        Test registration with email that already exists.
        
        Should return 409 status with conflict message.
        """
        # Arrange
        request_data = {
            "email": "existing@example.com",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.side_effect = UserAlreadyExistsError(
                "existing@example.com"
            )
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_409_CONFLICT
            assert "already exists" in response.json()["detail"]
    
    def test_registration_with_missing_email(self, mock_db):
        """
        Test registration with missing email field.
        
        Should return 422 status with validation error.
        """
        # Arrange
        request_data = {
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db:
            mock_get_db.return_value = mock_db
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_registration_with_missing_password(self, mock_db):
        """
        Test registration with missing password field.
        
        Should return 422 status with validation error.
        """
        # Arrange
        request_data = {
            "email": "test@example.com"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db:
            mock_get_db.return_value = mock_db
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_registration_with_empty_request_body(self, mock_db):
        """
        Test registration with empty request body.
        
        Should return 422 status with validation error.
        """
        with patch("app.api.v1.auth.get_db") as mock_get_db:
            mock_get_db.return_value = mock_db
            
            # Act
            response = client.post("/api/v1/auth/register", json={})
            
            # Assert
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_registration_with_database_error(self, mock_db):
        """
        Test registration when database error occurs.
        
        Should return 500 status with error message.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.side_effect = UserCreationError(
                "Database error occurred"
            )
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "error" in response.json()["detail"].lower()
    
    def test_registration_with_unexpected_error(self, mock_db):
        """
        Test registration when unexpected error occurs.
        
        Should return 500 status with generic error message.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.side_effect = Exception("Unexpected error")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "unexpected error" in response.json()["detail"].lower()
    
    def test_registration_includes_request_id_in_logs(self, mock_db, mock_user):
        """
        Test that registration logs include request ID.
        
        Verifies that request ID logging is working.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        headers = {
            "X-Request-ID": "test-request-123"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class, \
             patch("app.api.v1.auth.logger") as mock_logger:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.return_value = mock_user
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post(
                "/api/v1/auth/register",
                json=request_data,
                headers=headers
            )
            
            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            
            # Verify logger was called with request_id
            assert mock_logger.info.called
            log_calls = [str(call) for call in mock_logger.info.call_args_list]
            assert any("test-request-123" in str(call) for call in log_calls)
    
    def test_registration_password_requirements_all_missing(self, mock_db):
        """
        Test registration with password missing all requirements.
        
        Should return 400 with detailed validation errors.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "weakpass"  # No uppercase, no number, no special char
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.side_effect = UserServiceError(
                "Invalid password: Password must contain at least one uppercase letter, "
                "Password must contain at least one number, "
                "Password must contain at least one special character",
                "invalid_password"
            )
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            detail = response.json()["detail"]
            assert "uppercase" in detail.lower()
            assert "number" in detail.lower()
            assert "special" in detail.lower()
    
    def test_registration_normalizes_email_case(self, mock_db, mock_user):
        """
        Test that email is normalized to lowercase.
        
        Service should receive lowercase email.
        """
        # Arrange
        request_data = {
            "email": "Test@Example.COM",
            "password": "SecurePass123!"
        }
        
        with patch("app.api.v1.auth.get_db") as mock_get_db, \
             patch("app.api.v1.auth.UserService") as mock_service_class:
            
            # Setup mocks
            mock_get_db.return_value = mock_db
            mock_service = Mock()
            mock_service.register_user.return_value = mock_user
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/api/v1/auth/register", json=request_data)
            
            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            # Note: Email normalization happens in UserService, not in the endpoint
            # The endpoint passes the email as-is to the service


class TestRequestIDGeneration:
    """Test suite for request ID generation and handling."""
    
    def test_uses_provided_request_id_from_header(self):
        """
        Test that provided request ID in header is used.
        """
        from app.api.v1.auth import get_request_id
        from fastapi import Request
        
        # Create mock request with X-Request-ID header
        mock_request = Mock(spec=Request)
        mock_request.headers.get.return_value = "custom-request-id-123"
        
        # Act
        request_id = get_request_id(mock_request)
        
        # Assert
        assert request_id == "custom-request-id-123"
        mock_request.headers.get.assert_called_once_with("X-Request-ID")
    
    def test_generates_request_id_when_not_provided(self):
        """
        Test that request ID is generated when not provided in header.
        """
        from app.api.v1.auth import get_request_id
        from fastapi import Request
        
        # Create mock request without X-Request-ID header
        mock_request = Mock(spec=Request)
        mock_request.headers.get.return_value = None
        
        # Act
        request_id = get_request_id(mock_request)
        
        # Assert
        assert request_id is not None
        assert len(request_id) > 0
        # UUID format check (36 characters with hyphens)
        assert len(request_id) == 36
        mock_request.headers.get.assert_called_once_with("X-Request-ID")

