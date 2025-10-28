"""
JWT Service Implementation with PyJWT
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from src.shared.config import Settings

class JWTService:
    """JWT Service for token generation and validation"""
    
    def __init__(self, settings: Settings):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = settings.jwt_access_token_expire_minutes
        self.refresh_token_expire_days = settings.jwt_refresh_token_expire_days
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify access token specifically"""
        payload = self.verify_token(token)
        if payload and payload.get("type") == "access":
            return payload
        return None
    
    def verify_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify refresh token specifically"""
        payload = self.verify_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None
    
    def create_token_pair(self, user_id: str, email: str) -> Dict[str, str]:
        """Create both access and refresh tokens"""
        data = {"sub": user_id, "email": email}
        
        return {
            "access_token": self.create_access_token(data),
            "refresh_token": self.create_refresh_token(data),
            "token_type": "bearer"
        }
