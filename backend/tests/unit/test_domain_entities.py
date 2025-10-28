"""
Unit tests for domain entities.

Tests the core business logic in domain entities without external dependencies.
"""

import pytest
from datetime import datetime
from decimal import Decimal

from src.auth.domain.entities import User, UserRole, UserStatus
from src.auth.domain.value_objects import Email, Password, FirstName, LastName


class TestUser:
    """Test User domain entity."""
    
    def test_create_user_success(self):
        """Test creating a user with valid data."""
        user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == UserRole.CUSTOMER
        assert user.status == UserStatus.ACTIVE
        assert user.is_email_verified is True
    
    def test_user_full_name(self):
        """Test user full name property."""
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
        
        assert user.full_name == "John Doe"
    
    def test_user_is_active(self):
        """Test user is_active property."""
        active_user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        
        inactive_user = User(
            id=2,
            email="test2@example.com",
            password_hash="hashed_password",
            first_name="Jane",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.INACTIVE,
            is_email_verified=True
        )
        
        assert active_user.is_active is True
        assert inactive_user.is_active is False
    
    def test_user_role_checks(self):
        """Test user role checking methods."""
        admin_user = User(
            id=1,
            email="admin@example.com",
            password_hash="hashed_password",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        
        customer_user = User(
            id=2,
            email="customer@example.com",
            password_hash="hashed_password",
            first_name="Customer",
            last_name="User",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        
        assert admin_user.is_admin is True
        assert admin_user.is_customer is False
        assert customer_user.is_admin is False
        assert customer_user.is_customer is True
    
    def test_user_can_login(self):
        """Test user can_login method."""
        # Active, verified user
        active_user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        
        # Inactive user
        inactive_user = User(
            id=2,
            email="test2@example.com",
            password_hash="hashed_password",
            first_name="Jane",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.INACTIVE,
            is_email_verified=True
        )
        
        # Unverified user
        unverified_user = User(
            id=3,
            email="test3@example.com",
            password_hash="hashed_password",
            first_name="Bob",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            is_email_verified=False
        )
        
        # Suspended user
        suspended_user = User(
            id=4,
            email="test4@example.com",
            password_hash="hashed_password",
            first_name="Alice",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            status=UserStatus.SUSPENDED,
            is_email_verified=True
        )
        
        assert active_user.can_login() is True
        assert inactive_user.can_login() is False
        assert unverified_user.can_login() is False
        assert suspended_user.can_login() is False
    
    def test_user_activate(self):
        """Test user activation."""
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
        
        activated_user = user.activate()
        
        assert activated_user.status == UserStatus.ACTIVE
        assert activated_user.id == user.id
        assert activated_user.email == user.email
    
    def test_user_deactivate(self):
        """Test user deactivation."""
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
        
        deactivated_user = user.deactivate()
        
        assert deactivated_user.status == UserStatus.INACTIVE
        assert deactivated_user.id == user.id
        assert deactivated_user.email == user.email
    
    def test_user_suspend(self):
        """Test user suspension."""
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
        
        suspended_user = user.suspend()
        
        assert suspended_user.status == UserStatus.SUSPENDED
        assert suspended_user.id == user.id
        assert suspended_user.email == user.email
    
    def test_user_verify_email(self):
        """Test email verification."""
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
        
        verified_user = user.verify_email()
        
        assert verified_user.is_email_verified is True
        assert verified_user.id == user.id
        assert verified_user.email == user.email
    
    def test_user_update_password(self):
        """Test password update."""
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
        
        updated_user = user.update_password("new_hash")
        
        assert updated_user.password_hash == "new_hash"
        assert updated_user.id == user.id
        assert updated_user.email == user.email
    
    def test_user_update_password_empty_hash(self):
        """Test password update with empty hash raises error."""
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
        
        with pytest.raises(ValueError, match="Password hash cannot be empty"):
            user.update_password("")
    
    def test_user_update_profile(self):
        """Test profile update."""
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
        
        updated_user = user.update_profile("Jane", "Smith")
        
        assert updated_user.first_name == "Jane"
        assert updated_user.last_name == "Smith"
        assert updated_user.id == user.id
        assert updated_user.email == user.email
    
    def test_user_update_profile_empty_names(self):
        """Test profile update with empty names raises error."""
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
        
        with pytest.raises(ValueError, match="First name cannot be empty"):
            user.update_profile("", "Smith")
        
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            user.update_profile("Jane", "")
    
    def test_user_record_login(self):
        """Test recording login timestamp."""
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
        
        user_with_login = user.record_login()
        
        assert user_with_login.last_login_at is not None
        assert user_with_login.id == user.id
        assert user_with_login.email == user.email
    
    def test_user_change_role(self):
        """Test role change."""
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
        
        admin_user = user.change_role(UserRole.ADMIN)
        
        assert admin_user.role == UserRole.ADMIN
        assert admin_user.id == user.id
        assert admin_user.email == user.email
    
    def test_user_validation_errors(self):
        """Test user validation errors."""
        with pytest.raises(ValueError, match="Email cannot be empty"):
            User(
                id=1,
                email="",
                password_hash="hashed_password",
                first_name="John",
                last_name="Doe",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            )
        
        with pytest.raises(ValueError, match="First name cannot be empty"):
            User(
                id=1,
                email="test@example.com",
                password_hash="hashed_password",
                first_name="",
                last_name="Doe",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            )
        
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            User(
                id=1,
                email="test@example.com",
                password_hash="hashed_password",
                first_name="John",
                last_name="",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            )
        
        with pytest.raises(ValueError, match="Password hash cannot be empty"):
            User(
                id=1,
                email="test@example.com",
                password_hash="",
                first_name="John",
                last_name="Doe",
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
                is_email_verified=True
            )
