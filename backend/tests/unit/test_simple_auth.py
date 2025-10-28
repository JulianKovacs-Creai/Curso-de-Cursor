"""
Simple authentication tests that only test what we have implemented.
"""

import pytest
from unittest.mock import Mock

from src.auth.domain.entities import User, UserRole, UserStatus
from src.auth.domain.value_objects import Email, Password, FirstName, LastName
from src.auth.application.use_cases import (
    RegisterUserUseCase, LoginUserUseCase, LogoutUserUseCase, VerifyEmailUseCase
)
from src.auth.infrastructure.password_service import PasswordService
from src.auth.infrastructure.jwt_service import JWTService


class TestSimpleAuth:
    """Simple authentication tests"""
    
    def test_register_user_success(self):
        """Test successful user registration"""
        # Mock dependencies
        mock_repo = Mock()
        mock_repo.get_user_by_email.return_value = None
        
        # Create a mock user to return from create_user
        mock_user = Mock()
        mock_user.id.value = "user_12345678"
        mock_user.email.value = "test@example.com"
        mock_repo.create_user.return_value = mock_user
        
        password_service = Mock()
        password_service.is_password_strong.return_value = True
        password_service.hash_password.return_value = "hashed_password"
        
        # Create use case
        use_case = RegisterUserUseCase(mock_repo, password_service)
        
        # Execute
        result = use_case.execute("test@example.com", "StrongPassword123!", "John", "Doe")
        
        # Assertions
        assert result["user_id"] == "user_12345678"
        assert result["email"] == "test@example.com"
        assert result["message"] == "User registered successfully"
        mock_repo.create_user.assert_called_once()
    
    def test_register_user_already_exists(self):
        """Test registration when user already exists"""
        # Mock dependencies
        mock_repo = Mock()
        existing_user = User(
            id=Mock(value="123"),
            email=Email("test@example.com"),
            hashed_password="hashed",
            first_name="John",
            last_name="Doe"
        )
        mock_repo.get_user_by_email.return_value = existing_user
        
        password_service = Mock()
        password_service.is_password_strong.return_value = True
        
        # Create use case
        use_case = RegisterUserUseCase(mock_repo, password_service)
        
        # Execute and assert
        with pytest.raises(ValueError, match="User with this email already exists"):
            use_case.execute("test@example.com", "StrongPassword123!", "John", "Doe")
    
    def test_login_user_success(self):
        """Test successful user login"""
        # Mock dependencies
        mock_repo = Mock()
        user = User(
            id=Mock(value="123"),
            email=Email("test@example.com"),
            hashed_password="hashed_password",
            first_name="John",
            last_name="Doe"
        )
        mock_repo.get_user_by_email.return_value = user
        
        password_service = Mock()
        password_service.verify_password.return_value = True
        
        jwt_service = Mock()
        jwt_service.create_token_pair.return_value = {
            "access_token": "jwt_token",
            "refresh_token": "refresh_token",
            "token_type": "bearer"
        }
        
        # Create use case
        use_case = LoginUserUseCase(mock_repo, password_service, jwt_service)
        
        # Execute
        result = use_case.execute("test@example.com", "password123")
        
        # Assertions
        assert result["access_token"] == "jwt_token"
        assert result["refresh_token"] == "refresh_token"
        assert result["token_type"] == "bearer"
        assert result["user"]["email"] == "test@example.com"
    
    def test_logout_user_success(self):
        """Test successful user logout"""
        # Mock dependencies
        jwt_service = Mock()
        jwt_service.validate_token.return_value = {"sub": "123"}
        
        # Create use case
        use_case = LogoutUserUseCase(jwt_service)
        
        # Execute
        result = use_case.execute("valid_token")
        
        # Assertions
        assert result["success"] is True
        assert result["message"] == "User logged out successfully"
    
    def test_verify_email_success(self):
        """Test successful email verification"""
        # Mock dependencies
        mock_repo = Mock()
        user = User(
            id=Mock(value="123"),
            email=Email("test@example.com"),
            hashed_password="hashed",
            first_name="John",
            last_name="Doe"
        )
        mock_repo.get_user_by_email.return_value = user
        mock_repo.update_user.return_value = None
        
        # Create use case
        use_case = VerifyEmailUseCase(mock_repo)
        
        # Execute
        result = use_case.execute("test@example.com", "verification_code")
        
        # Assertions
        assert result["success"] is True
        assert result["message"] == "Email verified successfully"
        assert user.is_verified is True
        mock_repo.update_user.assert_called_once_with(user)
