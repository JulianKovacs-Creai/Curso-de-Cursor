"""
Auth API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.auth.application.use_cases import (
    RegisterUserUseCase, 
    LoginUserUseCase, 
    RefreshTokenUseCase, 
    GetCurrentUserUseCase
)
from src.auth.infrastructure.jwt_service import JWTService
from src.auth.infrastructure.password_service import PasswordService
from src.auth.infrastructure.user_repository import SQLiteUserRepository
from src.shared.config import Settings

# Pydantic models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    is_active: bool
    is_verified: bool

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

# Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency injection
def get_auth_services():
    """Get authentication services"""
    settings = Settings()
    jwt_service = JWTService(settings)
    password_service = PasswordService()
    user_repository = SQLiteUserRepository("ecommerce_clean.db")
    
    return {
        "jwt_service": jwt_service,
        "password_service": password_service,
        "user_repository": user_repository
    }

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """Register a new user"""
    services = get_auth_services()
    use_case = RegisterUserUseCase(
        services["user_repository"],
        services["password_service"]
    )
    
    try:
        result = use_case.execute(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login user"""
    services = get_auth_services()
    use_case = LoginUserUseCase(
        services["user_repository"],
        services["password_service"],
        services["jwt_service"]
    )
    
    try:
        result = use_case.execute(
            email=request.email,
            password=request.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    services = get_auth_services()
    use_case = RefreshTokenUseCase(
        services["jwt_service"],
        services["user_repository"]
    )
    
    try:
        result = use_case.execute(request.refresh_token)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: str = Header(None, alias="Authorization")):
    """Get current user information"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.split(" ")[1]
    services = get_auth_services()
    use_case = GetCurrentUserUseCase(
        services["jwt_service"],
        services["user_repository"]
    )
    
    try:
        result = use_case.execute(token)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Logged out successfully"}