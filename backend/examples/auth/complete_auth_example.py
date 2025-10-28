"""
Complete Authentication Example - Clean Architecture

This module demonstrates a complete authentication system using JWT service
and User Repository together, following Clean Architecture principles.

Features:
- User registration with password hashing
- User login with JWT token generation
- Token verification for protected routes
- Complete authentication flow
"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

from jwt_service_example import JWTService, JWTToken, JWTServiceError, InvalidTokenError, TokenExpiredError
from user_repository_example import UserRepository, User, UserRepositoryError, UserAlreadyExistsError, UserNotFoundError


class AuthenticationService:
    """
    Complete Authentication Service combining JWT and User Repository.
    
    This service demonstrates how to use JWT service and User Repository
    together to implement a complete authentication system.
    """
    
    def __init__(self, jwt_service: JWTService, user_repository: UserRepository):
        """
        Initialize authentication service.
        
        Args:
            jwt_service: JWT service instance
            user_repository: User repository instance
        """
        self.jwt_service = jwt_service
        self.user_repository = user_repository
    
    async def register_user(self, email: str, password: str, first_name: str, last_name: str) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            email: User email address
            password: Plain text password
            first_name: User first name
            last_name: User last name
            
        Returns:
            Dictionary with registration result
            
        Raises:
            UserAlreadyExistsError: If user already exists
            ValueError: If validation fails
        """
        try:
            # Validate input
            if not email or not email.strip():
                raise ValueError("Email is required")
            
            if not password or len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            
            if not first_name or not first_name.strip():
                raise ValueError("First name is required")
            
            if not last_name or not last_name.strip():
                raise ValueError("Last name is required")
            
            # Hash password
            password_hash = self.jwt_service.hash_password(password)
            
            # Create user
            user = await self.user_repository.create_user(
                email=email.strip().lower(),
                password_hash=password_hash,
                first_name=first_name.strip(),
                last_name=last_name.strip()
            )
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name
                }
            }
            
        except UserAlreadyExistsError:
            return {
                "success": False,
                "message": "User with this email already exists"
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Registration failed: {e}"
            }
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login a user and generate JWT token.
        
        Args:
            email: User email address
            password: Plain text password
            
        Returns:
            Dictionary with login result and token
            
        Raises:
            UserNotFoundError: If user not found
            ValueError: If credentials are invalid
        """
        try:
            # Validate input
            if not email or not email.strip():
                raise ValueError("Email is required")
            
            if not password:
                raise ValueError("Password is required")
            
            # Get user by email
            user = await self.user_repository.get_user_by_email(email.strip().lower())
            if not user:
                return {
                    "success": False,
                    "message": "Invalid email or password"
                }
            
            # Verify password
            if not self.jwt_service.verify_password(password, user.password_hash):
                return {
                    "success": False,
                    "message": "Invalid email or password"
                }
            
            # Generate JWT token
            token = self.jwt_service.create_token(
                user_id=user.id,
                email=user.email,
                role="customer"  # Default role for simplicity
            )
            
            return {
                "success": True,
                "message": "Login successful",
                "token": token.value,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name
                }
            }
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Login failed: {e}"
            }
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token and return user information.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dictionary with verification result and user info
        """
        try:
            # Create JWT token object
            jwt_token = JWTToken(token)
            
            # Verify token
            payload = self.jwt_service.verify_token(jwt_token)
            
            # Get user from database
            user = await self.user_repository.get_user_by_id(payload["user_id"])
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            return {
                "success": True,
                "message": "Token is valid",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name
                },
                "token_payload": payload
            }
            
        except (InvalidTokenError, TokenExpiredError) as e:
            return {
                "success": False,
                "message": f"Invalid token: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Token verification failed: {e}"
            }
    
    async def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Get user profile by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user profile
        """
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get user profile: {e}"
            }
    
    async def update_user_profile(self, user_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            updates: Dictionary of fields to update
            
        Returns:
            Dictionary with update result
        """
        try:
            # Validate updates
            allowed_fields = ['first_name', 'last_name']
            filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields and v is not None}
            
            if not filtered_updates:
                return {
                    "success": False,
                    "message": "No valid fields to update"
                }
            
            # Update user
            updated_user = await self.user_repository.update_user(user_id, filtered_updates)
            if not updated_user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            return {
                "success": True,
                "message": "Profile updated successfully",
                "user": {
                    "id": updated_user.id,
                    "email": updated_user.email,
                    "first_name": updated_user.first_name,
                    "last_name": updated_user.last_name,
                    "full_name": updated_user.full_name
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update profile: {e}"
            }


# Factory function
def create_authentication_service(jwt_secret: str = "my-super-secret-key", db_path: str = "example_users.db") -> AuthenticationService:
    """
    Factory function to create an authentication service.
    
    Args:
        jwt_secret: JWT secret key
        db_path: Database file path
        
    Returns:
        Authentication service instance
    """
    from jwt_service_example import create_jwt_service
    from user_repository_example import create_user_repository
    
    jwt_service = create_jwt_service(jwt_secret)
    user_repository = create_user_repository(db_path)
    
    return AuthenticationService(jwt_service, user_repository)


# Example usage
async def main():
    """Demonstrate complete authentication flow"""
    print("🔐 Complete Authentication Example")
    print("=" * 50)
    
    # Create authentication service
    auth_service = create_authentication_service()
    
    # Example 1: Register a new user
    print("\n1. Registering a new user...")
    register_result = await auth_service.register_user(
        email="jane.doe@example.com",
        password="SecurePassword123!",
        first_name="Jane",
        last_name="Doe"
    )
    
    if register_result["success"]:
        print(f"✅ {register_result['message']}")
        print(f"   User: {register_result['user']['full_name']} ({register_result['user']['email']})")
    else:
        print(f"❌ {register_result['message']}")
    
    # Example 2: Login user
    print("\n2. Logging in user...")
    login_result = await auth_service.login_user(
        email="jane.doe@example.com",
        password="SecurePassword123!"
    )
    
    if login_result["success"]:
        print(f"✅ {login_result['message']}")
        print(f"   User: {login_result['user']['full_name']}")
        print(f"   Token: {login_result['token'][:50]}...")
        
        # Store token for next example
        token = login_result["token"]
    else:
        print(f"❌ {login_result['message']}")
        return
    
    # Example 3: Verify token
    print("\n3. Verifying token...")
    verify_result = await auth_service.verify_token(token)
    
    if verify_result["success"]:
        print(f"✅ {verify_result['message']}")
        print(f"   User: {verify_result['user']['full_name']}")
        print(f"   Token payload: {verify_result['token_payload']}")
    else:
        print(f"❌ {verify_result['message']}")
    
    # Example 4: Get user profile
    print("\n4. Getting user profile...")
    user_id = verify_result["user"]["id"]
    profile_result = await auth_service.get_user_profile(user_id)
    
    if profile_result["success"]:
        print(f"✅ Profile retrieved")
        print(f"   User: {profile_result['user']['full_name']}")
        print(f"   Email: {profile_result['user']['email']}")
        print(f"   Created: {profile_result['user']['created_at']}")
    else:
        print(f"❌ {profile_result['message']}")
    
    # Example 5: Update user profile
    print("\n5. Updating user profile...")
    update_result = await auth_service.update_user_profile(
        user_id,
        {"first_name": "Jane", "last_name": "Smith"}
    )
    
    if update_result["success"]:
        print(f"✅ {update_result['message']}")
        print(f"   Updated user: {update_result['user']['full_name']}")
    else:
        print(f"❌ {update_result['message']}")
    
    # Example 6: Try to login with wrong password
    print("\n6. Testing wrong password...")
    wrong_login = await auth_service.login_user(
        email="jane.doe@example.com",
        password="WrongPassword123!"
    )
    
    if wrong_login["success"]:
        print(f"✅ {wrong_login['message']}")
    else:
        print(f"❌ {wrong_login['message']}")
    
    # Example 7: Try to verify invalid token
    print("\n7. Testing invalid token...")
    invalid_verify = await auth_service.verify_token("invalid.token.here")
    
    if invalid_verify["success"]:
        print(f"✅ {invalid_verify['message']}")
    else:
        print(f"❌ {invalid_verify['message']}")
    
    print("\n🎉 Authentication example completed!")


if __name__ == "__main__":
    # Run the complete authentication example
    asyncio.run(main())
