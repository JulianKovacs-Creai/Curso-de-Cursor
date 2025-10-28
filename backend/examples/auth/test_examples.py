"""
Test Examples - JWT Service and User Repository

This module contains comprehensive tests for the JWT service and User Repository
examples, demonstrating proper testing practices.

Features:
- Unit tests for JWT service
- Unit tests for User Repository
- Integration tests for authentication flow
- Test fixtures and utilities
"""

import pytest
import asyncio
import tempfile
import os
from datetime import datetime, timedelta

from jwt_service_example import JWTService, JWTToken, JWTServiceError, InvalidTokenError, TokenExpiredError
from user_repository_example import UserRepository, User, UserRepositoryError, UserAlreadyExistsError, UserNotFoundError
from complete_auth_example import AuthenticationService, create_authentication_service


class TestJWTService:
    """Test cases for JWT service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.jwt_service = JWTService("test-secret-key")
    
    def test_create_token(self):
        """Test JWT token creation"""
        # Test data
        user_id = 1
        email = "test@example.com"
        role = "customer"
        
        # Create token
        token = self.jwt_service.create_token(user_id, email, role)
        
        # Assertions
        assert isinstance(token, JWTToken)
        assert token.value is not None
        assert len(token.value) > 0
        assert token.token_type == "Bearer"
    
    def test_verify_token(self):
        """Test JWT token verification"""
        # Test data
        user_id = 1
        email = "test@example.com"
        role = "customer"
        
        # Create and verify token
        token = self.jwt_service.create_token(user_id, email, role)
        payload = self.jwt_service.verify_token(token)
        
        # Assertions
        assert payload["user_id"] == user_id
        assert payload["email"] == email
        assert payload["role"] == role
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token"""
        # Create invalid token
        invalid_token = JWTToken("invalid.token.here")
        
        # Should raise exception
        with pytest.raises(InvalidTokenError):
            self.jwt_service.verify_token(invalid_token)
    
    def test_token_expiration(self):
        """Test token expiration"""
        # Create token with very short expiration
        token = self.jwt_service.create_token(
            user_id=1,
            email="test@example.com",
            role="customer",
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        # Should raise exception
        with pytest.raises(TokenExpiredError):
            self.jwt_service.verify_token(token)
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "TestPassword123!"
        hashed = self.jwt_service.hash_password(password)
        
        # Assertions
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")
    
    def test_verify_password(self):
        """Test password verification"""
        password = "TestPassword123!"
        hashed = self.jwt_service.hash_password(password)
        
        # Test correct password
        assert self.jwt_service.verify_password(password, hashed) is True
        
        # Test wrong password
        assert self.jwt_service.verify_password("WrongPassword", hashed) is False
    
    def test_revoke_token(self):
        """Test token revocation"""
        # Create token
        token = self.jwt_service.create_token(1, "test@example.com", "customer")
        
        # Revoke token
        result = self.jwt_service.revoke_token(token)
        assert result is True
        
        # Check if token is revoked
        assert self.jwt_service.is_token_revoked(token) is True
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        user_id = 1
        refresh_token = self.jwt_service.create_refresh_token(user_id)
        
        # Assertions
        assert isinstance(refresh_token, str)
        assert len(refresh_token) == 64  # Should be 64 characters


class TestUserRepository:
    """Test cases for User Repository"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.user_repo = UserRepository(self.temp_db.name)
    
    def teardown_method(self):
        """Cleanup test fixtures"""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test user creation"""
        # Test data
        email = "test@example.com"
        password_hash = "$2b$12$example_hash"
        first_name = "John"
        last_name = "Doe"
        
        # Create user
        user = await self.user_repo.create_user(email, password_hash, first_name, last_name)
        
        # Assertions
        assert user.id is not None
        assert user.email == email
        assert user.password_hash == password_hash
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.created_at is not None
    
    @pytest.mark.asyncio
    async def test_create_duplicate_user(self):
        """Test creating duplicate user"""
        # Create first user
        await self.user_repo.create_user("test@example.com", "hash1", "John", "Doe")
        
        # Try to create duplicate
        with pytest.raises(UserAlreadyExistsError):
            await self.user_repo.create_user("test@example.com", "hash2", "Jane", "Smith")
    
    @pytest.mark.asyncio
    async def test_get_user_by_email(self):
        """Test getting user by email"""
        # Create user
        user = await self.user_repo.create_user("test@example.com", "hash", "John", "Doe")
        
        # Get user by email
        found_user = await self.user_repo.get_user_by_email("test@example.com")
        
        # Assertions
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "test@example.com"
        assert found_user.full_name == "John Doe"
    
    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self):
        """Test getting non-existent user by email"""
        found_user = await self.user_repo.get_user_by_email("nonexistent@example.com")
        assert found_user is None
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self):
        """Test getting user by ID"""
        # Create user
        user = await self.user_repo.create_user("test@example.com", "hash", "John", "Doe")
        
        # Get user by ID
        found_user = await self.user_repo.get_user_by_id(user.id)
        
        # Assertions
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_update_user(self):
        """Test updating user"""
        # Create user
        user = await self.user_repo.create_user("test@example.com", "hash", "John", "Doe")
        
        # Update user
        updated_user = await self.user_repo.update_user(
            user.id,
            {"first_name": "Johnny", "last_name": "Smith"}
        )
        
        # Assertions
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.first_name == "Johnny"
        assert updated_user.last_name == "Smith"
        assert updated_user.full_name == "Johnny Smith"
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_user(self):
        """Test updating non-existent user"""
        updated_user = await self.user_repo.update_user(999, {"first_name": "John"})
        assert updated_user is None
    
    @pytest.mark.asyncio
    async def test_delete_user(self):
        """Test deleting user"""
        # Create user
        user = await self.user_repo.create_user("test@example.com", "hash", "John", "Doe")
        
        # Delete user
        result = await self.user_repo.delete_user(user.id)
        assert result is True
        
        # Verify user is deleted
        found_user = await self.user_repo.get_user_by_id(user.id)
        assert found_user is None
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self):
        """Test deleting non-existent user"""
        result = await self.user_repo.delete_user(999)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_list_users(self):
        """Test listing users"""
        # Create multiple users
        await self.user_repo.create_user("user1@example.com", "hash1", "User", "One")
        await self.user_repo.create_user("user2@example.com", "hash2", "User", "Two")
        await self.user_repo.create_user("user3@example.com", "hash3", "User", "Three")
        
        # List users
        users = await self.user_repo.list_users(limit=2, offset=0)
        
        # Assertions
        assert len(users) == 2
        assert all(isinstance(user, User) for user in users)
    
    @pytest.mark.asyncio
    async def test_count_users(self):
        """Test counting users"""
        # Create users
        await self.user_repo.create_user("user1@example.com", "hash1", "User", "One")
        await self.user_repo.create_user("user2@example.com", "hash2", "User", "Two")
        
        # Count users
        count = await self.user_repo.count_users()
        assert count == 2


class TestAuthenticationService:
    """Test cases for complete authentication service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create authentication service
        self.auth_service = create_authentication_service(
            jwt_secret="test-secret-key",
            db_path=self.temp_db.name
        )
    
    def teardown_method(self):
        """Cleanup test fixtures"""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    @pytest.mark.asyncio
    async def test_register_user(self):
        """Test user registration"""
        # Register user
        result = await self.auth_service.register_user(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="John",
            last_name="Doe"
        )
        
        # Assertions
        assert result["success"] is True
        assert result["user"]["email"] == "test@example.com"
        assert result["user"]["full_name"] == "John Doe"
    
    @pytest.mark.asyncio
    async def test_register_duplicate_user(self):
        """Test registering duplicate user"""
        # Register first user
        await self.auth_service.register_user("test@example.com", "password", "John", "Doe")
        
        # Try to register duplicate
        result = await self.auth_service.register_user("test@example.com", "password", "Jane", "Smith")
        
        # Assertions
        assert result["success"] is False
        assert "already exists" in result["message"]
    
    @pytest.mark.asyncio
    async def test_login_user(self):
        """Test user login"""
        # Register user
        await self.auth_service.register_user("test@example.com", "SecurePassword123!", "John", "Doe")
        
        # Login user
        result = await self.auth_service.login_user("test@example.com", "SecurePassword123!")
        
        # Assertions
        assert result["success"] is True
        assert "token" in result
        assert result["user"]["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self):
        """Test login with wrong password"""
        # Register user
        await self.auth_service.register_user("test@example.com", "SecurePassword123!", "John", "Doe")
        
        # Try to login with wrong password
        result = await self.auth_service.login_user("test@example.com", "WrongPassword")
        
        # Assertions
        assert result["success"] is False
        assert "Invalid email or password" in result["message"]
    
    @pytest.mark.asyncio
    async def test_verify_token(self):
        """Test token verification"""
        # Register and login user
        await self.auth_service.register_user("test@example.com", "SecurePassword123!", "John", "Doe")
        login_result = await self.auth_service.login_user("test@example.com", "SecurePassword123!")
        
        # Verify token
        verify_result = await self.auth_service.verify_token(login_result["token"])
        
        # Assertions
        assert verify_result["success"] is True
        assert verify_result["user"]["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_verify_invalid_token(self):
        """Test verifying invalid token"""
        result = await self.auth_service.verify_token("invalid.token.here")
        
        # Assertions
        assert result["success"] is False
        assert "Invalid token" in result["message"]
    
    @pytest.mark.asyncio
    async def test_get_user_profile(self):
        """Test getting user profile"""
        # Register user
        await self.auth_service.register_user("test@example.com", "SecurePassword123!", "John", "Doe")
        
        # Get user profile (we need to get user ID first)
        # For this test, we'll use a known user ID
        result = await self.auth_service.get_user_profile(1)
        
        # Assertions
        assert result["success"] is True
        assert result["user"]["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_update_user_profile(self):
        """Test updating user profile"""
        # Register user
        await self.auth_service.register_user("test@example.com", "SecurePassword123!", "John", "Doe")
        
        # Update user profile
        result = await self.auth_service.update_user_profile(
            1,  # User ID
            {"first_name": "Johnny", "last_name": "Smith"}
        )
        
        # Assertions
        assert result["success"] is True
        assert result["user"]["first_name"] == "Johnny"
        assert result["user"]["last_name"] == "Smith"


# Test utilities
class TestUtilities:
    """Utility functions for testing"""
    
    @staticmethod
    def create_test_user() -> User:
        """Create a test user entity"""
        return User(
            id=1,
            email="test@example.com",
            password_hash="$2b$12$example_hash",
            first_name="John",
            last_name="Doe",
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_test_jwt_service() -> JWTService:
        """Create a test JWT service"""
        return JWTService("test-secret-key")
    
    @staticmethod
    async def create_test_user_repository() -> UserRepository:
        """Create a test user repository with temporary database"""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        return UserRepository(temp_db.name)


# Run tests
if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])
