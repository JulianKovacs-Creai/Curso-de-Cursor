"""
Unit tests for authentication use cases.

Tests the business logic orchestration in use cases with mocked dependencies.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta

from src.auth.domain.entities import User, UserRole, UserStatus
from src.auth.domain.value_objects import Email, Password, FirstName, LastName, JWTToken, RefreshToken
from src.auth.application.use_cases import (
    RegisterUserUseCase, LoginUserUseCase, LogoutUserUseCase,
    RefreshTokenUseCase, VerifyEmailUseCase, GetUserProfileUseCase, 
    UpdateUserProfileUseCase, ChangePasswordUseCase
)
from src.auth.domain.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError,
    InvalidTokenError, TokenExpiredError, UserNotActiveError,
    EmailNotVerifiedError, InvalidPasswordError, InsufficientPermissionsError
)


class TestRegisterUserUseCase:
    """Test RegisterUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_password_service, mock_email_service):
        """Create use case with mocked dependencies."""
        return RegisterUserUseCase(
            user_repository=mock_user_repository,
            password_service=mock_password_service,
            email_service=mock_email_service
        )
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, use_case, mock_user_repository, mock_password_service, mock_email_service):
        """Test successful user registration."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = False
        mock_password_service.hash_password.return_value = "hashed_password"
        mock_user_repository.save.return_value = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=False
        )
        mock_email_service.send_verification_email.return_value = None
        
        # Create a mock request object
        class MockRequest:
            def __init__(self):
                self.email = "test@example.com"
                self.password = "ValidPass123!"
                self.first_name = "John"
                self.last_name = "Doe"
        
        request = MockRequest()
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert result[0].email == "test@example.com"
        assert result[0].first_name == "John"
        assert result[0].last_name == "Doe"
        assert result[0].role == UserRole.CUSTOMER
        assert result[0].status == UserStatus.ACTIVE
        assert result[0].is_email_verified is False
        assert isinstance(result[1], str)  # Verification token
        
        mock_user_repository.exists_by_email.assert_called_once()
        mock_password_service.hash_password.assert_called_once()
        mock_user_repository.save.assert_called_once()
        mock_email_service.send_verification_email.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_email_already_exists(self, use_case, mock_user_repository):
        """Test registration with existing email raises error."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = True
        
        class MockRequest:
            def __init__(self):
                self.email = "test@example.com"
                self.password = "ValidPass123!"
                self.first_name = "John"
                self.last_name = "Doe"
        
        request = MockRequest()
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="User with email test@example.com already exists"):
            await use_case.execute(request)


class TestLoginUserUseCase:
    """Test LoginUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_password_service, mock_jwt_service):
        """Create use case with mocked dependencies."""
        return LoginUserUseCase(
            user_repository=mock_user_repository,
            password_service=mock_password_service,
            jwt_service=mock_jwt_service
        )
    
    @pytest.mark.asyncio
    async def test_login_user_success(self, use_case, mock_user_repository, mock_password_service, mock_jwt_service):
        """Test successful user login."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_email.return_value = user
        mock_password_service.verify_password.return_value = True
        mock_jwt_service.create_token.return_value = JWTToken("access_token")
        mock_jwt_service.create_refresh_token.return_value = RefreshToken("refresh_token")
        
        # Create a mock request object
        class MockRequest:
            def __init__(self):
                self.email = "test@example.com"
                self.password = "ValidPass123!"
        
        request = MockRequest()
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert result.user == user
        assert result.access_token.value == "access_token"
        assert result.refresh_token.value == "refresh_token"
        
        mock_user_repository.get_by_email.assert_called_once()
        mock_password_service.verify_password.assert_called_once()
        mock_jwt_service.create_token.assert_called_once()
        mock_jwt_service.create_refresh_token.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_user_not_found(self, use_case, mock_user_repository):
        """Test login with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_email.return_value = None
        
        class MockRequest:
            def __init__(self):
                self.email = "nonexistent@example.com"
                self.password = "password"
        
        request = MockRequest()
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            await use_case.execute(request)


class TestLogoutUserUseCase:
    """Test LogoutUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_jwt_service):
        """Create use case with mocked dependencies."""
        return LogoutUserUseCase(jwt_service=mock_jwt_service)
    
    @pytest.mark.asyncio
    async def test_logout_user_success(self, use_case, mock_jwt_service):
        """Test successful user logout."""
        # Arrange
        mock_jwt_service.revoke_token.return_value = None
        
        # Act
        await use_case.execute("access_token")
        
        # Assert
        mock_jwt_service.revoke_token.assert_called_once_with("access_token")


class TestRefreshTokenUseCase:
    """Test RefreshTokenUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_jwt_service):
        """Create use case with mocked dependencies."""
        return RefreshTokenUseCase(
            user_repository=mock_user_repository,
            jwt_service=mock_jwt_service
        )
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, use_case, mock_user_repository, mock_jwt_service):
        """Test successful token refresh."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_jwt_service.verify_refresh_token.return_value = 1
        mock_user_repository.get_by_id.return_value = user
        mock_jwt_service.create_token.return_value = JWTToken("new_access_token")
        mock_jwt_service.create_refresh_token.return_value = RefreshToken("new_refresh_token")
        
        # Act
        result = await use_case.execute("refresh_token")
        
        # Assert
        assert result.user == user
        assert result.access_token.value == "new_access_token"
        assert result.refresh_token.value == "new_refresh_token"
        
        mock_jwt_service.verify_refresh_token.assert_called_once_with("refresh_token")
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_jwt_service.create_token.assert_called_once()
        mock_jwt_service.create_refresh_token.assert_called_once()


class TestGetUserProfileUseCase:
    """Test GetUserProfileUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return GetUserProfileUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_get_user_profile_success(self, use_case, mock_user_repository):
        """Test successful user profile retrieval."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_id.return_value = user
        
        # Act
        result = await use_case.execute(1)
        
        # Assert
        assert result.user == user
        mock_user_repository.get_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_user_profile_not_found(self, use_case, mock_user_repository):
        """Test user profile retrieval with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User not found"):
            await use_case.execute(999)
