"""
Service Implementations - Authentication infrastructure layer services.

Clean Architecture: Infrastructure layer implements the service interfaces
defined in the domain layer. This layer handles external concerns like
JWT tokens, password hashing, and email sending.
"""

import jwt
import bcrypt
import secrets
import string
from typing import Dict, Any, Optional, Set
from datetime import datetime, timedelta

from ..domain.services import JWTService, PasswordService, EmailService
from ..domain.value_objects import JWTToken, RefreshToken
from ..domain.entities import UserRole


class PyJWTService(JWTService):
    """
    PyJWT implementation of JWT service.
    
    This implementation handles JWT token creation, verification, and management
    using the PyJWT library.
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_hours: int = 1):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_hours = access_token_expire_hours
        self.revoked_tokens: Set[str] = set()  # In production, use Redis or database
    
    def create_token(self, user_id: int, email: str, role: str, expires_delta: Optional[timedelta] = None) -> JWTToken:
        """Create a JWT token for a user"""
        try:
            # Set expiration time
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
            
            # Create payload
            payload = {
                "user_id": user_id,
                "email": email,
                "role": role,
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access"
            }
            
            # Create token
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            
            return JWTToken(token)
            
        except Exception as e:
            raise Exception(f"Failed to create JWT token: {e}")
    
    def verify_token(self, token: JWTToken) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            # Check if token is revoked
            if token.value in self.revoked_tokens:
                raise Exception("Token has been revoked")
            
            # Decode token
            payload = jwt.decode(token.value, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != "access":
                raise Exception("Invalid token type")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError as e:
            raise Exception(f"Invalid token: {e}")
        except Exception as e:
            raise Exception(f"Token verification failed: {e}")
    
    def create_refresh_token(self, user_id: int) -> RefreshToken:
        """Create a refresh token for a user"""
        try:
            # Generate secure random token
            token_length = 64
            characters = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(characters) for _ in range(token_length))
            
            # In production, store refresh tokens in database with expiration
            return RefreshToken(token)
            
        except Exception as e:
            raise Exception(f"Failed to create refresh token: {e}")
    
    def verify_refresh_token(self, refresh_token: RefreshToken) -> int:
        """Verify a refresh token and return user ID"""
        try:
            # In production, verify against database
            # For now, we'll use a simple approach
            # In a real implementation, you'd store refresh tokens in the database
            # with user_id and expiration time
            
            # This is a simplified implementation
            # In production, you should:
            # 1. Store refresh tokens in database
            # 2. Check expiration
            # 3. Verify token exists and is not revoked
            
            # For demo purposes, we'll extract user_id from a simple encoding
            # In production, use proper database lookup
            if len(refresh_token.value) < 32:
                raise Exception("Invalid refresh token format")
            
            # This is a placeholder - in production, lookup in database
            # For now, we'll return a default user_id
            # You should implement proper token-to-user mapping
            return 1  # Placeholder user_id
            
        except Exception as e:
            raise Exception(f"Refresh token verification failed: {e}")
    
    def revoke_token(self, token: JWTToken) -> bool:
        """Revoke a JWT token (add to blacklist)"""
        try:
            self.revoked_tokens.add(token.value)
            return True
        except Exception as e:
            raise Exception(f"Failed to revoke token: {e}")
    
    def is_token_revoked(self, token: JWTToken) -> bool:
        """Check if a token is revoked"""
        return token.value in self.revoked_tokens


class BCryptPasswordService(PasswordService):
    """
    BCrypt implementation of password service.
    
    This implementation handles password hashing and verification
    using the bcrypt library for secure password storage.
    """
    
    def __init__(self, rounds: int = 12):
        self.rounds = rounds
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=self.rounds)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Failed to hash password: {e}")
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            # Check if password matches hash
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            
        except Exception as e:
            raise Exception(f"Failed to verify password: {e}")


class MockEmailService(EmailService):
    """
    Mock implementation of email service for development.
    
    This implementation logs email operations instead of actually sending emails.
    In production, you would implement a real email service using SMTP, SendGrid, etc.
    """
    
    def __init__(self):
        self.sent_emails = []  # Store sent emails for testing
    
    async def send_verification_email(self, email: str, verification_token: str) -> bool:
        """Send email verification email"""
        try:
            # In production, implement actual email sending
            email_data = {
                "to": email,
                "subject": "Email Verification",
                "body": f"Please click the link to verify your email: /verify-email?token={verification_token}",
                "type": "verification",
                "token": verification_token,
                "sent_at": datetime.now()
            }
            
            self.sent_emails.append(email_data)
            print(f"📧 [MOCK] Verification email sent to {email}")
            print(f"   Token: {verification_token}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send verification email: {e}")
            return False
    
    async def send_password_reset_email(self, email: str, reset_token: str) -> bool:
        """Send password reset email"""
        try:
            # In production, implement actual email sending
            email_data = {
                "to": email,
                "subject": "Password Reset",
                "body": f"Please click the link to reset your password: /reset-password?token={reset_token}",
                "type": "password_reset",
                "token": reset_token,
                "sent_at": datetime.now()
            }
            
            self.sent_emails.append(email_data)
            print(f"📧 [MOCK] Password reset email sent to {email}")
            print(f"   Token: {reset_token}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send password reset email: {e}")
            return False
    
    def get_sent_emails(self) -> list:
        """Get list of sent emails (for testing)"""
        return self.sent_emails.copy()
    
    def clear_sent_emails(self):
        """Clear sent emails list (for testing)"""
        self.sent_emails.clear()


# Factory functions for creating service instances

def create_jwt_service(secret_key: str, algorithm: str = "HS256") -> PyJWTService:
    """Create a JWT service instance"""
    return PyJWTService(secret_key, algorithm)


def create_password_service(rounds: int = 12) -> BCryptPasswordService:
    """Create a password service instance"""
    return BCryptPasswordService(rounds)


def create_email_service() -> MockEmailService:
    """Create an email service instance"""
    return MockEmailService()
