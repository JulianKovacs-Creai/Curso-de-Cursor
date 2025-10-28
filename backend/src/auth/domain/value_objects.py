"""
Auth Domain Value Objects
"""
import re
from dataclasses import dataclass
from typing import Any

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