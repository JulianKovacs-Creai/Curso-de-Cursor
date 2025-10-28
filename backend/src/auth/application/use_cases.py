"""
Auth Use Cases
"""
from typing import Optional, Dict, Any
from src.auth.domain.entities import User
from src.auth.domain.value_objects import UserId, Email
from src.auth.infrastructure.jwt_service import JWTService
from src.auth.infrastructure.password_service import PasswordService
from src.auth.infrastructure.user_repository import SQLiteUserRepository

class RegisterUserUseCase:
    """Register new user use case"""
    
    def __init__(self, user_repository: SQLiteUserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(self, email: str, password: str, first_name: str = None, last_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        # Validate password strength
        if not self.password_service.is_password_strong(password):
            raise ValueError("Password does not meet security requirements")
        
        # Check if user already exists
        email_obj = Email(email)
        existing_user = self.user_repository.get_user_by_email(email_obj)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = self.password_service.hash_password(password)
        
        # Create user
        import uuid
        user_id = UserId(f"user_{uuid.uuid4().hex[:8]}")
        user = User(
            id=user_id,
            email=email_obj,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Save user
        created_user = self.user_repository.create_user(user)
        
        return {
            "user_id": created_user.id.value,
            "email": created_user.email.value,
            "message": "User registered successfully"
        }

class LoginUserUseCase:
    """Login user use case"""
    
    def __init__(self, user_repository: SQLiteUserRepository, password_service: PasswordService, jwt_service: JWTService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    def execute(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        # Get user by email
        email_obj = Email(email)
        user = self.user_repository.get_user_by_email(email_obj)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Verify password
        if not self.password_service.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Create tokens
        tokens = self.jwt_service.create_token_pair(user.id.value, user.email.value)
        
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"],
            "user": {
                "id": user.id.value,
                "email": user.email.value,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified
            }
        }

class RefreshTokenUseCase:
    """Refresh token use case"""
    
    def __init__(self, jwt_service: JWTService, user_repository: SQLiteUserRepository):
        self.jwt_service = jwt_service
        self.user_repository = user_repository
    
    def execute(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        # Verify refresh token
        payload = self.jwt_service.verify_refresh_token(refresh_token)
        if not payload:
            raise ValueError("Invalid refresh token")
        
        # Get user
        user_id = UserId(payload["sub"])
        user = self.user_repository.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        # Create new access token
        new_tokens = self.jwt_service.create_token_pair(user.id.value, user.email.value)
        
        return {
            "access_token": new_tokens["access_token"],
            "refresh_token": new_tokens["refresh_token"],
            "token_type": new_tokens["token_type"]
        }

class GetCurrentUserUseCase:
    """Get current user use case"""
    
    def __init__(self, jwt_service: JWTService, user_repository: SQLiteUserRepository):
        self.jwt_service = jwt_service
        self.user_repository = user_repository
    
    def execute(self, access_token: str) -> Dict[str, Any]:
        """Get current user from token"""
        # Verify access token
        payload = self.jwt_service.verify_access_token(access_token)
        if not payload:
            raise ValueError("Invalid access token")
        
        # Get user
        user_id = UserId(payload["sub"])
        user = self.user_repository.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        return {
            "id": user.id.value,
            "email": user.email.value,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified
        }

class LogoutUserUseCase:
    """Logout user use case"""
    
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service
    
    def execute(self, token: str) -> Dict[str, Any]:
        """Logout user by invalidating token"""
        try:
            # Validate token
            payload = self.jwt_service.validate_token(token)
            if not payload:
                raise ValueError("Invalid token")
            
            # In a real implementation, you would add the token to a blacklist
            # For now, we'll just return success
            return {
                "success": True,
                "message": "User logged out successfully"
            }
        except Exception as e:
            raise ValueError(f"Logout failed: {str(e)}")

class VerifyEmailUseCase:
    """Verify email use case"""
    
    def __init__(self, user_repository: SQLiteUserRepository):
        self.user_repository = user_repository
    
    def execute(self, email: str, verification_code: str) -> Dict[str, Any]:
        """Verify user email with verification code"""
        try:
            email_obj = Email(email)
            user = self.user_repository.get_user_by_email(email_obj)
            if not user:
                raise ValueError("User not found")
            
            # In a real implementation, you would verify the code
            # For now, we'll just mark the user as verified
            user.verify()
            self.user_repository.update_user(user)
            
            return {
                "success": True,
                "message": "Email verified successfully"
            }
        except Exception as e:
            raise ValueError(f"Email verification failed: {str(e)}")