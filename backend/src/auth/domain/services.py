"""
Domain Services - Authentication business services.

Clean Architecture: Domain services contain business logic that doesn't
naturally belong to a single entity but is part of the domain.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .value_objects import JWTToken, RefreshToken


class JWTService(ABC):
    """
    Abstract JWT service interface.
    
    This interface defines the contract for JWT token operations,
    allowing different implementations (PyJWT, custom, etc.).
    """
    
    @abstractmethod
    def create_token(self, user_id: int, email: str, role: str, expires_delta: Optional[timedelta] = None) -> JWTToken:
        """
        Create a JWT token for a user.
        
        Args:
            user_id: User ID
            email: User email
            role: User role
            expires_delta: Token expiration time
            
        Returns:
            JWT token
            
        Raises:
            JWTServiceError: If token creation fails
        """
        pass
    
    @abstractmethod
    def verify_token(self, token: JWTToken) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token payload as dictionary
            
        Raises:
            JWTServiceError: If token verification fails
        """
        pass
    
    @abstractmethod
    def create_refresh_token(self, user_id: int) -> RefreshToken:
        """
        Create a refresh token for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Refresh token
            
        Raises:
            JWTServiceError: If refresh token creation fails
        """
        pass
    
    @abstractmethod
    def verify_refresh_token(self, refresh_token: RefreshToken) -> int:
        """
        Verify a refresh token and return user ID.
        
        Args:
            refresh_token: Refresh token to verify
            
        Returns:
            User ID from token
            
        Raises:
            JWTServiceError: If refresh token verification fails
        """
        pass
    
    @abstractmethod
    def revoke_token(self, token: JWTToken) -> bool:
        """
        Revoke a JWT token (add to blacklist).
        
        Args:
            token: Token to revoke
            
        Returns:
            True if revoked successfully
            
        Raises:
            JWTServiceError: If token revocation fails
        """
        pass
    
    @abstractmethod
    def is_token_revoked(self, token: JWTToken) -> bool:
        """
        Check if a token is revoked.
        
        Args:
            token: Token to check
            
        Returns:
            True if token is revoked
        """
        pass


class PasswordService(ABC):
    """
    Abstract password service interface.
    
    This interface defines the contract for password hashing and verification.
    """
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Hash a password using secure algorithm.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
            
        Raises:
            PasswordServiceError: If hashing fails
        """
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
            
        Raises:
            PasswordServiceError: If verification fails
        """
        pass


class EmailService(ABC):
    """
    Abstract email service interface.
    
    This interface defines the contract for sending emails.
    """
    
    @abstractmethod
    async def send_verification_email(self, email: str, verification_token: str) -> bool:
        """
        Send email verification email.
        
        Args:
            email: Recipient email address
            verification_token: Email verification token
            
        Returns:
            True if email sent successfully
            
        Raises:
            EmailServiceError: If email sending fails
        """
        pass
    
    @abstractmethod
    async def send_password_reset_email(self, email: str, reset_token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            email: Recipient email address
            reset_token: Password reset token
            
        Returns:
            True if email sent successfully
            
        Raises:
            EmailServiceError: If email sending fails
        """
        pass


# Exception classes for domain services

class JWTServiceError(Exception):
    """Base exception for JWT service operations"""
    pass


class InvalidTokenError(JWTServiceError):
    """Raised when token is invalid or expired"""
    pass


class TokenExpiredError(JWTServiceError):
    """Raised when token has expired"""
    pass


class TokenRevokedError(JWTServiceError):
    """Raised when token has been revoked"""
    pass


class PasswordServiceError(Exception):
    """Base exception for password service operations"""
    pass


class EmailServiceError(Exception):
    """Base exception for email service operations"""
    pass
