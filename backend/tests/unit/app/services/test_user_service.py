"""
Unit tests for user registration service.

Tests user creation, password hashing, validation, error handling, and database
transaction management to ensure secure and reliable user registration.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.services.user_service import (
    UserService,
    UserServiceError,
    UserAlreadyExistsError,
    UserCreationError,
)
from app.models.user import User


class TestUserServiceExceptions:
    """Tests for UserService exception classes."""
    
    def test_user_service_error_initialization(self):
        """Test that UserServiceError initializes correctly."""
        error = UserServiceError("Test message", "test_code")
        assert error.message == "Test message"
        assert error.code == "test_code"
        assert str(error) == "Test message"
    
    def test_user_service_error_default_code(self):
        """Test that UserServiceError has default code."""
        error = UserServiceError("Test message")
        assert error.code == "user_service_error"
    
    def test_user_already_exists_error(self):
        """Test that UserAlreadyExistsError formats message correctly."""
        error = UserAlreadyExistsError("test@example.com")
        assert error.email == "test@example.com"
        assert "test@example.com" in error.message
        assert error.code == "user_already_exists"
    
    def test_user_creation_error_default_message(self):
        """Test that UserCreationError has default message."""
        error = UserCreationError()
        assert error.message == "Failed to create user"
        assert error.code == "user_creation_failed"
    
    def test_user_creation_error_custom_message(self):
        """Test that UserCreationError accepts custom message."""
        error = UserCreationError("Custom error message")
        assert error.message == "Custom error message"


class TestPasswordHashing:
    """Tests for password hashing functionality."""
    
    def test_hash_password_returns_string(self):
        """Test that _hash_password returns a string."""
        password = "TestPassword1!"
        password_hash = UserService._hash_password(password)
        
        assert isinstance(password_hash, str)
        assert len(password_hash) > 0
    
    def test_hash_password_returns_different_hashes_with_different_salts(self):
        """Test that hashing the same password twice produces different hashes."""
        password = "TestPassword1!"
        hash1 = UserService._hash_password(password)
        hash2 = UserService._hash_password(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
    
    def test_hash_password_produces_bcrypt_format(self):
        """Test that password hash is in bcrypt format."""
        password = "TestPassword1!"
        password_hash = UserService._hash_password(password)
        
        # Bcrypt hashes start with $2b$ or $2a$ or $2y$
        assert password_hash.startswith("$2")
        # Bcrypt hashes with rounds=12 should contain $12$
        assert "$12$" in password_hash
    
    def test_verify_password_with_correct_password(self):
        """Test that verify_password returns True for correct password."""
        password = "TestPassword1!"
        password_hash = UserService._hash_password(password)
        
        assert UserService.verify_password(password, password_hash) is True
    
    def test_verify_password_with_incorrect_password(self):
        """Test that verify_password returns False for incorrect password."""
        password = "TestPassword1!"
        password_hash = UserService._hash_password(password)
        
        assert UserService.verify_password("WrongPassword1!", password_hash) is False
    
    def test_verify_password_is_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "TestPassword1!"
        password_hash = UserService._hash_password(password)
        
        assert UserService.verify_password("testpassword1!", password_hash) is False


class TestUserServiceInitialization:
    """Tests for UserService initialization."""
    
    def test_user_service_initialization(self):
        """Test that UserService initializes with database session."""
        mock_db = Mock(spec=Session)
        service = UserService(mock_db)
        
        assert service.db == mock_db
    
    def test_bcrypt_rounds_constant(self):
        """Test that BCRYPT_ROUNDS is set to 12."""
        assert UserService.BCRYPT_ROUNDS == 12


class TestRegisterUser:
    """Tests for user registration functionality."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = Mock(spec=Session)
        return db
    
    @pytest.fixture
    def user_service(self, mock_db):
        """Create a UserService instance with mock database."""
        return UserService(mock_db)
    
    def test_register_user_success(self, user_service, mock_db):
        """Test successful user registration."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        # Mock the validators
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            # Configure mock database to return a user after commit
            created_user = User(
                id=1,
                email=email.lower(),
                password_hash="hashed_password",
                is_active=True
            )
            mock_db.refresh = Mock(side_effect=lambda u: setattr(u, 'id', 1))
            
            user = user_service.register_user(email, password)
            
            # Verify database operations
            assert mock_db.add.called
            assert mock_db.commit.called
            assert mock_db.refresh.called
            
            # Verify user was created with correct attributes
            added_user = mock_db.add.call_args[0][0]
            assert added_user.email == email.lower()
            assert added_user.is_active is True
            assert len(added_user.password_hash) > 0
    
    def test_register_user_hashes_password(self, user_service, mock_db):
        """Test that password is hashed during registration."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            mock_db.refresh = Mock()
            user_service.register_user(email, password)
            
            # Get the user that was added
            added_user = mock_db.add.call_args[0][0]
            
            # Verify password is hashed (should be bcrypt format)
            assert added_user.password_hash != password
            assert added_user.password_hash.startswith("$2")
            
            # Verify hashed password can be verified
            assert UserService.verify_password(password, added_user.password_hash)
    
    def test_register_user_sets_active_by_default(self, user_service, mock_db):
        """Test that user is created as active by default (MVP)."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            mock_db.refresh = Mock()
            user_service.register_user(email, password)
            
            # Get the user that was added
            added_user = mock_db.add.call_args[0][0]
            
            # Verify user is active by default
            assert added_user.is_active is True
    
    def test_register_user_normalizes_email(self, user_service, mock_db):
        """Test that email is normalized to lowercase."""
        email = "NewUser@EXAMPLE.COM"
        password = "SecurePass1!"
        normalized_email = "newuser@example.com"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=normalized_email), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            mock_db.refresh = Mock()
            user_service.register_user(email, password)
            
            # Get the user that was added
            added_user = mock_db.add.call_args[0][0]
            
            # Verify email was normalized
            assert added_user.email == normalized_email
    
    def test_register_user_invalid_email_format(self, user_service):
        """Test that invalid email format raises UserServiceError."""
        email = "invalid-email"
        password = "SecurePass1!"
        
        mock_error = Mock()
        mock_error.message = "Invalid email format"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[mock_error]):
            with pytest.raises(UserServiceError) as exc_info:
                user_service.register_user(email, password)
            
            assert exc_info.value.code == "invalid_email"
            assert "Invalid email" in exc_info.value.message
    
    def test_register_user_duplicate_email(self, user_service):
        """Test that duplicate email raises UserAlreadyExistsError."""
        email = "existing@example.com"
        password = "SecurePass1!"
        
        mock_error = Mock()
        mock_error.message = "Email already exists"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[mock_error]):
            
            with pytest.raises(UserAlreadyExistsError) as exc_info:
                user_service.register_user(email, password)
            
            assert exc_info.value.email == email.lower()
    
    def test_register_user_invalid_password(self, user_service):
        """Test that invalid password raises UserServiceError."""
        email = "newuser@example.com"
        password = "weak"
        
        mock_error = Mock()
        mock_error.message = "Password too short"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[mock_error]):
            
            with pytest.raises(UserServiceError) as exc_info:
                user_service.register_user(email, password)
            
            assert exc_info.value.code == "invalid_password"
            assert "Invalid password" in exc_info.value.message
    
    def test_register_user_database_integrity_error(self, user_service, mock_db):
        """Test that IntegrityError during commit triggers rollback and raises UserAlreadyExistsError."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            # Simulate IntegrityError on commit
            mock_db.commit.side_effect = IntegrityError("Duplicate entry", None, None)
            
            with pytest.raises(UserAlreadyExistsError):
                user_service.register_user(email, password)
            
            # Verify rollback was called
            assert mock_db.rollback.called
    
    def test_register_user_database_error(self, user_service, mock_db):
        """Test that SQLAlchemyError during commit triggers rollback and raises UserCreationError."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            # Simulate SQLAlchemyError on commit
            mock_db.commit.side_effect = SQLAlchemyError("Database connection error")
            
            with pytest.raises(UserCreationError) as exc_info:
                user_service.register_user(email, password)
            
            # Verify rollback was called
            assert mock_db.rollback.called
            assert "Database error occurred" in exc_info.value.message
    
    def test_register_user_unexpected_error(self, user_service, mock_db):
        """Test that unexpected errors trigger rollback and raise UserCreationError."""
        email = "newuser@example.com"
        password = "SecurePass1!"
        
        with patch('app.services.user_service.EmailValidator.validate_format', return_value=[]), \
             patch('app.services.user_service.EmailValidator.normalize_email', return_value=email.lower()), \
             patch('app.services.user_service.EmailValidator.check_duplicate', return_value=[]), \
             patch('app.services.user_service.PasswordValidator.validate', return_value=[]):
            
            # Simulate unexpected error on commit
            mock_db.commit.side_effect = RuntimeError("Unexpected error")
            
            with pytest.raises(UserCreationError) as exc_info:
                user_service.register_user(email, password)
            
            # Verify rollback was called
            assert mock_db.rollback.called
            assert "Unexpected error occurred" in exc_info.value.message


class TestGetUserByEmail:
    """Tests for get_user_by_email functionality."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = Mock(spec=Session)
        return db
    
    @pytest.fixture
    def user_service(self, mock_db):
        """Create a UserService instance with mock database."""
        return UserService(mock_db)
    
    def test_get_user_by_email_found(self, user_service, mock_db):
        """Test retrieving an existing user by email."""
        email = "test@example.com"
        expected_user = User(id=1, email=email, password_hash="hash", is_active=True)
        
        # Mock query chain
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = expected_user
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        with patch('app.services.user_service.EmailValidator.normalize_email', return_value=email):
            user = user_service.get_user_by_email(email)
            
            assert user == expected_user
            assert user.email == email
    
    def test_get_user_by_email_not_found(self, user_service, mock_db):
        """Test that None is returned when user doesn't exist."""
        email = "nonexistent@example.com"
        
        # Mock query chain to return None
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        with patch('app.services.user_service.EmailValidator.normalize_email', return_value=email):
            user = user_service.get_user_by_email(email)
            
            assert user is None
    
    def test_get_user_by_email_normalizes_email(self, user_service, mock_db):
        """Test that email is normalized when querying."""
        email = "Test@EXAMPLE.COM"
        normalized_email = "test@example.com"
        
        # Mock query chain
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        with patch('app.services.user_service.EmailValidator.normalize_email', return_value=normalized_email) as mock_normalize:
            user_service.get_user_by_email(email)
            
            # Verify normalize was called with original email
            mock_normalize.assert_called_once_with(email)


class TestGetUserById:
    """Tests for get_user_by_id functionality."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = Mock(spec=Session)
        return db
    
    @pytest.fixture
    def user_service(self, mock_db):
        """Create a UserService instance with mock database."""
        return UserService(mock_db)
    
    def test_get_user_by_id_found(self, user_service, mock_db):
        """Test retrieving an existing user by ID."""
        user_id = 1
        expected_user = User(id=user_id, email="test@example.com", password_hash="hash", is_active=True)
        
        # Mock query chain
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = expected_user
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        user = user_service.get_user_by_id(user_id)
        
        assert user == expected_user
        assert user.id == user_id
    
    def test_get_user_by_id_not_found(self, user_service, mock_db):
        """Test that None is returned when user doesn't exist."""
        user_id = 999
        
        # Mock query chain to return None
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        user = user_service.get_user_by_id(user_id)
        
        assert user is None


# Mark all tests as unit tests
pytestmark = pytest.mark.unit

