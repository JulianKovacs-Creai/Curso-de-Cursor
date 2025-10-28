"""
End-to-End Tests - Authentication Examples

This module contains comprehensive end-to-end tests for critical authentication
endpoints and complete user journeys.

Target: E2E tests for critical authentication endpoints
"""

import pytest
import asyncio
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import patch, Mock, AsyncMock
from typing import Dict, Any, List

from jwt_service_example import JWTService, JWTToken
from user_repository_example import UserRepository, User
from complete_auth_example import AuthenticationService


class TestAuthenticationE2E:
    """End-to-end tests for complete authentication flows"""
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_user_registration_and_login_flow(self, auth_service):
        """Test complete user registration and login flow."""
        # Step 1: Register new user
        register_result = await auth_service.register_user(
            email="newuser@example.com",
            password="SecurePassword123!",
            first_name="New",
            last_name="User"
        )
        
        # Verify registration success
        assert register_result["success"] is True
        assert register_result["user"]["email"] == "newuser@example.com"
        assert register_result["user"]["full_name"] == "New User"
        user_id = register_result["user"]["id"]
        
        # Step 2: Login with registered user
        login_result = await auth_service.login_user(
            email="newuser@example.com",
            password="SecurePassword123!"
        )
        
        # Verify login success
        assert login_result["success"] is True
        assert "token" in login_result
        assert login_result["user"]["email"] == "newuser@example.com"
        token = login_result["token"]
        
        # Step 3: Verify token and get user info
        verify_result = await auth_service.verify_token(token)
        
        # Verify token is valid
        assert verify_result["success"] is True
        assert verify_result["user"]["id"] == user_id
        assert verify_result["user"]["email"] == "newuser@example.com"
        
        # Step 4: Get user profile
        profile_result = await auth_service.get_user_profile(user_id)
        
        # Verify profile data
        assert profile_result["success"] is True
        assert profile_result["user"]["email"] == "newuser@example.com"
        assert profile_result["user"]["first_name"] == "New"
        assert profile_result["user"]["last_name"] == "User"
        
        # Step 5: Update user profile
        update_result = await auth_service.update_user_profile(
            user_id,
            {"first_name": "Updated", "last_name": "Name"}
        )
        
        # Verify update success
        assert update_result["success"] is True
        assert update_result["user"]["first_name"] == "Updated"
        assert update_result["user"]["last_name"] == "Name"
        
        # Step 6: Verify updated profile
        updated_profile = await auth_service.get_user_profile(user_id)
        assert updated_profile["user"]["first_name"] == "Updated"
        assert updated_profile["user"]["last_name"] == "Name"
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_multiple_users_registration_and_authentication(self, auth_service):
        """Test multiple users registration and authentication."""
        users_data = [
            {"email": "user1@example.com", "password": "Password123!", "first_name": "User", "last_name": "One"},
            {"email": "user2@example.com", "password": "Password123!", "first_name": "User", "last_name": "Two"},
            {"email": "user3@example.com", "password": "Password123!", "first_name": "User", "last_name": "Three"}
        ]
        
        registered_users = []
        tokens = []
        
        # Register all users
        for user_data in users_data:
            register_result = await auth_service.register_user(**user_data)
            assert register_result["success"] is True
            registered_users.append(register_result["user"])
        
        # Login all users
        for user_data in users_data:
            login_result = await auth_service.login_user(
                user_data["email"], user_data["password"]
            )
            assert login_result["success"] is True
            tokens.append(login_result["token"])
        
        # Verify all tokens
        for i, token in enumerate(tokens):
            verify_result = await auth_service.verify_token(token)
            assert verify_result["success"] is True
            assert verify_result["user"]["email"] == users_data[i]["email"]
        
        # Get profiles for all users
        for user in registered_users:
            profile_result = await auth_service.get_user_profile(user["id"])
            assert profile_result["success"] is True
            assert profile_result["user"]["email"] == user["email"]
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_authentication_error_scenarios(self, auth_service):
        """Test authentication error scenarios end-to-end."""
        # Test 1: Register user with invalid data
        invalid_register = await auth_service.register_user(
            email="invalid-email",
            password="123",  # Too short
            first_name="",
            last_name=""
        )
        assert invalid_register["success"] is False
        
        # Test 2: Register user with valid data
        valid_register = await auth_service.register_user(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User"
        )
        assert valid_register["success"] is True
        
        # Test 3: Try to register duplicate user
        duplicate_register = await auth_service.register_user(
            email="test@example.com",
            password="AnotherPassword123!",
            first_name="Another",
            last_name="User"
        )
        assert duplicate_register["success"] is False
        
        # Test 4: Login with wrong password
        wrong_password_login = await auth_service.login_user(
            "test@example.com", "WrongPassword"
        )
        assert wrong_password_login["success"] is False
        
        # Test 5: Login with non-existent user
        nonexistent_login = await auth_service.login_user(
            "nonexistent@example.com", "Password123!"
        )
        assert nonexistent_login["success"] is False
        
        # Test 6: Login with correct credentials
        correct_login = await auth_service.login_user(
            "test@example.com", "SecurePassword123!"
        )
        assert correct_login["success"] is True
        token = correct_login["token"]
        
        # Test 7: Verify invalid token
        invalid_verify = await auth_service.verify_token("invalid.token.here")
        assert invalid_verify["success"] is False
        
        # Test 8: Verify valid token
        valid_verify = await auth_service.verify_token(token)
        assert valid_verify["success"] is True
        
        # Test 9: Get profile for non-existent user
        nonexistent_profile = await auth_service.get_user_profile(999)
        assert nonexistent_profile["success"] is False
        
        # Test 10: Update profile with no valid fields
        user_id = valid_verify["user"]["id"]
        invalid_update = await auth_service.update_user_profile(user_id, {})
        assert invalid_update["success"] is False
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_token_expiration_and_refresh_flow(self, auth_service):
        """Test token expiration and refresh flow."""
        # Register and login user
        await auth_service.register_user(
            "test@example.com", "SecurePassword123!", "Test", "User"
        )
        
        login_result = await auth_service.login_user(
            "test@example.com", "SecurePassword123!"
        )
        assert login_result["success"] is True
        token = login_result["token"]
        
        # Verify token is valid
        verify_result = await auth_service.verify_token(token)
        assert verify_result["success"] is True
        
        # Simulate token expiration by creating a new service with short expiration
        jwt_service = JWTService("test-secret", access_token_expire_hours=0.0001)  # Very short expiration
        user_repo = UserRepository(auth_service.user_repository.database_path)
        expired_auth_service = AuthenticationService(jwt_service, user_repo)
        
        # Create token that will expire quickly
        expired_token = jwt_service.create_token(1, "test@example.com", "customer")
        
        # Wait for token to expire
        await asyncio.sleep(0.1)
        
        # Try to verify expired token
        expired_verify = await expired_auth_service.verify_token(expired_token.value)
        assert expired_verify["success"] is False
        
        # Login again to get new token
        new_login = await auth_service.login_user(
            "test@example.com", "SecurePassword123!"
        )
        assert new_login["success"] is True
        
        # Verify new token
        new_verify = await auth_service.verify_token(new_login["token"])
        assert new_verify["success"] is True
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_concurrent_user_operations(self, auth_service):
        """Test concurrent user operations end-to-end."""
        # Register multiple users concurrently
        async def register_and_login_user(user_id):
            email = f"user{user_id}@example.com"
            password = "SecurePassword123!"
            
            # Register user
            register_result = await auth_service.register_user(
                email, password, f"User{user_id}", f"Test{user_id}"
            )
            
            if not register_result["success"]:
                return None
            
            # Login user
            login_result = await auth_service.login_user(email, password)
            
            if not login_result["success"]:
                return None
            
            # Verify token
            verify_result = await auth_service.verify_token(login_result["token"])
            
            if not verify_result["success"]:
                return None
            
            # Get profile
            profile_result = await auth_service.get_user_profile(verify_result["user"]["id"])
            
            return {
                "user_id": user_id,
                "email": email,
                "register_success": register_result["success"],
                "login_success": login_result["success"],
                "verify_success": verify_result["success"],
                "profile_success": profile_result["success"]
            }
        
        # Run 20 concurrent user operations
        tasks = [register_and_login_user(i) for i in range(20)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None results
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        
        # All operations should succeed
        assert len(valid_results) == 20
        
        for result in valid_results:
            assert result["register_success"] is True
            assert result["login_success"] is True
            assert result["verify_success"] is True
            assert result["profile_success"] is True
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_data_consistency_across_operations(self, auth_service):
        """Test data consistency across all operations."""
        # Register user
        register_result = await auth_service.register_user(
            "consistency@example.com", "SecurePassword123!", "Consistency", "Test"
        )
        assert register_result["success"] is True
        user_id = register_result["user"]["id"]
        
        # Login user
        login_result = await auth_service.login_user(
            "consistency@example.com", "SecurePassword123!"
        )
        assert login_result["success"] is True
        token = login_result["token"]
        
        # Verify token
        verify_result = await auth_service.verify_token(token)
        assert verify_result["success"] is True
        
        # Get profile
        profile_result = await auth_service.get_user_profile(user_id)
        assert profile_result["success"] is True
        
        # All operations should return consistent data
        assert register_result["user"]["email"] == "consistency@example.com"
        assert login_result["user"]["email"] == "consistency@example.com"
        assert verify_result["user"]["email"] == "consistency@example.com"
        assert profile_result["user"]["email"] == "consistency@example.com"
        
        assert register_result["user"]["first_name"] == "Consistency"
        assert login_result["user"]["first_name"] == "Consistency"
        assert verify_result["user"]["first_name"] == "Consistency"
        assert profile_result["user"]["first_name"] == "Consistency"
        
        # Update profile
        update_result = await auth_service.update_user_profile(
            user_id, {"first_name": "Updated", "last_name": "Name"}
        )
        assert update_result["success"] is True
        
        # Verify update is consistent across all operations
        updated_profile = await auth_service.get_user_profile(user_id)
        assert updated_profile["user"]["first_name"] == "Updated"
        assert updated_profile["user"]["last_name"] == "Name"
        
        # Login again to verify updated data
        new_login = await auth_service.login_user(
            "consistency@example.com", "SecurePassword123!"
        )
        assert new_login["success"] is True
        assert new_login["user"]["first_name"] == "Updated"
        assert new_login["user"]["last_name"] == "Name"
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_security_scenarios(self, auth_service):
        """Test security scenarios end-to-end."""
        # Register user
        await auth_service.register_user(
            "security@example.com", "SecurePassword123!", "Security", "Test"
        )
        
        # Test 1: Try to access with invalid token
        invalid_token_result = await auth_service.verify_token("invalid.token.here")
        assert invalid_token_result["success"] is False
        
        # Test 2: Try to access with malformed token
        malformed_token_result = await auth_service.verify_token("not.a.jwt.token")
        assert malformed_token_result["success"] is False
        
        # Test 3: Try to access with empty token
        empty_token_result = await auth_service.verify_token("")
        assert empty_token_result["success"] is False
        
        # Test 4: Login with correct credentials
        login_result = await auth_service.login_user(
            "security@example.com", "SecurePassword123!"
        )
        assert login_result["success"] is True
        token = login_result["token"]
        
        # Test 5: Verify valid token
        valid_verify = await auth_service.verify_token(token)
        assert valid_verify["success"] is True
        
        # Test 6: Try to access non-existent user profile
        nonexistent_profile = await auth_service.get_user_profile(999)
        assert nonexistent_profile["success"] is False
        
        # Test 7: Try to update non-existent user
        nonexistent_update = await auth_service.update_user_profile(
            999, {"first_name": "Test"}
        )
        assert nonexistent_update["success"] is False
        
        # Test 8: Try to update with invalid data
        user_id = valid_verify["user"]["id"]
        invalid_update = await auth_service.update_user_profile(
            user_id, {"invalid_field": "value"}
        )
        assert invalid_update["success"] is False
    
    @pytest.mark.e2e
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_performance_under_load(self, auth_service):
        """Test performance under load."""
        # Register 100 users
        start_time = datetime.now()
        
        for i in range(100):
            await auth_service.register_user(
                f"loaduser{i}@example.com",
                "SecurePassword123!",
                f"LoadUser{i}",
                f"Test{i}"
            )
        
        registration_time = datetime.now() - start_time
        
        # Registration should complete in reasonable time
        assert registration_time.total_seconds() < 30.0
        
        # Login all users concurrently
        start_time = datetime.now()
        
        async def login_user(i):
            return await auth_service.login_user(
                f"loaduser{i}@example.com", "SecurePassword123!"
            )
        
        login_tasks = [login_user(i) for i in range(100)]
        login_results = await asyncio.gather(*login_tasks)
        
        login_time = datetime.now() - start_time
        
        # All logins should succeed
        assert all(result["success"] for result in login_results)
        
        # Login should complete in reasonable time
        assert login_time.total_seconds() < 15.0
        
        # Verify all tokens concurrently
        start_time = datetime.now()
        
        async def verify_token(result):
            return await auth_service.verify_token(result["token"])
        
        verify_tasks = [verify_token(result) for result in login_results]
        verify_results = await asyncio.gather(*verify_tasks)
        
        verify_time = datetime.now() - start_time
        
        # All verifications should succeed
        assert all(result["success"] for result in verify_results)
        
        # Verification should complete quickly
        assert verify_time.total_seconds() < 10.0
        
        # Get profiles for all users concurrently
        start_time = datetime.now()
        
        async def get_profile(result):
            user_id = result["user"]["id"]
            return await auth_service.get_user_profile(user_id)
        
        profile_tasks = [get_profile(result) for result in login_results]
        profile_results = await asyncio.gather(*profile_tasks)
        
        profile_time = datetime.now() - start_time
        
        # All profile retrievals should succeed
        assert all(result["success"] for result in profile_results)
        
        # Profile retrieval should complete quickly
        assert profile_time.total_seconds() < 10.0
