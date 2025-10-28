"""
Comprehensive Unit Tests - Authentication Examples

This module contains comprehensive unit tests with high coverage
for all authentication components.

Target: >85% coverage with comprehensive unit testing
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from jwt_service_example import (
    JWTService, JWTToken, JWTServiceError, InvalidTokenError, TokenExpiredError
)
from user_repository_example import (
    UserRepository, User, UserRepositoryError, UserAlreadyExistsError, UserNotFoundError
)
from complete_auth_example import AuthenticationService


class TestJWTServiceComprehensive:
    """Comprehensive unit tests for JWT service"""
    
    @pytest.mark.unit
    def test_jwt_service_initialization(self):
        """Test JWT service initialization with various parameters."""
        # Test default initialization
        service = JWTService("secret-key")
        assert service.secret_key == "secret-key"
        assert service.algorithm == "HS256"
        assert service.access_token_expire_hours == 1
        
        # Test custom initialization
        service = JWTService("secret-key", "HS512", 2)
        assert service.algorithm == "HS512"
        assert service.access_token_expire_hours == 2
    
    @pytest.mark.unit
    def test_create_token_success(self, jwt_service):
        """Test successful token creation."""
        token = jwt_service.create_token(1, "test@example.com", "customer")
        
        assert isinstance(token, JWTToken)
        assert token.value is not None
        assert len(token.value) > 0
        assert token.token_type == "Bearer"
    
    @pytest.mark.unit
    def test_create_token_with_custom_expiration(self, jwt_service):
        """Test token creation with custom expiration."""
        custom_delta = timedelta(hours=2)
        token = jwt_service.create_token(1, "test@example.com", "customer", custom_delta)
        
        # Verify token is created
        assert isinstance(token, JWTToken)
        
        # Verify token payload
        payload = jwt_service.verify_token(token)
        assert payload["user_id"] == 1
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "customer"
    
    @pytest.mark.unit
    def test_create_token_with_invalid_parameters(self, jwt_service):
        """Test token creation with invalid parameters."""
        # Test with None values
        with pytest.raises(Exception):
            jwt_service.create_token(None, "test@example.com", "customer")
        
        # Test with empty string
        with pytest.raises(Exception):
            jwt_service.create_token(1, "", "customer")
    
    @pytest.mark.unit
    def test_verify_token_success(self, jwt_token, jwt_service):
        """Test successful token verification."""
        payload = jwt_service.verify_token(jwt_token)
        
        assert payload["user_id"] == 1
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "customer"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    @pytest.mark.unit
    def test_verify_token_invalid_format(self, jwt_service):
        """Test verification of invalid token format."""
        invalid_tokens = [
            "invalid.token",
            "not.a.jwt.token",
            "",
            "single",
            "two.parts",
            "too.many.parts.here.extra"
        ]
        
        for invalid_token in invalid_tokens:
            with pytest.raises(InvalidTokenError):
                jwt_service.verify_token(JWTToken(invalid_token))
    
    @pytest.mark.unit
    def test_verify_token_expired(self, expired_jwt_token, jwt_service):
        """Test verification of expired token."""
        with pytest.raises(TokenExpiredError):
            jwt_service.verify_token(expired_jwt_token)
    
    @pytest.mark.unit
    def test_verify_token_revoked(self, jwt_token, jwt_service):
        """Test verification of revoked token."""
        # Revoke token
        jwt_service.revoke_token(jwt_token)
        
        # Should raise exception
        with pytest.raises(InvalidTokenError):
            jwt_service.verify_token(jwt_token)
    
    @pytest.mark.unit
    def test_hash_password_success(self, jwt_service):
        """Test successful password hashing."""
        password = "TestPassword123!"
        hashed = jwt_service.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60  # bcrypt hash length
    
    @pytest.mark.unit
    def test_hash_password_different_salts(self, jwt_service):
        """Test that different salts are generated."""
        password = "TestPassword123!"
        hash1 = jwt_service.hash_password(password)
        hash2 = jwt_service.hash_password(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
    
    @pytest.mark.unit
    def test_hash_password_empty_string(self, jwt_service):
        """Test password hashing with empty string."""
        with pytest.raises(Exception):
            jwt_service.hash_password("")
    
    @pytest.mark.unit
    def test_verify_password_success(self, jwt_service):
        """Test successful password verification."""
        password = "TestPassword123!"
        hashed = jwt_service.hash_password(password)
        
        assert jwt_service.verify_password(password, hashed) is True
    
    @pytest.mark.unit
    def test_verify_password_wrong_password(self, jwt_service):
        """Test password verification with wrong password."""
        password = "TestPassword123!"
        hashed = jwt_service.hash_password(password)
        
        assert jwt_service.verify_password("WrongPassword", hashed) is False
    
    @pytest.mark.unit
    def test_verify_password_invalid_hash(self, jwt_service):
        """Test password verification with invalid hash."""
        password = "TestPassword123!"
        invalid_hash = "invalid_hash"
        
        with pytest.raises(JWTServiceError):
            jwt_service.verify_password(password, invalid_hash)
    
    @pytest.mark.unit
    def test_create_refresh_token_success(self, jwt_service):
        """Test successful refresh token creation."""
        refresh_token = jwt_service.create_refresh_token(1)
        
        assert isinstance(refresh_token, str)
        assert len(refresh_token) == 64
        assert refresh_token.isalnum()
    
    @pytest.mark.unit
    def test_create_refresh_token_different_tokens(self, jwt_service):
        """Test that different refresh tokens are generated."""
        token1 = jwt_service.create_refresh_token(1)
        token2 = jwt_service.create_refresh_token(1)
        
        assert token1 != token2
    
    @pytest.mark.unit
    def test_revoke_token_success(self, jwt_token, jwt_service):
        """Test successful token revocation."""
        result = jwt_service.revoke_token(jwt_token)
        
        assert result is True
        assert jwt_service.is_token_revoked(jwt_token) is True
    
    @pytest.mark.unit
    def test_revoke_token_multiple_times(self, jwt_token, jwt_service):
        """Test revoking the same token multiple times."""
        # First revocation
        result1 = jwt_service.revoke_token(jwt_token)
        assert result1 is True
        
        # Second revocation should still work
        result2 = jwt_service.revoke_token(jwt_token)
        assert result2 is True
    
    @pytest.mark.unit
    def test_is_token_revoked_false(self, jwt_token, jwt_service):
        """Test checking non-revoked token."""
        assert jwt_service.is_token_revoked(jwt_token) is False
    
    @pytest.mark.unit
    def test_is_token_revoked_true(self, jwt_token, jwt_service):
        """Test checking revoked token."""
        jwt_service.revoke_token(jwt_token)
        assert jwt_service.is_token_revoked(jwt_token) is True
    
    @pytest.mark.unit
    def test_jwt_token_value_object_validation(self):
        """Test JWT token value object validation."""
        # Valid token
        token = JWTToken("valid.jwt.token")
        assert token.value == "valid.jwt.token"
        assert token.token_type == "Bearer"
        
        # Invalid token format
        with pytest.raises(ValueError):
            JWTToken("invalid")
        
        # Empty token
        with pytest.raises(ValueError):
            JWTToken("")
    
    @pytest.mark.unit
    def test_jwt_token_authorization_header(self):
        """Test JWT token authorization header format."""
        token = JWTToken("valid.jwt.token")
        assert token.authorization_header == "Bearer valid.jwt.token"


class TestUserRepositoryComprehensive:
    """Comprehensive unit tests for User Repository"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_user_repository_initialization(self, temp_database):
        """Test user repository initialization."""
        repo = UserRepository(temp_database)
        assert repo.database_path == temp_database
        
        # Verify database was created
        import os
        assert os.path.exists(temp_database)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_repository):
        """Test successful user creation."""
        user = await user_repository.create_user(
            "test@example.com",
            "$2b$12$example_hash",
            "John",
            "Doe"
        )
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.password_hash == "$2b$12$example_hash"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.created_at is not None
        assert user.full_name == "John Doe"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, user_repository):
        """Test creating user with duplicate email."""
        # Create first user
        await user_repository.create_user("test@example.com", "hash1", "John", "Doe")
        
        # Try to create duplicate
        with pytest.raises(UserAlreadyExistsError):
            await user_repository.create_user("test@example.com", "hash2", "Jane", "Smith")
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_create_user_invalid_data(self, user_repository):
        """Test creating user with invalid data."""
        # Empty email
        with pytest.raises(ValueError):
            await user_repository.create_user("", "hash", "John", "Doe")
        
        # Empty first name
        with pytest.raises(ValueError):
            await user_repository.create_user("test@example.com", "hash", "", "Doe")
        
        # Empty last name
        with pytest.raises(ValueError):
            await user_repository.create_user("test@example.com", "hash", "John", "")
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, user_repository):
        """Test successful user retrieval by email."""
        # Create user
        created_user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Retrieve user
        retrieved_user = await user_repository.get_user_by_email("test@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "test@example.com"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, user_repository):
        """Test retrieving non-existent user by email."""
        user = await user_repository.get_user_by_email("nonexistent@example.com")
        assert user is None
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_repository):
        """Test successful user retrieval by ID."""
        # Create user
        created_user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Retrieve user
        retrieved_user = await user_repository.get_user_by_id(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "test@example.com"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, user_repository):
        """Test retrieving non-existent user by ID."""
        user = await user_repository.get_user_by_id(999)
        assert user is None
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_user_success(self, user_repository):
        """Test successful user update."""
        # Create user
        user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Update user
        updated_user = await user_repository.update_user(
            user.id,
            {"first_name": "Johnny", "last_name": "Smith"}
        )
        
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.first_name == "Johnny"
        assert updated_user.last_name == "Smith"
        assert updated_user.full_name == "Johnny Smith"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_repository):
        """Test updating non-existent user."""
        updated_user = await user_repository.update_user(
            999, {"first_name": "John"}
        )
        assert updated_user is None
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_user_no_valid_fields(self, user_repository):
        """Test updating user with no valid fields."""
        # Create user
        user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Try to update with no valid fields
        with pytest.raises(ValueError):
            await user_repository.update_user(user.id, {})
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_repository):
        """Test successful user deletion."""
        # Create user
        user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Delete user
        result = await user_repository.delete_user(user.id)
        assert result is True
        
        # Verify user is deleted
        deleted_user = await user_repository.get_user_by_id(user.id)
        assert deleted_user is None
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_repository):
        """Test deleting non-existent user."""
        result = await user_repository.delete_user(999)
        assert result is False
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_users_success(self, user_repository, sample_users):
        """Test successful user listing."""
        # Create users
        for user in sample_users:
            await user_repository.create_user(
                user.email, user.password_hash, user.first_name, user.last_name
            )
        
        # List users
        users = await user_repository.list_users(limit=2, offset=0)
        
        assert len(users) == 2
        assert all(isinstance(user, User) for user in users)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_users_pagination(self, user_repository, sample_users):
        """Test user listing with pagination."""
        # Create users
        for user in sample_users:
            await user_repository.create_user(
                user.email, user.password_hash, user.first_name, user.last_name
            )
        
        # Test pagination
        page1 = await user_repository.list_users(limit=2, offset=0)
        page2 = await user_repository.list_users(limit=2, offset=2)
        
        assert len(page1) == 2
        assert len(page2) == 1
        assert page1[0].id != page2[0].id
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_count_users_success(self, user_repository, sample_users):
        """Test successful user counting."""
        # Create users
        for user in sample_users:
            await user_repository.create_user(
                user.email, user.password_hash, user.first_name, user.last_name
            )
        
        # Count users
        count = await user_repository.count_users()
        assert count == len(sample_users)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_count_users_empty_database(self, user_repository):
        """Test counting users in empty database."""
        count = await user_repository.count_users()
        assert count == 0
    
    @pytest.mark.unit
    def test_user_entity_validation(self):
        """Test User entity validation."""
        # Valid user
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        assert user.full_name == "John Doe"
        
        # Invalid user - empty email
        with pytest.raises(ValueError):
            User(1, "", "hash", "John", "Doe")
        
        # Invalid user - empty first name
        with pytest.raises(ValueError):
            User(1, "test@example.com", "hash", "", "Doe")
    
    @pytest.mark.unit
    def test_user_to_dict(self, sample_user):
        """Test User to_dict method."""
        user_dict = sample_user.to_dict()
        
        assert user_dict["id"] == sample_user.id
        assert user_dict["email"] == sample_user.email
        assert user_dict["first_name"] == sample_user.first_name
        assert user_dict["last_name"] == sample_user.last_name


class TestAuthenticationServiceComprehensive:
    """Comprehensive unit tests for Authentication Service"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_register_user_success(self, auth_service, valid_registration_data):
        """Test successful user registration."""
        result = await auth_service.register_user(**valid_registration_data)
        
        assert result["success"] is True
        assert result["user"]["email"] == valid_registration_data["email"]
        assert result["user"]["full_name"] == "New User"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, auth_service, valid_registration_data):
        """Test registering user with duplicate email."""
        # Register first user
        await auth_service.register_user(**valid_registration_data)
        
        # Try to register duplicate
        result = await auth_service.register_user(**valid_registration_data)
        
        assert result["success"] is False
        assert "already exists" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_register_user_invalid_data(self, auth_service, invalid_registration_data):
        """Test registering user with invalid data."""
        result = await auth_service.register_user(**invalid_registration_data)
        
        assert result["success"] is False
        assert "required" in result["message"] or "characters" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_login_user_success(self, auth_service, valid_registration_data, valid_login_data):
        """Test successful user login."""
        # Register user
        await auth_service.register_user(**valid_registration_data)
        
        # Login user
        result = await auth_service.login_user(**valid_login_data)
        
        assert result["success"] is True
        assert "token" in result
        assert result["user"]["email"] == valid_login_data["email"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_login_user_wrong_password(self, auth_service, valid_registration_data):
        """Test login with wrong password."""
        # Register user
        await auth_service.register_user(**valid_registration_data)
        
        # Try to login with wrong password
        result = await auth_service.login_user("test@example.com", "WrongPassword")
        
        assert result["success"] is False
        assert "Invalid email or password" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_login_user_nonexistent_user(self, auth_service):
        """Test login with non-existent user."""
        result = await auth_service.login_user("nonexistent@example.com", "password")
        
        assert result["success"] is False
        assert "Invalid email or password" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_verify_token_success(self, auth_service, valid_registration_data, valid_login_data):
        """Test successful token verification."""
        # Register and login user
        await auth_service.register_user(**valid_registration_data)
        login_result = await auth_service.login_user(**valid_login_data)
        
        # Verify token
        verify_result = await auth_service.verify_token(login_result["token"])
        
        assert verify_result["success"] is True
        assert verify_result["user"]["email"] == valid_login_data["email"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_verify_token_invalid(self, auth_service):
        """Test verifying invalid token."""
        result = await auth_service.verify_token("invalid.token.here")
        
        assert result["success"] is False
        assert "Invalid token" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_profile_success(self, auth_service, valid_registration_data):
        """Test getting user profile."""
        # Register user
        await auth_service.register_user(**valid_registration_data)
        
        # Get user profile
        result = await auth_service.get_user_profile(1)
        
        assert result["success"] is True
        assert result["user"]["email"] == valid_registration_data["email"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_user_profile_not_found(self, auth_service):
        """Test getting profile of non-existent user."""
        result = await auth_service.get_user_profile(999)
        
        assert result["success"] is False
        assert "not found" in result["message"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_user_profile_success(self, auth_service, valid_registration_data):
        """Test updating user profile."""
        # Register user
        await auth_service.register_user(**valid_registration_data)
        
        # Update profile
        result = await auth_service.update_user_profile(
            1, {"first_name": "Updated", "last_name": "Name"}
        )
        
        assert result["success"] is True
        assert result["user"]["first_name"] == "Updated"
        assert result["user"]["last_name"] == "Name"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_user_profile_no_valid_fields(self, auth_service, valid_registration_data):
        """Test updating user profile with no valid fields."""
        # Register user
        await auth_service.register_user(**valid_registration_data)
        
        # Try to update with no valid fields
        result = await auth_service.update_user_profile(1, {})
        
        assert result["success"] is False
        assert "No valid fields" in result["message"]


# Test utilities and helpers
class TestUtilities:
    """Test utility functions"""
    
    @pytest.mark.unit
    def test_jwt_token_creation_edge_cases(self):
        """Test JWT token creation with edge cases."""
        # Test with very long email
        long_email = "a" * 100 + "@example.com"
        service = JWTService("secret")
        token = service.create_token(1, long_email, "customer")
        assert isinstance(token, JWTToken)
        
        # Test with special characters in role
        service = JWTService("secret")
        token = service.create_token(1, "test@example.com", "admin-special")
        assert isinstance(token, JWTToken)
    
    @pytest.mark.unit
    def test_password_hashing_edge_cases(self):
        """Test password hashing with edge cases."""
        service = JWTService("secret")
        
        # Test with very long password
        long_password = "A" * 1000
        hashed = service.hash_password(long_password)
        assert len(hashed) > 0
        
        # Test with special characters
        special_password = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        hashed = service.hash_password(special_password)
        assert len(hashed) > 0
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_user_repository_edge_cases(self, user_repository):
        """Test user repository with edge cases."""
        # Test with very long email
        long_email = "a" * 100 + "@example.com"
        user = await user_repository.create_user(long_email, "hash", "John", "Doe")
        assert user.email == long_email
        
        # Test with special characters in names
        user = await user_repository.create_user(
            "special@example.com", "hash", "José-María", "O'Connor"
        )
        assert user.first_name == "José-María"
        assert user.last_name == "O'Connor"
