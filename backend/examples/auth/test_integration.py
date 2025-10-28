"""
Integration Tests - Authentication Examples

This module contains comprehensive integration tests for database operations,
repository interactions, and service integrations.

Target: Integration tests for repositories and database operations
"""

import pytest
import asyncio
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from typing import List, Dict, Any

from jwt_service_example import JWTService, JWTToken
from user_repository_example import UserRepository, User
from complete_auth_example import AuthenticationService


class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_connection_and_initialization(self, temp_database):
        """Test database connection and table creation."""
        # Create repository (this should initialize database)
        repo = UserRepository(temp_database)
        
        # Verify database file exists
        assert os.path.exists(temp_database)
        
        # Verify tables exist by trying to insert a user
        user = await repo.create_user("test@example.com", "hash", "John", "Doe")
        assert user.id is not None
        
        # Verify indexes exist by checking performance
        start_time = datetime.now()
        await repo.get_user_by_email("test@example.com")
        end_time = datetime.now()
        
        # Should be fast due to index
        assert (end_time - start_time).total_seconds() < 1.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_transaction_rollback(self, temp_database):
        """Test database transaction rollback on error."""
        repo = UserRepository(temp_database)
        
        # Create a user
        user1 = await repo.create_user("user1@example.com", "hash1", "User", "One")
        
        # Try to create user with duplicate email (should fail)
        with pytest.raises(Exception):
            await repo.create_user("user1@example.com", "hash2", "User", "Two")
        
        # Verify first user still exists
        retrieved_user = await repo.get_user_by_email("user1@example.com")
        assert retrieved_user is not None
        assert retrieved_user.id == user1.id
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_concurrent_operations(self, temp_database):
        """Test concurrent database operations."""
        repo = UserRepository(temp_database)
        
        # Create multiple users concurrently
        async def create_user(email_suffix):
            return await repo.create_user(
                f"user{email_suffix}@example.com",
                f"hash{email_suffix}",
                f"User{email_suffix}",
                f"Test{email_suffix}"
            )
        
        # Create 10 users concurrently
        tasks = [create_user(i) for i in range(10)]
        users = await asyncio.gather(*tasks)
        
        # Verify all users were created
        assert len(users) == 10
        assert all(user.id is not None for user in users)
        
        # Verify all users can be retrieved
        for user in users:
            retrieved = await repo.get_user_by_id(user.id)
            assert retrieved is not None
            assert retrieved.email == user.email
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_pagination_performance(self, temp_database):
        """Test database pagination performance with large dataset."""
        repo = UserRepository(temp_database)
        
        # Create 100 users
        for i in range(100):
            await repo.create_user(
                f"user{i}@example.com",
                f"hash{i}",
                f"User{i}",
                f"Test{i}"
            )
        
        # Test pagination performance
        start_time = datetime.now()
        
        # Get first page
        page1 = await repo.list_users(limit=10, offset=0)
        assert len(page1) == 10
        
        # Get second page
        page2 = await repo.list_users(limit=10, offset=10)
        assert len(page2) == 10
        
        # Get last page
        page3 = await repo.list_users(limit=10, offset=90)
        assert len(page3) == 10
        
        end_time = datetime.now()
        
        # Should be fast even with 100 users
        assert (end_time - start_time).total_seconds() < 2.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_constraint_violations(self, temp_database):
        """Test database constraint violations."""
        repo = UserRepository(temp_database)
        
        # Test unique email constraint
        await repo.create_user("test@example.com", "hash1", "John", "Doe")
        
        with pytest.raises(Exception):
            await repo.create_user("test@example.com", "hash2", "Jane", "Smith")
        
        # Test NOT NULL constraints
        with pytest.raises(Exception):
            await repo.create_user(None, "hash", "John", "Doe")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_database_connection_pooling(self, temp_database):
        """Test database connection handling."""
        repo = UserRepository(temp_database)
        
        # Perform multiple operations to test connection handling
        for i in range(50):
            user = await repo.create_user(
                f"user{i}@example.com",
                f"hash{i}",
                f"User{i}",
                f"Test{i}"
            )
            
            # Retrieve user
            retrieved = await repo.get_user_by_id(user.id)
            assert retrieved is not None
            
            # Update user
            updated = await repo.update_user(user.id, {"first_name": f"Updated{i}"})
            assert updated is not None


class TestRepositoryIntegration:
    """Integration tests for repository operations"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_user_repository_full_crud_cycle(self, user_repository):
        """Test complete CRUD cycle for user repository."""
        # Create user
        user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        assert user.id is not None
        
        # Read user by email
        retrieved_by_email = await user_repository.get_user_by_email("test@example.com")
        assert retrieved_by_email.id == user.id
        
        # Read user by ID
        retrieved_by_id = await user_repository.get_user_by_id(user.id)
        assert retrieved_by_id.id == user.id
        
        # Update user
        updated_user = await user_repository.update_user(
            user.id, {"first_name": "Johnny", "last_name": "Smith"}
        )
        assert updated_user.first_name == "Johnny"
        assert updated_user.last_name == "Smith"
        
        # Delete user
        deleted = await user_repository.delete_user(user.id)
        assert deleted is True
        
        # Verify user is deleted
        deleted_user = await user_repository.get_user_by_id(user.id)
        assert deleted_user is None
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_user_repository_bulk_operations(self, user_repository):
        """Test bulk operations on user repository."""
        # Create multiple users
        users = []
        for i in range(20):
            user = await user_repository.create_user(
                f"user{i}@example.com", f"hash{i}", f"User{i}", f"Test{i}"
            )
            users.append(user)
        
        # Test listing with pagination
        page1 = await user_repository.list_users(limit=10, offset=0)
        page2 = await user_repository.list_users(limit=10, offset=10)
        
        assert len(page1) == 10
        assert len(page2) == 10
        assert page1[0].id != page2[0].id
        
        # Test counting
        count = await user_repository.count_users()
        assert count == 20
        
        # Test bulk updates
        for user in users[:5]:
            await user_repository.update_user(
                user.id, {"first_name": f"Updated{user.id}"}
            )
        
        # Test bulk deletes
        for user in users[5:10]:
            deleted = await user_repository.delete_user(user.id)
            assert deleted is True
        
        # Verify final count
        final_count = await user_repository.count_users()
        assert final_count == 15
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_user_repository_error_handling(self, user_repository):
        """Test error handling in user repository."""
        # Test getting non-existent user
        user = await user_repository.get_user_by_id(999)
        assert user is None
        
        # Test updating non-existent user
        updated = await user_repository.update_user(999, {"first_name": "Test"})
        assert updated is None
        
        # Test deleting non-existent user
        deleted = await user_repository.delete_user(999)
        assert deleted is False
        
        # Test creating user with invalid data
        with pytest.raises(ValueError):
            await user_repository.create_user("", "hash", "John", "Doe")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_user_repository_data_consistency(self, user_repository):
        """Test data consistency in user repository."""
        # Create user
        user = await user_repository.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Verify data consistency across operations
        retrieved1 = await user_repository.get_user_by_email("test@example.com")
        retrieved2 = await user_repository.get_user_by_id(user.id)
        
        assert retrieved1.id == retrieved2.id
        assert retrieved1.email == retrieved2.email
        assert retrieved1.first_name == retrieved2.first_name
        assert retrieved1.last_name == retrieved2.last_name
        
        # Update user
        updated = await user_repository.update_user(
            user.id, {"first_name": "Johnny"}
        )
        
        # Verify update is consistent
        retrieved3 = await user_repository.get_user_by_id(user.id)
        assert retrieved3.first_name == "Johnny"
        assert retrieved3.last_name == "Doe"  # Should remain unchanged


class TestServiceIntegration:
    """Integration tests for service interactions"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_jwt_service_with_user_repository(self, temp_database):
        """Test JWT service integration with user repository."""
        jwt_service = JWTService("test-secret")
        user_repo = UserRepository(temp_database)
        
        # Create user
        user = await user_repo.create_user(
            "test@example.com", "hash", "John", "Doe"
        )
        
        # Create JWT token
        token = jwt_service.create_token(user.id, user.email, "customer")
        
        # Verify token
        payload = jwt_service.verify_token(token)
        assert payload["user_id"] == user.id
        assert payload["email"] == user.email
        
        # Get user from repository using token payload
        retrieved_user = await user_repo.get_user_by_id(payload["user_id"])
        assert retrieved_user.id == user.id
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_authentication_service_full_flow(self, auth_service):
        """Test complete authentication flow."""
        # Register user
        register_result = await auth_service.register_user(
            "test@example.com", "SecurePassword123!", "John", "Doe"
        )
        assert register_result["success"] is True
        
        # Login user
        login_result = await auth_service.login_user(
            "test@example.com", "SecurePassword123!"
        )
        assert login_result["success"] is True
        assert "token" in login_result
        
        # Verify token
        verify_result = await auth_service.verify_token(login_result["token"])
        assert verify_result["success"] is True
        assert verify_result["user"]["email"] == "test@example.com"
        
        # Get user profile
        profile_result = await auth_service.get_user_profile(verify_result["user"]["id"])
        assert profile_result["success"] is True
        assert profile_result["user"]["email"] == "test@example.com"
        
        # Update user profile
        update_result = await auth_service.update_user_profile(
            verify_result["user"]["id"],
            {"first_name": "Johnny", "last_name": "Smith"}
        )
        assert update_result["success"] is True
        assert update_result["user"]["first_name"] == "Johnny"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_authentication_service_error_scenarios(self, auth_service):
        """Test authentication service error scenarios."""
        # Test login with non-existent user
        login_result = await auth_service.login_user(
            "nonexistent@example.com", "password"
        )
        assert login_result["success"] is False
        
        # Test login with wrong password
        await auth_service.register_user(
            "test@example.com", "SecurePassword123!", "John", "Doe"
        )
        
        wrong_login = await auth_service.login_user(
            "test@example.com", "WrongPassword"
        )
        assert wrong_login["success"] is False
        
        # Test verifying invalid token
        verify_result = await auth_service.verify_token("invalid.token.here")
        assert verify_result["success"] is False
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_authentication_service_concurrent_operations(self, auth_service):
        """Test concurrent authentication operations."""
        # Register multiple users concurrently
        async def register_user(email_suffix):
            return await auth_service.register_user(
                f"user{email_suffix}@example.com",
                "SecurePassword123!",
                f"User{email_suffix}",
                f"Test{email_suffix}"
            )
        
        # Register 10 users concurrently
        tasks = [register_user(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All registrations should succeed
        assert all(result["success"] for result in results)
        
        # Login all users concurrently
        async def login_user(email_suffix):
            return await auth_service.login_user(
                f"user{email_suffix}@example.com",
                "SecurePassword123!"
            )
        
        login_tasks = [login_user(i) for i in range(10)]
        login_results = await asyncio.gather(*login_tasks)
        
        # All logins should succeed
        assert all(result["success"] for result in login_results)
        
        # Verify all tokens
        async def verify_token(token):
            return await auth_service.verify_token(token)
        
        verify_tasks = [verify_token(result["token"]) for result in login_results]
        verify_results = await asyncio.gather(*verify_tasks)
        
        # All token verifications should succeed
        assert all(result["success"] for result in verify_results)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_authentication_service_data_persistence(self, auth_service):
        """Test data persistence across service operations."""
        # Register user
        register_result = await auth_service.register_user(
            "test@example.com", "SecurePassword123!", "John", "Doe"
        )
        user_id = register_result["user"]["id"]
        
        # Login user
        login_result = await auth_service.login_user(
            "test@example.com", "SecurePassword123!"
        )
        
        # Verify token
        verify_result = await auth_service.verify_token(login_result["token"])
        
        # Get user profile
        profile_result = await auth_service.get_user_profile(user_id)
        
        # All operations should return consistent data
        assert register_result["user"]["email"] == "test@example.com"
        assert login_result["user"]["email"] == "test@example.com"
        assert verify_result["user"]["email"] == "test@example.com"
        assert profile_result["user"]["email"] == "test@example.com"
        
        # Update user profile
        update_result = await auth_service.update_user_profile(
            user_id, {"first_name": "Johnny"}
        )
        
        # Verify update is persistent
        updated_profile = await auth_service.get_user_profile(user_id)
        assert updated_profile["user"]["first_name"] == "Johnny"
        assert updated_profile["user"]["last_name"] == "Doe"  # Should remain unchanged


class TestPerformanceIntegration:
    """Integration tests for performance scenarios"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_large_dataset_performance(self, temp_database):
        """Test performance with large dataset."""
        user_repo = UserRepository(temp_database)
        
        # Create 1000 users
        start_time = datetime.now()
        
        for i in range(1000):
            await user_repo.create_user(
                f"user{i}@example.com",
                f"hash{i}",
                f"User{i}",
                f"Test{i}"
            )
        
        creation_time = datetime.now() - start_time
        
        # Should create 1000 users in reasonable time
        assert creation_time.total_seconds() < 30.0
        
        # Test pagination performance
        start_time = datetime.now()
        
        for offset in range(0, 1000, 100):
            users = await user_repo.list_users(limit=100, offset=offset)
            assert len(users) == 100
        
        pagination_time = datetime.now() - start_time
        
        # Should paginate through all users quickly
        assert pagination_time.total_seconds() < 5.0
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_concurrent_authentication_performance(self, auth_service):
        """Test concurrent authentication performance."""
        # Register 100 users
        for i in range(100):
            await auth_service.register_user(
                f"user{i}@example.com",
                "SecurePassword123!",
                f"User{i}",
                f"Test{i}"
            )
        
        # Login all users concurrently
        start_time = datetime.now()
        
        async def login_user(i):
            return await auth_service.login_user(
                f"user{i}@example.com",
                "SecurePassword123!"
            )
        
        tasks = [login_user(i) for i in range(100)]
        results = await asyncio.gather(*tasks)
        
        login_time = datetime.now() - start_time
        
        # All logins should succeed
        assert all(result["success"] for result in results)
        
        # Should complete in reasonable time
        assert login_time.total_seconds() < 10.0
        
        # Verify all tokens concurrently
        start_time = datetime.now()
        
        async def verify_token(result):
            return await auth_service.verify_token(result["token"])
        
        verify_tasks = [verify_token(result) for result in results]
        verify_results = await asyncio.gather(*verify_tasks)
        
        verify_time = datetime.now() - start_time
        
        # All verifications should succeed
        assert all(result["success"] for result in verify_results)
        
        # Should complete quickly
        assert verify_time.total_seconds() < 5.0
