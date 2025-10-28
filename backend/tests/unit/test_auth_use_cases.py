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
    UpdateUserProfileUseCase, ChangePasswordUseCase, DeactivateUserUseCase, 
    ActivateUserUseCase, SuspendUserUseCase, GetUserListUseCase, GetUserByIdUseCase
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
        
        # Act
        result = await use_case.execute(
            email="test@example.com",
            password="ValidPass123!",
            first_name="John",
            last_name="Doe"
        )
        
        # Assert
        assert result.user.email == "test@example.com"
        assert result.user.first_name == "John"
        assert result.user.last_name == "Doe"
        assert result.user.role == UserRole.CUSTOMER
        assert result.user.status == UserStatus.ACTIVE
        assert result.user.is_email_verified is False
        
        mock_user_repository.exists_by_email.assert_called_once_with("test@example.com")
        mock_password_service.hash_password.assert_called_once_with("ValidPass123!")
        mock_user_repository.save.assert_called_once()
        mock_email_service.send_verification_email.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_email_already_exists(self, use_case, mock_user_repository):
        """Test registration with existing email raises error."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = True
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="User with email test@example.com already exists"):
            await use_case.execute(
                email="test@example.com",
                password="ValidPass123!",
                first_name="John",
                last_name="Doe"
            )
    
    @pytest.mark.asyncio
    async def test_register_user_invalid_password(self, use_case, mock_user_repository):
        """Test registration with invalid password raises error."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = False
        
        # Act & Assert
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            await use_case.execute(
                email="test@example.com",
                password="short",
                first_name="John",
                last_name="Doe"
            )


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
        
        # Act
        result = await use_case.execute("test@example.com", "ValidPass123!")
        
        # Assert
        assert result.user == user
        assert result.access_token.value == "access_token"
        assert result.refresh_token.value == "refresh_token"
        
        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_password_service.verify_password.assert_called_once_with("ValidPass123!", "hashed_password")
        mock_jwt_service.create_token.assert_called_once_with(user.id, user.role.value)
        mock_jwt_service.create_refresh_token.assert_called_once_with(user.id)
    
    @pytest.mark.asyncio
    async def test_login_user_not_found(self, use_case, mock_user_repository):
        """Test login with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_email.return_value = None
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            await use_case.execute("nonexistent@example.com", "password")
    
    @pytest.mark.asyncio
    async def test_login_user_invalid_password(self, use_case, mock_user_repository, mock_password_service):
        """Test login with invalid password raises error."""
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
        mock_password_service.verify_password.return_value = False
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            await use_case.execute("test@example.com", "wrong_password")
    
    @pytest.mark.asyncio
    async def test_login_user_not_active(self, use_case, mock_user_repository, mock_password_service):
        """Test login with inactive user raises error."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.INACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_email.return_value = user
        mock_password_service.verify_password.return_value = True
        
        # Act & Assert
        with pytest.raises(UserNotActiveError, match="User account is not active"):
            await use_case.execute("test@example.com", "ValidPass123!")
    
    @pytest.mark.asyncio
    async def test_login_user_email_not_verified(self, use_case, mock_user_repository, mock_password_service):
        """Test login with unverified email raises error."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=False
        )
        mock_user_repository.get_by_email.return_value = user
        mock_password_service.verify_password.return_value = True
        
        # Act & Assert
        with pytest.raises(EmailNotVerifiedError, match="Email address is not verified"):
            await use_case.execute("test@example.com", "ValidPass123!")


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
        mock_jwt_service.create_token.assert_called_once_with(user.id, user.role.value)
        mock_jwt_service.create_refresh_token.assert_called_once_with(user.id)
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, use_case, mock_jwt_service):
        """Test refresh with invalid token raises error."""
        # Arrange
        mock_jwt_service.verify_refresh_token.side_effect = InvalidTokenError("Invalid refresh token")
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Invalid refresh token"):
            await use_case.execute("invalid_token")
    
    @pytest.mark.asyncio
    async def test_refresh_token_user_not_found(self, use_case, mock_user_repository, mock_jwt_service):
        """Test refresh with non-existent user raises error."""
        # Arrange
        mock_jwt_service.verify_refresh_token.return_value = 999
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User not found"):
            await use_case.execute("refresh_token")


class TestVerifyEmailUseCase:
    """Test VerifyEmailUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_jwt_service):
        """Create use case with mocked dependencies."""
        return VerifyEmailUseCase(
            user_repository=mock_user_repository,
            jwt_service=mock_jwt_service
        )
    
    @pytest.mark.asyncio
    async def test_verify_email_success(self, use_case, mock_user_repository, mock_jwt_service):
        """Test successful email verification."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=False
        )
        mock_jwt_service.verify_token.return_value = 1
        mock_user_repository.get_by_id.return_value = user
        mock_user_repository.save.return_value = user.verify_email()
        
        # Act
        result = await use_case.execute("verification_token")
        
        # Assert
        assert result.user.is_email_verified is True
        
        mock_jwt_service.verify_token.assert_called_once_with("verification_token")
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_verify_email_invalid_token(self, use_case, mock_jwt_service):
        """Test email verification with invalid token raises error."""
        # Arrange
        mock_jwt_service.verify_token.side_effect = InvalidTokenError("Invalid token")
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Invalid token"):
            await use_case.execute("invalid_token")


class TestRequestPasswordResetUseCase:
    """Test RequestPasswordResetUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_jwt_service, mock_email_service):
        """Create use case with mocked dependencies."""
        return RequestPasswordResetUseCase(
            user_repository=mock_user_repository,
            jwt_service=mock_jwt_service,
            email_service=mock_email_service
        )
    
    @pytest.mark.asyncio
    async def test_request_password_reset_success(self, use_case, mock_user_repository, mock_jwt_service, mock_email_service):
        """Test successful password reset request."""
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
        mock_jwt_service.create_token.return_value = JWTToken("reset_token")
        mock_email_service.send_password_reset_email.return_value = None
        
        # Act
        await use_case.execute("test@example.com")
        
        # Assert
        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_jwt_service.create_token.assert_called_once()
        mock_email_service.send_password_reset_email.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_request_password_reset_user_not_found(self, use_case, mock_user_repository):
        """Test password reset request with non-existent user."""
        # Arrange
        mock_user_repository.get_by_email.return_value = None
        
        # Act
        await use_case.execute("nonexistent@example.com")
        
        # Assert - Should not raise error for security reasons
        mock_user_repository.get_by_email.assert_called_once_with("nonexistent@example.com")


class TestResetPasswordUseCase:
    """Test ResetPasswordUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_password_service, mock_jwt_service):
        """Create use case with mocked dependencies."""
        return ResetPasswordUseCase(
            user_repository=mock_user_repository,
            password_service=mock_password_service,
            jwt_service=mock_jwt_service
        )
    
    @pytest.mark.asyncio
    async def test_reset_password_success(self, use_case, mock_user_repository, mock_password_service, mock_jwt_service):
        """Test successful password reset."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="old_hash",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_jwt_service.verify_token.return_value = 1
        mock_user_repository.get_by_id.return_value = user
        mock_password_service.hash_password.return_value = "new_hash"
        mock_user_repository.save.return_value = user.update_password("new_hash")
        
        # Act
        result = await use_case.execute("reset_token", "NewPass123!")
        
        # Assert
        assert result.user.password_hash == "new_hash"
        
        mock_jwt_service.verify_token.assert_called_once_with("reset_token")
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_password_service.hash_password.assert_called_once_with("NewPass123!")
        mock_user_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_reset_password_invalid_token(self, use_case, mock_jwt_service):
        """Test password reset with invalid token raises error."""
        # Arrange
        mock_jwt_service.verify_token.side_effect = InvalidTokenError("Invalid token")
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Invalid token"):
            await use_case.execute("invalid_token", "NewPass123!")
    
    @pytest.mark.asyncio
    async def test_reset_password_invalid_password(self, use_case, mock_user_repository, mock_jwt_service):
        """Test password reset with invalid password raises error."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="old_hash",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_jwt_service.verify_token.return_value = 1
        mock_user_repository.get_by_id.return_value = user
        
        # Act & Assert
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            await use_case.execute("reset_token", "short")


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


class TestUpdateUserProfileUseCase:
    """Test UpdateUserProfileUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return UpdateUserProfileUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_update_user_profile_success(self, use_case, mock_user_repository):
        """Test successful user profile update."""
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
        updated_user = user.update_profile("Jane", "Smith")
        mock_user_repository.save.return_value = updated_user
        
        # Act
        result = await use_case.execute(1, "Jane", "Smith")
        
        # Assert
        assert result.user.first_name == "Jane"
        assert result.user.last_name == "Smith"
        
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_user_profile_not_found(self, use_case, mock_user_repository):
        """Test user profile update with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User not found"):
            await use_case.execute(999, "Jane", "Smith")


class TestChangePasswordUseCase:
    """Test ChangePasswordUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_password_service):
        """Create use case with mocked dependencies."""
        return ChangePasswordUseCase(
            user_repository=mock_user_repository,
            password_service=mock_password_service
        )
    
    @pytest.mark.asyncio
    async def test_change_password_success(self, use_case, mock_user_repository, mock_password_service):
        """Test successful password change."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="old_hash",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_id.return_value = user
        mock_password_service.verify_password.return_value = True
        mock_password_service.hash_password.return_value = "new_hash"
        updated_user = user.update_password("new_hash")
        mock_user_repository.save.return_value = updated_user
        
        # Act
        result = await use_case.execute(1, "OldPass123!", "NewPass123!")
        
        # Assert
        assert result.user.password_hash == "new_hash"
        
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_password_service.verify_password.assert_called_once_with("OldPass123!", "old_hash")
        mock_password_service.hash_password.assert_called_once_with("NewPass123!")
        mock_user_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_change_password_invalid_current_password(self, use_case, mock_user_repository, mock_password_service):
        """Test password change with invalid current password raises error."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="old_hash",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_id.return_value = user
        mock_password_service.verify_password.return_value = False
        
        # Act & Assert
        with pytest.raises(InvalidPasswordError, match="Current password is incorrect"):
            await use_case.execute(1, "WrongPass123!", "NewPass123!")
    
    @pytest.mark.asyncio
    async def test_change_password_same_password(self, use_case, mock_user_repository, mock_password_service):
        """Test password change with same password raises error."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="old_hash",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_id.return_value = user
        mock_password_service.verify_password.return_value = True
        
        # Act & Assert
        with pytest.raises(InvalidPasswordError, match="New password must be different from current password"):
            await use_case.execute(1, "OldPass123!", "OldPass123!")


class TestDeactivateUserUseCase:
    """Test DeactivateUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return DeactivateUserUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_deactivate_user_success(self, use_case, mock_user_repository):
        """Test successful user deactivation."""
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
        deactivated_user = user.deactivate()
        mock_user_repository.save.return_value = deactivated_user
        
        # Act
        result = await use_case.execute(1)
        
        # Assert
        assert result.user.status == UserStatus.INACTIVE
        
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_deactivate_user_not_found(self, use_case, mock_user_repository):
        """Test user deactivation with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User not found"):
            await use_case.execute(999)


class TestActivateUserUseCase:
    """Test ActivateUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return ActivateUserUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_activate_user_success(self, use_case, mock_user_repository):
        """Test successful user activation."""
        # Arrange
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.INACTIVE,
            is_email_verified=True
        )
        mock_user_repository.get_by_id.return_value = user
        activated_user = user.activate()
        mock_user_repository.save.return_value = activated_user
        
        # Act
        result = await use_case.execute(1)
        
        # Assert
        assert result.user.status == UserStatus.ACTIVE
        
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()


class TestSuspendUserUseCase:
    """Test SuspendUserUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return SuspendUserUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_suspend_user_success(self, use_case, mock_user_repository):
        """Test successful user suspension."""
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
        suspended_user = user.suspend()
        mock_user_repository.save.return_value = suspended_user
        
        # Act
        result = await use_case.execute(1)
        
        # Assert
        assert result.user.status == UserStatus.SUSPENDED
        
        mock_user_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()


class TestGetUserListUseCase:
    """Test GetUserListUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return GetUserListUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_get_user_list_success(self, use_case, mock_user_repository):
        """Test successful user list retrieval."""
        # Arrange
        users = [
            User(
                id=1,
                email="user1@example.com",
                password_hash="hash1",
                first_name="User",
                last_name="One",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            ),
            User(
                id=2,
                email="user2@example.com",
                password_hash="hash2",
                first_name="User",
                last_name="Two",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            )
        ]
        mock_user_repository.find_all.return_value = users
        mock_user_repository.count.return_value = 2
        
        # Act
        result = await use_case.execute(page=1, page_size=10)
        
        # Assert
        assert len(result.users) == 2
        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 10
        
        mock_user_repository.find_all.assert_called_once_with(offset=0, limit=10)
        mock_user_repository.count.assert_called_once()


class TestGetUserByIdUseCase:
    """Test GetUserByIdUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_user_repository):
        """Create use case with mocked dependencies."""
        return GetUserByIdUseCase(user_repository=mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, use_case, mock_user_repository):
        """Test successful user retrieval by ID."""
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
    async def test_get_user_by_id_not_found(self, use_case, mock_user_repository):
        """Test user retrieval by ID with non-existent user raises error."""
        # Arrange
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User not found"):
            await use_case.execute(999)
