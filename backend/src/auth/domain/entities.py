"""
Auth Domain Entities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .value_objects import UserId, Email

@dataclass
class User:
    """User entity"""
    id: UserId
    email: Email
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email.value
    
    def activate(self):
        """Activate user account"""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate user account"""
        self.is_active = False
    
    def verify(self):
        """Mark user as verified"""
        self.is_verified = True