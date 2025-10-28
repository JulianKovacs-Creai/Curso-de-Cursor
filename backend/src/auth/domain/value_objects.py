"""
Auth Domain Value Objects
"""
import re
from dataclasses import dataclass
from typing import Any, Optional

@dataclass(frozen=True)
class UserId:
    """User ID value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("User ID cannot be empty")
        if len(self.value) < 3:
            raise ValueError("User ID must be at least 3 characters long")

@dataclass(frozen=True)
class Email:
    """Email value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Email cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value):
            raise ValueError("Invalid email format")
        
        if len(self.value) > 254:
            raise ValueError("Email is too long")

@dataclass(frozen=True)
class JWTToken:
    """JWT Token value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("JWT Token cannot be empty")
        if len(self.value) < 10:
            raise ValueError("JWT Token is too short")

@dataclass(frozen=True)
class RefreshToken:
    """Refresh Token value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Refresh Token cannot be empty")
        if len(self.value) < 10:
            raise ValueError("Refresh Token is too short")

@dataclass(frozen=True)
class Password:
    """Password value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Password cannot be empty")
        if len(self.value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(self.value) > 128:
            raise ValueError("Password is too long")

@dataclass(frozen=True)
class FirstName:
    """First Name value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("First name cannot be empty")
        if len(self.value) < 2:
            raise ValueError("First name must be at least 2 characters long")
        if len(self.value) > 50:
            raise ValueError("First name is too long")

@dataclass(frozen=True)
class LastName:
    """Last Name value object"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Last name cannot be empty")
        if len(self.value) < 2:
            raise ValueError("Last name must be at least 2 characters long")
        if len(self.value) > 50:
            raise ValueError("Last name is too long")

@dataclass(frozen=True)
class LoginCredentials:
    """Login credentials value object"""
    email: Email
    password: Password
    
    def __post_init__(self):
        if not self.email or not self.password:
            raise ValueError("Email and password are required")

@dataclass(frozen=True)
class UserRegistration:
    """User registration value object"""
    email: Email
    password: Password
    first_name: Optional[FirstName] = None
    last_name: Optional[LastName] = None
    
    def __post_init__(self):
        if not self.email or not self.password:
            raise ValueError("Email and password are required")