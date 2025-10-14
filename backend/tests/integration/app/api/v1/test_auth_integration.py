"""
Integration tests for authentication endpoints.

These tests use a real database connection to verify the complete registration
flow including database operations, validation, and error handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User


# Create in-memory SQLite database for testing
# Using StaticPool to maintain the same connection across threads
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test.
    
    Creates all tables before the test and drops them after.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for the test
    session = TestingSessionLocal()
    
    yield session
    
    # Cleanup after test
    session.close()
    Base.metadata.drop_all(bind=engine)


class TestRegisterEndpointIntegration:
    """Integration test suite for POST /api/v1/auth/register endpoint."""
    
    def test_successful_registration_creates_user_in_database(self, db: Session):
        """
        Test successful registration creates user in database.
        
        Verifies that:
        - User is created with correct data
        - Password is hashed (not stored in plain text)
        - User is active by default
        - Response contains correct user data
        """
        # Arrange
        request_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert response
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == request_data["email"]
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password should not be in response
        
        # Verify user exists in database
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
        assert user.email == request_data["email"]
        assert user.is_active is True
        
        # Verify password is hashed (not plain text)
        assert user.password_hash != request_data["password"]
        assert len(user.password_hash) == 60  # Bcrypt hash length
        assert user.password_hash.startswith("$2b$")  # Bcrypt prefix
    
    def test_duplicate_email_returns_409(self, db: Session):
        """
        Test registration with duplicate email returns 409 Conflict.
        
        Verifies that:
        - First registration succeeds
        - Second registration with same email fails with 409
        - Only one user exists in database
        """
        # Arrange
        request_data = {
            "email": "duplicate@example.com",
            "password": "SecurePass123!"
        }
        
        # Act - First registration
        response1 = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert first registration succeeded
        assert response1.status_code == 201
        
        # Act - Second registration with same email
        response2 = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert second registration failed
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"]
        
        # Verify only one user exists in database
        user_count = db.query(User).filter(User.email == request_data["email"]).count()
        assert user_count == 1
    
    def test_case_insensitive_email_duplicate_check(self, db: Session):
        """
        Test duplicate email check is case-insensitive.
        
        Verifies that emails are normalized to lowercase and duplicate
        check works regardless of case.
        """
        # Arrange
        request_data_1 = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        request_data_2 = {
            "email": "User@Example.COM",
            "password": "SecurePass123!"
        }
        
        # Act - First registration with lowercase
        response1 = client.post("/api/v1/auth/register", json=request_data_1)
        
        # Assert first registration succeeded
        assert response1.status_code == 201
        
        # Act - Second registration with uppercase
        response2 = client.post("/api/v1/auth/register", json=request_data_2)
        
        # Assert second registration failed (duplicate detected)
        assert response2.status_code == 409
        
        # Verify email is stored in lowercase
        user = db.query(User).filter(User.email == "user@example.com").first()
        assert user is not None
        assert user.email == "user@example.com"
    
    def test_invalid_email_format_returns_422(self, db: Session):
        """
        Test registration with invalid email format returns 422.
        
        Pydantic validation should catch invalid email format.
        """
        # Arrange
        request_data = {
            "email": "not-an-email",
            "password": "SecurePass123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 422
        
        # Verify no user was created
        user_count = db.query(User).count()
        assert user_count == 0
    
    def test_password_too_short_returns_422(self, db: Session):
        """
        Test registration with short password returns 422.
        
        Password must be at least 8 characters (caught by Pydantic validation).
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "Short1!"  # Only 7 chars - fails Pydantic validation
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert - Pydantic catches this before service validation
        assert response.status_code == 422
        
        # Verify no user was created
        user_count = db.query(User).count()
        assert user_count == 0
    
    def test_password_missing_uppercase_returns_400(self, db: Session):
        """
        Test registration with password missing uppercase returns 400.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "securepass123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "password" in detail
        assert "uppercase" in detail
        
        # Verify no user was created
        user_count = db.query(User).count()
        assert user_count == 0
    
    def test_password_missing_number_returns_400(self, db: Session):
        """
        Test registration with password missing number returns 400.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "password" in detail
        assert "number" in detail
        
        # Verify no user was created
        user_count = db.query(User).count()
        assert user_count == 0
    
    def test_password_missing_special_character_returns_400(self, db: Session):
        """
        Test registration with password missing special character returns 400.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "password" in detail
        assert "special" in detail
        
        # Verify no user was created
        user_count = db.query(User).count()
        assert user_count == 0
    
    def test_multiple_users_can_register(self, db: Session):
        """
        Test multiple users can register successfully.
        
        Verifies that multiple users can be created with different emails.
        """
        # Arrange
        users = [
            {"email": "user1@example.com", "password": "SecurePass123!"},
            {"email": "user2@example.com", "password": "SecurePass456!"},
            {"email": "user3@example.com", "password": "SecurePass789!"},
        ]
        
        # Act - Register all users
        responses = []
        for user_data in users:
            response = client.post("/api/v1/auth/register", json=user_data)
            responses.append(response)
        
        # Assert all registrations succeeded
        for response in responses:
            assert response.status_code == 201
        
        # Verify all users exist in database
        user_count = db.query(User).count()
        assert user_count == len(users)
        
        # Verify each email exists
        for user_data in users:
            user = db.query(User).filter(User.email == user_data["email"]).first()
            assert user is not None
            assert user.is_active is True
    
    def test_registration_with_request_id_header(self, db: Session):
        """
        Test registration with custom request ID header.
        
        Verifies that custom request ID is accepted and used.
        """
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        headers = {
            "X-Request-ID": "custom-request-id-123"
        }
        
        # Act
        response = client.post(
            "/api/v1/auth/register",
            json=request_data,
            headers=headers
        )
        
        # Assert
        assert response.status_code == 201
        
        # Verify user was created
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
    
    def test_registration_transaction_rollback_on_error(self, db: Session):
        """
        Test that database transaction is rolled back on error.
        
        This test is more of a sanity check since the UserService
        already handles transaction rollback.
        """
        # Arrange - Invalid password to trigger service validation error
        # Must be 8+ chars to pass Pydantic but fail service validation
        request_data = {
            "email": "test@example.com",
            "password": "weakpass"  # 8 chars but no uppercase, number, special char
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert - Service validation returns 400
        assert response.status_code == 400
        
        # Verify no user was created (transaction rolled back)
        user_count = db.query(User).count()
        assert user_count == 0


class TestRegisterEndpointEdgeCases:
    """Edge case tests for registration endpoint."""
    
    def test_registration_with_very_long_email(self, db: Session):
        """
        Test registration with very long email address.
        
        Should succeed if email is valid (within database limits).
        """
        # Arrange - Create a long but valid email
        long_local_part = "a" * 50
        request_data = {
            "email": f"{long_local_part}@example.com",
            "password": "SecurePass123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 201
        
        # Verify user was created
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
    
    def test_registration_with_special_characters_in_email(self, db: Session):
        """
        Test registration with special characters in email.
        
        Valid email addresses can contain special characters.
        """
        # Arrange
        request_data = {
            "email": "user+tag@example.com",
            "password": "SecurePass123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 201
        
        # Verify user was created
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
    
    def test_registration_with_minimum_valid_password(self, db: Session):
        """
        Test registration with minimum valid password.
        
        Password that just meets all requirements should succeed.
        """
        # Arrange - Exactly 8 chars with all requirements
        request_data = {
            "email": "test@example.com",
            "password": "Abcdef1!"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 201
        
        # Verify user was created
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
    
    def test_registration_with_very_long_password(self, db: Session):
        """
        Test registration with very long password.
        
        Should succeed and properly hash the long password.
        """
        # Arrange - Very long password
        request_data = {
            "email": "test@example.com",
            "password": "SecurePass123!" * 10  # 140 characters
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=request_data)
        
        # Assert
        assert response.status_code == 201
        
        # Verify user was created with hashed password
        user = db.query(User).filter(User.email == request_data["email"]).first()
        assert user is not None
        assert len(user.password_hash) == 60  # Bcrypt always produces 60 char hash

