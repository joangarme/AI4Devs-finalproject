"""
Integration tests for user service with real database.

Tests user service with actual database operations to ensure
proper integration with SQLAlchemy and database constraints.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.services.user_service import (
    UserService,
    UserServiceError,
    UserAlreadyExistsError,
    UserCreationError,
)


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh in-memory SQLite database for each test.
    
    This ensures complete isolation between tests and fast execution.
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_service(test_db):
    """Create a UserService instance with real database session."""
    return UserService(test_db)


class TestUserServiceIntegration:
    """Integration tests for UserService with real database."""
    
    def test_register_user_creates_database_record(self, user_service, test_db):
        """Test that register_user creates an actual database record."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Register user
        user = user_service.register_user(email, password)
        
        # Verify user has ID (was persisted)
        assert user.id is not None
        assert user.id > 0
        
        # Query database directly to verify
        db_user = test_db.query(User).filter(User.email == email).first()
        assert db_user is not None
        assert db_user.email == email
        assert db_user.is_active is True
    
    def test_register_user_password_is_hashed(self, user_service, test_db):
        """Test that password is properly hashed in database."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Register user
        user = user_service.register_user(email, password)
        
        # Verify password is hashed, not stored in plain text
        db_user = test_db.query(User).filter(User.email == email).first()
        assert db_user.password_hash != password
        assert db_user.password_hash.startswith("$2")  # bcrypt format
        
        # Verify password can be verified
        assert UserService.verify_password(password, db_user.password_hash)
    
    def test_register_user_active_by_default(self, user_service, test_db):
        """Test that users are created as active by default (MVP)."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Register user
        user = user_service.register_user(email, password)
        
        # Verify user is active in database
        db_user = test_db.query(User).filter(User.id == user.id).first()
        assert db_user.is_active is True
    
    def test_register_user_duplicate_email_prevented_by_constraint(self, user_service):
        """Test that database constraint prevents duplicate emails."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Register first user
        user_service.register_user(email, password)
        
        # Attempt to register with same email
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            user_service.register_user(email, password)
        
        assert exc_info.value.email == email
    
    def test_register_user_duplicate_email_case_insensitive(self, user_service):
        """Test that duplicate email check is case-insensitive."""
        email_lower = "test@example.com"
        email_upper = "TEST@EXAMPLE.COM"
        password = "SecurePass1!"
        
        # Register with lowercase email
        user_service.register_user(email_lower, password)
        
        # Attempt to register with uppercase email
        with pytest.raises(UserAlreadyExistsError):
            user_service.register_user(email_upper, password)
    
    def test_register_user_invalid_email_format(self, user_service):
        """Test that invalid email format is rejected."""
        invalid_email = "not-an-email"
        password = "SecurePass1!"
        
        with pytest.raises(UserServiceError) as exc_info:
            user_service.register_user(invalid_email, password)
        
        assert exc_info.value.code == "invalid_email"
    
    def test_register_user_invalid_password_too_short(self, user_service):
        """Test that password shorter than 8 characters is rejected."""
        email = "test@example.com"
        password = "Short1!"  # 7 characters
        
        with pytest.raises(UserServiceError) as exc_info:
            user_service.register_user(email, password)
        
        assert exc_info.value.code == "invalid_password"
    
    def test_register_user_invalid_password_no_uppercase(self, user_service):
        """Test that password without uppercase letter is rejected."""
        email = "test@example.com"
        password = "lowercase1!"
        
        with pytest.raises(UserServiceError) as exc_info:
            user_service.register_user(email, password)
        
        assert exc_info.value.code == "invalid_password"
    
    def test_register_user_invalid_password_no_number(self, user_service):
        """Test that password without number is rejected."""
        email = "test@example.com"
        password = "NoNumbers!"
        
        with pytest.raises(UserServiceError) as exc_info:
            user_service.register_user(email, password)
        
        assert exc_info.value.code == "invalid_password"
    
    def test_register_user_invalid_password_no_special_char(self, user_service):
        """Test that password without special character is rejected."""
        email = "test@example.com"
        password = "NoSpecial1"
        
        with pytest.raises(UserServiceError) as exc_info:
            user_service.register_user(email, password)
        
        assert exc_info.value.code == "invalid_password"
    
    def test_register_multiple_users(self, user_service, test_db):
        """Test that multiple users can be registered successfully."""
        users_data = [
            ("user1@example.com", "Password1!"),
            ("user2@example.com", "Password2!"),
            ("user3@example.com", "Password3!"),
        ]
        
        created_users = []
        for email, password in users_data:
            user = user_service.register_user(email, password)
            created_users.append(user)
        
        # Verify all users were created
        assert len(created_users) == 3
        
        # Verify all users are in database
        db_users = test_db.query(User).all()
        assert len(db_users) == 3
        
        # Verify each user has unique ID
        user_ids = [u.id for u in created_users]
        assert len(set(user_ids)) == 3
    
    def test_get_user_by_email_returns_user(self, user_service, test_db):
        """Test that get_user_by_email returns the correct user."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Create user
        created_user = user_service.register_user(email, password)
        
        # Retrieve user by email
        retrieved_user = user_service.get_user_by_email(email)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == email
    
    def test_get_user_by_email_case_insensitive(self, user_service, test_db):
        """Test that get_user_by_email is case-insensitive."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Create user with lowercase email
        user_service.register_user(email, password)
        
        # Retrieve with uppercase email
        retrieved_user = user_service.get_user_by_email("TEST@EXAMPLE.COM")
        
        assert retrieved_user is not None
        assert retrieved_user.email == email
    
    def test_get_user_by_email_not_found(self, user_service):
        """Test that get_user_by_email returns None for non-existent user."""
        retrieved_user = user_service.get_user_by_email("nonexistent@example.com")
        assert retrieved_user is None
    
    def test_get_user_by_id_returns_user(self, user_service, test_db):
        """Test that get_user_by_id returns the correct user."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Create user
        created_user = user_service.register_user(email, password)
        
        # Retrieve user by ID
        retrieved_user = user_service.get_user_by_id(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == email
    
    def test_get_user_by_id_not_found(self, user_service):
        """Test that get_user_by_id returns None for non-existent user."""
        retrieved_user = user_service.get_user_by_id(99999)
        assert retrieved_user is None
    
    def test_user_timestamps_are_set(self, user_service, test_db):
        """Test that created_at and updated_at timestamps are set."""
        email = "test@example.com"
        password = "SecurePass1!"
        
        # Create user
        user = user_service.register_user(email, password)
        
        # Verify timestamps are set
        db_user = test_db.query(User).filter(User.id == user.id).first()
        assert db_user.created_at is not None
        assert db_user.updated_at is not None


# Mark all tests as integration tests
pytestmark = pytest.mark.integration

