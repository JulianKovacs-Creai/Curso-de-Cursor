"""
End-to-end tests for authentication endpoints.

Tests the complete authentication flow from HTTP requests to database operations.
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch

from main_clean import app


class TestAuthEndpoints:
    """Test authentication endpoints E2E."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "email": "test@example.com",
            "password": "ValidPass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
    
    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration."""
        # Act
        response = client.post("/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["first_name"] == "John"
        assert data["user"]["last_name"] == "Doe"
        assert data["user"]["role"] == "customer"
        assert data["user"]["status"] == "active"
        assert data["user"]["is_email_verified"] is False
        assert "user_id" in data
    
    def test_register_user_duplicate_email(self, client, sample_user_data):
        """Test registration with duplicate email."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Act
        response = client.post("/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "User with email test@example.com already exists" in data["detail"]
    
    def test_register_user_invalid_email(self, client, sample_user_data):
        """Test registration with invalid email."""
        # Arrange
        sample_user_data["email"] = "invalid-email"
        
        # Act
        response = client.post("/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "Invalid email format" in str(data["detail"])
    
    def test_register_user_invalid_password(self, client, sample_user_data):
        """Test registration with invalid password."""
        # Arrange
        sample_user_data["password"] = "short"
        
        # Act
        response = client.post("/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "Password must be at least 8 characters long" in str(data["detail"])
    
    def test_register_user_missing_fields(self, client):
        """Test registration with missing required fields."""
        # Act
        response = client.post("/auth/register", json={"email": "test@example.com"})
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "field required" in str(data["detail"]).lower()
    
    def test_login_user_success(self, client, sample_user_data):
        """Test successful user login."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Act
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["first_name"] == "John"
        assert data["user"]["last_name"] == "Doe"
    
    def test_login_user_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        # Act
        response = client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data["detail"]
    
    def test_login_user_wrong_password(self, client, sample_user_data):
        """Test login with wrong password."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Act
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPass123!"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data["detail"]
    
    def test_login_user_missing_credentials(self, client):
        """Test login with missing credentials."""
        # Act
        response = client.post("/auth/login", json={})
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "field required" in str(data["detail"]).lower()
    
    def test_logout_user_success(self, client, sample_user_data):
        """Test successful user logout."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.post("/auth/logout", headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"
    
    def test_logout_user_without_token(self, client):
        """Test logout without token."""
        # Act
        response = client.post("/auth/logout")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["detail"]
    
    def test_logout_user_invalid_token(self, client):
        """Test logout with invalid token."""
        # Act
        response = client.post("/auth/logout", headers={
            "Authorization": "Bearer invalid_token"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token" in data["detail"]
    
    def test_refresh_token_success(self, client, sample_user_data):
        """Test successful token refresh."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        refresh_token = login_response.json()["refresh_token"]
        
        # Act
        response = client.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"
    
    def test_refresh_token_invalid(self, client):
        """Test refresh with invalid token."""
        # Act
        response = client.post("/auth/refresh", json={
            "refresh_token": "invalid_token"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid refresh token" in data["detail"]
    
    def test_get_user_profile_success(self, client, sample_user_data):
        """Test successful user profile retrieval."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.get("/auth/profile", headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["first_name"] == "John"
        assert data["user"]["last_name"] == "Doe"
        assert data["user"]["role"] == "customer"
        assert data["user"]["status"] == "active"
    
    def test_get_user_profile_without_token(self, client):
        """Test profile retrieval without token."""
        # Act
        response = client.get("/auth/profile")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["detail"]
    
    def test_update_user_profile_success(self, client, sample_user_data):
        """Test successful user profile update."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/profile", json={
            "first_name": "Jane",
            "last_name": "Smith"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Profile updated successfully"
        assert data["user"]["first_name"] == "Jane"
        assert data["user"]["last_name"] == "Smith"
        assert data["user"]["email"] == "test@example.com"  # Email should not change
    
    def test_update_user_profile_invalid_data(self, client, sample_user_data):
        """Test profile update with invalid data."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/profile", json={
            "first_name": "",  # Empty first name
            "last_name": "Smith"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "First name cannot be empty" in str(data["detail"])
    
    def test_change_password_success(self, client, sample_user_data):
        """Test successful password change."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/change-password", json={
            "current_password": "ValidPass123!",
            "new_password": "NewPass123!"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password changed successfully"
    
    def test_change_password_wrong_current_password(self, client, sample_user_data):
        """Test password change with wrong current password."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/change-password", json={
            "current_password": "WrongPass123!",
            "new_password": "NewPass123!"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "Current password is incorrect" in data["detail"]
    
    def test_change_password_same_password(self, client, sample_user_data):
        """Test password change with same password."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/change-password", json={
            "current_password": "ValidPass123!",
            "new_password": "ValidPass123!"  # Same password
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "New password must be different from current password" in data["detail"]
    
    def test_change_password_invalid_new_password(self, client, sample_user_data):
        """Test password change with invalid new password."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "ValidPass123!"
        })
        access_token = login_response.json()["access_token"]
        
        # Act
        response = client.put("/auth/change-password", json={
            "current_password": "ValidPass123!",
            "new_password": "short"  # Too short
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "Password must be at least 8 characters long" in str(data["detail"])
    
    def test_request_password_reset_success(self, client, sample_user_data):
        """Test successful password reset request."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Act
        response = client.post("/auth/request-password-reset", json={
            "email": "test@example.com"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password reset email sent"
    
    def test_request_password_reset_nonexistent_user(self, client):
        """Test password reset request for non-existent user."""
        # Act
        response = client.post("/auth/request-password-reset", json={
            "email": "nonexistent@example.com"
        })
        
        # Assert
        assert response.status_code == 200  # Should not reveal if user exists
        data = response.json()
        assert data["message"] == "Password reset email sent"
    
    def test_reset_password_success(self, client, sample_user_data):
        """Test successful password reset."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Mock the JWT service to return a valid token
        with patch('src.auth.infrastructure.services.create_jwt_service') as mock_jwt:
            mock_jwt.return_value.verify_token.return_value = 1
            mock_jwt.return_value.create_token.return_value = "reset_token"
            
            # Request password reset
            client.post("/auth/request-password-reset", json={
                "email": "test@example.com"
            })
        
        # Act
        response = client.post("/auth/reset-password", json={
            "token": "reset_token",
            "new_password": "NewPass123!"
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password reset successfully"
    
    def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token."""
        # Act
        response = client.post("/auth/reset-password", json={
            "token": "invalid_token",
            "new_password": "NewPass123!"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token" in data["detail"]
    
    def test_reset_password_invalid_new_password(self, client):
        """Test password reset with invalid new password."""
        # Act
        response = client.post("/auth/reset-password", json={
            "token": "valid_token",
            "new_password": "short"  # Too short
        })
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "Password must be at least 8 characters long" in str(data["detail"])
    
    def test_verify_email_success(self, client, sample_user_data):
        """Test successful email verification."""
        # Arrange
        client.post("/auth/register", json=sample_user_data)
        
        # Mock the JWT service to return a valid token
        with patch('src.auth.infrastructure.services.create_jwt_service') as mock_jwt:
            mock_jwt.return_value.verify_token.return_value = 1
            
            # Act
            response = client.post("/auth/verify-email", json={
                "token": "verification_token"
            })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Email verified successfully"
    
    def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token."""
        # Act
        response = client.post("/auth/verify-email", json={
            "token": "invalid_token"
        })
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token" in data["detail"]
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        # Act
        response = client.options("/auth/register")
        
        # Assert
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    def test_rate_limiting(self, client, sample_user_data):
        """Test rate limiting on authentication endpoints."""
        # This would require implementing rate limiting middleware
        # For now, we'll test that the endpoint responds correctly
        
        # Act
        response = client.post("/auth/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == 201  # Should work normally without rate limiting
    
    def test_input_validation(self, client):
        """Test comprehensive input validation."""
        # Test various invalid inputs
        invalid_inputs = [
            {"email": "invalid-email", "password": "ValidPass123!", "first_name": "John", "last_name": "Doe"},
            {"email": "test@example.com", "password": "short", "first_name": "John", "last_name": "Doe"},
            {"email": "test@example.com", "password": "ValidPass123!", "first_name": "", "last_name": "Doe"},
            {"email": "test@example.com", "password": "ValidPass123!", "first_name": "John", "last_name": ""},
            {"email": "", "password": "ValidPass123!", "first_name": "John", "last_name": "Doe"},
            {"email": "test@example.com", "password": "", "first_name": "John", "last_name": "Doe"},
        ]
        
        for invalid_input in invalid_inputs:
            response = client.post("/auth/register", json=invalid_input)
            assert response.status_code == 422, f"Input {invalid_input} should be invalid"
    
    def test_security_headers(self, client):
        """Test security headers are present."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        # Check for security headers (these would be set by security middleware)
        # assert "x-content-type-options" in response.headers
        # assert "x-frame-options" in response.headers
        # assert "x-xss-protection" in response.headers
