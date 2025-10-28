"""
JWT Service Example - Clean Architecture

This module demonstrates a complete JWT authentication service using PyJWT and bcrypt.
It follows Clean Architecture principles with clear separation of concerns.

Features:
- JWT token creation and verification
- Password hashing and verification with bcrypt
- Token expiration and validation
- Comprehensive error handling
"""

import jwt
import bcrypt
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class JWTToken:
    """Value object for JWT token"""
    value: str
    token_type: str = "Bearer"
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Token cannot be empty")
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def authorization_header(self) -> str:
        """Get token formatted for Authorization header"""
        return f"{self.token_type} {self.value}"


class JWTServiceError(Exception):
    """Base exception for JWT service operations"""
    pass


class InvalidTokenError(JWTServiceError):
    """Raised when token is invalid or expired"""
    pass


class TokenExpiredError(JWTServiceError):
    """Raised when token has expired"""
    pass


class JWTService:
    """
    JWT Authentication Service using PyJWT and bcrypt.
    
    This service handles JWT token creation, verification, and password hashing
    following Clean Architecture principles.
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_hours: int = 1):
        """
        Initialize JWT service.
        
        Args:
            secret_key: Secret key for JWT signing
            algorithm: JWT algorithm (default: HS256)
            access_token_expire_hours: Token expiration in hours (default: 1)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_hours = access_token_expire_hours
        self.revoked_tokens: set = set()  # In production, use Redis or database
    
    def create_token(self, user_id: int, email: str, role: str, expires_delta: Optional[timedelta] = None) -> JWTToken:
        """
        Create a JWT token for a user.
        
        Args:
            user_id: User ID
            email: User email
            role: User role
            expires_delta: Custom expiration time
            
        Returns:
            JWT token
            
        Raises:
            JWTServiceError: If token creation fails
        """
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
            raise JWTServiceError(f"Failed to create JWT token: {e}")
    
    def verify_token(self, token: JWTToken) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token payload as dictionary
            
        Raises:
            InvalidTokenError: If token is invalid
            TokenExpiredError: If token has expired
        """
        try:
            # Check if token is revoked
            if token.value in self.revoked_tokens:
                raise InvalidTokenError("Token has been revoked")
            
            # Decode token
            payload = jwt.decode(token.value, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != "access":
                raise InvalidTokenError("Invalid token type")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {e}")
        except Exception as e:
            raise JWTServiceError(f"Token verification failed: {e}")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
            
        Raises:
            JWTServiceError: If hashing fails
        """
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
            
        except Exception as e:
            raise JWTServiceError(f"Failed to hash password: {e}")
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
            
        Raises:
            JWTServiceError: If verification fails
        """
        try:
            # Check if password matches hash
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            
        except Exception as e:
            raise JWTServiceError(f"Failed to verify password: {e}")
    
    def create_refresh_token(self, user_id: int) -> str:
        """
        Create a refresh token for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Refresh token string
        """
        try:
            # Generate secure random token
            token_length = 64
            characters = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(characters) for _ in range(token_length))
            
            # In production, store refresh tokens in database with expiration
            return token
            
        except Exception as e:
            raise JWTServiceError(f"Failed to create refresh token: {e}")
    
    def revoke_token(self, token: JWTToken) -> bool:
        """
        Revoke a JWT token (add to blacklist).
        
        Args:
            token: Token to revoke
            
        Returns:
            True if revoked successfully
        """
        try:
            self.revoked_tokens.add(token.value)
            return True
        except Exception as e:
            raise JWTServiceError(f"Failed to revoke token: {e}")
    
    def is_token_revoked(self, token: JWTToken) -> bool:
        """
        Check if a token is revoked.
        
        Args:
            token: Token to check
            
        Returns:
            True if token is revoked
        """
        return token.value in self.revoked_tokens


# Example usage and factory function
def create_jwt_service(secret_key: str = "your-secret-key-here") -> JWTService:
    """
    Factory function to create a JWT service instance.
    
    Args:
        secret_key: Secret key for JWT signing
        
    Returns:
        JWT service instance
    """
    return JWTService(secret_key)


# Example usage
if __name__ == "__main__":
    # Create JWT service
    jwt_service = create_jwt_service("my-super-secret-key")
    
    # Example: Hash a password
    password = "MySecurePassword123!"
    hashed_password = jwt_service.hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed_password}")
    
    # Example: Verify password
    is_valid = jwt_service.verify_password(password, hashed_password)
    print(f"Password verification: {is_valid}")
    
    # Example: Create JWT token
    user_id = 1
    email = "user@example.com"
    role = "customer"
    
    token = jwt_service.create_token(user_id, email, role)
    print(f"Created token: {token.value}")
    
    # Example: Verify token
    try:
        payload = jwt_service.verify_token(token)
        print(f"Token payload: {payload}")
    except (InvalidTokenError, TokenExpiredError) as e:
        print(f"Token verification failed: {e}")
    
    # Example: Revoke token
    revoked = jwt_service.revoke_token(token)
    print(f"Token revoked: {revoked}")
    
    # Example: Check if token is revoked
    is_revoked = jwt_service.is_token_revoked(token)
    print(f"Token is revoked: {is_revoked}")
