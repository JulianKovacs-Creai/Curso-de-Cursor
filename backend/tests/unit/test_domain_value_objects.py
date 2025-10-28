"""
Unit tests for domain value objects.

Tests the validation logic and business rules in value objects.
"""

import pytest
from datetime import datetime, timedelta

from src.auth.domain.value_objects import (
    Email, Password, FirstName, LastName, JWTToken, RefreshToken,
    LoginCredentials, UserRegistration, PasswordResetToken
)


class TestEmail:
    """Test Email value object."""
    
    def test_valid_email(self):
        """Test creating email with valid format."""
        email = Email("test@example.com")
        assert email.value == "test@example.com"
    
    def test_email_normalization(self):
        """Test email normalization to lowercase."""
        email = Email("TEST@EXAMPLE.COM")
        assert email.value == "test@example.com"
    
    def test_email_trimming(self):
        """Test email trimming of whitespace."""
        email = Email("  test@example.com  ")
        assert email.value == "test@example.com"
    
    def test_invalid_email_format(self):
        """Test invalid email format raises error."""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("invalid-email")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("test@")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("@example.com")
    
    def test_empty_email(self):
        """Test empty email raises error."""
        with pytest.raises(ValueError, match="Email cannot be empty"):
            Email("")
        
        with pytest.raises(ValueError, match="Email cannot be empty"):
            Email("   ")


class TestPassword:
    """Test Password value object."""
    
    def test_valid_password(self):
        """Test creating password with valid format."""
        password = Password("ValidPass123!")
        assert str(password) == "***"  # Never expose password
    
    def test_password_too_short(self):
        """Test password too short raises error."""
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            Password("Short1!")
    
    def test_password_too_long(self):
        """Test password too long raises error."""
        long_password = "A" * 129 + "1!"
        with pytest.raises(ValueError, match="Password cannot exceed 128 characters"):
            Password(long_password)
    
    def test_password_missing_uppercase(self):
        """Test password missing uppercase raises error."""
        with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
            Password("validpass123!")
    
    def test_password_missing_lowercase(self):
        """Test password missing lowercase raises error."""
        with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
            Password("VALIDPASS123!")
    
    def test_password_missing_digit(self):
        """Test password missing digit raises error."""
        with pytest.raises(ValueError, match="Password must contain at least one digit"):
            Password("ValidPass!")
    
    def test_password_missing_special_char(self):
        """Test password missing special character raises error."""
        with pytest.raises(ValueError, match="Password must contain at least one special character"):
            Password("ValidPass123")
    
    def test_empty_password(self):
        """Test empty password raises error."""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            Password("")


class TestFirstName:
    """Test FirstName value object."""
    
    def test_valid_first_name(self):
        """Test creating first name with valid format."""
        first_name = FirstName("John")
        assert first_name.value == "John"
    
    def test_first_name_normalization(self):
        """Test first name normalization to title case."""
        first_name = FirstName("john")
        assert first_name.value == "John"
        
        first_name = FirstName("JOHN")
        assert first_name.value == "John"
    
    def test_first_name_trimming(self):
        """Test first name trimming of whitespace."""
        first_name = FirstName("  John  ")
        assert first_name.value == "John"
    
    def test_first_name_too_short(self):
        """Test first name too short raises error."""
        with pytest.raises(ValueError, match="First name must be at least 2 characters long"):
            FirstName("J")
    
    def test_first_name_too_long(self):
        """Test first name too long raises error."""
        long_name = "A" * 51
        with pytest.raises(ValueError, match="First name cannot exceed 50 characters"):
            FirstName(long_name)
    
    def test_first_name_invalid_characters(self):
        """Test first name with invalid characters raises error."""
        with pytest.raises(ValueError, match="First name can only contain letters, spaces, and hyphens"):
            FirstName("John123")
        
        with pytest.raises(ValueError, match="First name can only contain letters, spaces, and hyphens"):
            FirstName("John@Doe")
    
    def test_first_name_with_hyphen(self):
        """Test first name with hyphen is valid."""
        first_name = FirstName("Mary-Jane")
        assert first_name.value == "Mary-Jane"
    
    def test_empty_first_name(self):
        """Test empty first name raises error."""
        with pytest.raises(ValueError, match="First name cannot be empty"):
            FirstName("")


class TestLastName:
    """Test LastName value object."""
    
    def test_valid_last_name(self):
        """Test creating last name with valid format."""
        last_name = LastName("Doe")
        assert last_name.value == "Doe"
    
    def test_last_name_normalization(self):
        """Test last name normalization to title case."""
        last_name = LastName("doe")
        assert last_name.value == "Doe"
        
        last_name = LastName("DOE")
        assert last_name.value == "Doe"
    
    def test_last_name_trimming(self):
        """Test last name trimming of whitespace."""
        last_name = LastName("  Doe  ")
        assert last_name.value == "Doe"
    
    def test_last_name_too_short(self):
        """Test last name too short raises error."""
        with pytest.raises(ValueError, match="Last name must be at least 2 characters long"):
            LastName("D")
    
    def test_last_name_too_long(self):
        """Test last name too long raises error."""
        long_name = "A" * 51
        with pytest.raises(ValueError, match="Last name cannot exceed 50 characters"):
            LastName(long_name)
    
    def test_last_name_invalid_characters(self):
        """Test last name with invalid characters raises error."""
        with pytest.raises(ValueError, match="Last name can only contain letters, spaces, and hyphens"):
            LastName("Doe123")
        
        with pytest.raises(ValueError, match="Last name can only contain letters, spaces, and hyphens"):
            LastName("Doe@Smith")
    
    def test_last_name_with_hyphen(self):
        """Test last name with hyphen is valid."""
        last_name = LastName("Smith-Jones")
        assert last_name.value == "Smith-Jones"
    
    def test_empty_last_name(self):
        """Test empty last name raises error."""
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            LastName("")


class TestJWTToken:
    """Test JWTToken value object."""
    
    def test_valid_jwt_token(self):
        """Test creating JWT token with valid format."""
        token = JWTToken("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.signature")
        assert token.value == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.signature"
        assert token.token_type == "Bearer"
    
    def test_jwt_token_authorization_header(self):
        """Test JWT token authorization header format."""
        token = JWTToken("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.signature")
        assert token.authorization_header == "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.signature"
    
    def test_invalid_jwt_token_format(self):
        """Test invalid JWT token format raises error."""
        with pytest.raises(ValueError, match="Invalid JWT token format"):
            JWTToken("invalid-token")
        
        with pytest.raises(ValueError, match="Invalid JWT token format"):
            JWTToken("header.payload")  # Missing signature
    
    def test_empty_jwt_token(self):
        """Test empty JWT token raises error."""
        with pytest.raises(ValueError, match="Token cannot be empty"):
            JWTToken("")


class TestRefreshToken:
    """Test RefreshToken value object."""
    
    def test_valid_refresh_token(self):
        """Test creating refresh token with valid format."""
        token = RefreshToken("a" * 32)
        assert token.value == "a" * 32
    
    def test_refresh_token_too_short(self):
        """Test refresh token too short raises error."""
        with pytest.raises(ValueError, match="Refresh token must be at least 32 characters long"):
            RefreshToken("short")
    
    def test_empty_refresh_token(self):
        """Test empty refresh token raises error."""
        with pytest.raises(ValueError, match="Refresh token cannot be empty"):
            RefreshToken("")


class TestLoginCredentials:
    """Test LoginCredentials value object."""
    
    def test_valid_login_credentials(self):
        """Test creating login credentials with valid data."""
        email = Email("test@example.com")
        credentials = LoginCredentials(email, "password123")
        assert credentials.email == email
        assert credentials.password == "password123"
    
    def test_empty_password_raises_error(self):
        """Test empty password raises error."""
        email = Email("test@example.com")
        with pytest.raises(ValueError, match="Password cannot be empty"):
            LoginCredentials(email, "")


class TestUserRegistration:
    """Test UserRegistration value object."""
    
    def test_valid_user_registration(self):
        """Test creating user registration with valid data."""
        email = Email("test@example.com")
        password = Password("ValidPass123!")
        first_name = FirstName("John")
        last_name = LastName("Doe")
        
        registration = UserRegistration(email, password, first_name, last_name)
        assert registration.email == email
        assert registration.password == password
        assert registration.first_name == first_name
        assert registration.last_name == last_name
    
    def test_user_registration_string_representation(self):
        """Test user registration string representation."""
        email = Email("test@example.com")
        password = Password("ValidPass123!")
        first_name = FirstName("John")
        last_name = LastName("Doe")
        
        registration = UserRegistration(email, password, first_name, last_name)
        assert str(registration) == "Registration for test@example.com"


class TestPasswordResetToken:
    """Test PasswordResetToken value object."""
    
    def test_valid_password_reset_token(self):
        """Test creating password reset token with valid data."""
        expires_at = datetime.now() + timedelta(hours=1)
        token = PasswordResetToken("a" * 32, expires_at)
        assert token.value == "a" * 32
        assert token.expires_at == expires_at
    
    def test_password_reset_token_not_expired(self):
        """Test password reset token not expired."""
        expires_at = datetime.now() + timedelta(hours=1)
        token = PasswordResetToken("a" * 32, expires_at)
        assert token.is_expired() is False
    
    def test_password_reset_token_expired(self):
        """Test password reset token expired."""
        expires_at = datetime.now() - timedelta(hours=1)
        token = PasswordResetToken("a" * 32, expires_at)
        assert token.is_expired() is True
    
    def test_password_reset_token_too_short(self):
        """Test password reset token too short raises error."""
        expires_at = datetime.now() + timedelta(hours=1)
        with pytest.raises(ValueError, match="Reset token must be at least 32 characters long"):
            PasswordResetToken("short", expires_at)
    
    def test_empty_password_reset_token(self):
        """Test empty password reset token raises error."""
        expires_at = datetime.now() + timedelta(hours=1)
        with pytest.raises(ValueError, match="Reset token cannot be empty"):
            PasswordResetToken("", expires_at)
