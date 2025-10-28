"""
Pytest Configuration and Fixtures

This module provides comprehensive test fixtures and configuration
for the authentication examples testing suite.
"""

import pytest
import tempfile
import os
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from jwt_service_example import JWTService, JWTToken
from user_repository_example import UserRepository, User
from complete_auth_example import AuthenticationService


# Pytest configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Database fixtures
@pytest.fixture
def temp_database():
    """Create a temporary database for testing."""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    yield temp_db.name
    # Cleanup
    if os.path.exists(temp_db.name):
        os.unlink(temp_db.name)


@pytest.fixture
async def user_repository(temp_database):
    """Create a user repository with temporary database."""
    repo = UserRepository(temp_database)
    yield repo


# JWT Service fixtures
@pytest.fixture
def jwt_service():
    """Create a JWT service for testing."""
    return JWTService("test-secret-key")


@pytest.fixture
def jwt_token(jwt_service):
    """Create a valid JWT token for testing."""
    return jwt_service.create_token(1, "test@example.com", "customer")


@pytest.fixture
def expired_jwt_token(jwt_service):
    """Create an expired JWT token for testing."""
    return jwt_service.create_token(
        1, "test@example.com", "customer", 
        expires_delta=timedelta(seconds=-1)
    )


# User fixtures
@pytest.fixture
def sample_user():
    """Create a sample user entity."""
    return User(
        id=1,
        email="test@example.com",
        password_hash="$2b$12$example_hash_here",
        first_name="John",
        last_name="Doe",
        created_at=datetime.now()
    )


@pytest.fixture
def sample_users():
    """Create multiple sample users."""
    return [
        User(
            id=1,
            email="user1@example.com",
            password_hash="$2b$12$hash1",
            first_name="User",
            last_name="One",
            created_at=datetime.now()
        ),
        User(
            id=2,
            email="user2@example.com",
            password_hash="$2b$12$hash2",
            first_name="User",
            last_name="Two",
            created_at=datetime.now()
        ),
        User(
            id=3,
            email="user3@example.com",
            password_hash="$2b$12$hash3",
            first_name="User",
            last_name="Three",
            created_at=datetime.now()
        )
    ]


# Authentication service fixtures
@pytest.fixture
async def auth_service(temp_database):
    """Create an authentication service for testing."""
    jwt_service = JWTService("test-secret-key")
    user_repo = UserRepository(temp_database)
    return AuthenticationService(jwt_service, user_repo)


# Mock fixtures
@pytest.fixture
def mock_jwt_service():
    """Create a mock JWT service."""
    mock = Mock(spec=JWTService)
    mock.create_token.return_value = JWTToken("mock_token")
    mock.verify_token.return_value = {"user_id": 1, "email": "test@example.com", "role": "customer"}
    mock.hash_password.return_value = "$2b$12$mock_hash"
    mock.verify_password.return_value = True
    mock.revoke_token.return_value = True
    mock.is_token_revoked.return_value = False
    return mock


@pytest.fixture
def mock_user_repository():
    """Create a mock user repository."""
    mock = Mock(spec=UserRepository)
    mock.create_user = AsyncMock()
    mock.get_user_by_email = AsyncMock()
    mock.get_user_by_id = AsyncMock()
    mock.update_user = AsyncMock()
    mock.delete_user = AsyncMock()
    mock.list_users = AsyncMock()
    mock.count_users = AsyncMock()
    return mock


@pytest.fixture
def mock_database_connection():
    """Create a mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_cursor.rowcount = 0
    mock_cursor.lastrowid = 1
    return mock_conn


# Test data fixtures
@pytest.fixture
def valid_registration_data():
    """Valid user registration data."""
    return {
        "email": "newuser@example.com",
        "password": "SecurePassword123!",
        "first_name": "New",
        "last_name": "User"
    }


@pytest.fixture
def invalid_registration_data():
    """Invalid user registration data."""
    return {
        "email": "invalid-email",
        "password": "123",  # Too short
        "first_name": "",
        "last_name": ""
    }


@pytest.fixture
def valid_login_data():
    """Valid login data."""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }


@pytest.fixture
def invalid_login_data():
    """Invalid login data."""
    return {
        "email": "nonexistent@example.com",
        "password": "WrongPassword"
    }


# Database test data
@pytest.fixture
async def populated_database(user_repository, sample_users):
    """Populate database with test users."""
    for user in sample_users:
        await user_repository.create_user(
            user.email,
            user.password_hash,
            user.first_name,
            user.last_name
        )
    return sample_users


# Performance test fixtures
@pytest.fixture
def performance_test_data():
    """Generate large dataset for performance testing."""
    users = []
    for i in range(100):
        users.append({
            "email": f"user{i}@example.com",
            "password_hash": f"$2b$12$hash{i}",
            "first_name": f"User{i}",
            "last_name": f"Test{i}"
        })
    return users


# Error simulation fixtures
@pytest.fixture
def database_error_simulation():
    """Simulate database errors."""
    def _simulate_error(error_type: str):
        if error_type == "connection":
            raise Exception("Database connection failed")
        elif error_type == "constraint":
            raise Exception("UNIQUE constraint failed")
        elif error_type == "timeout":
            raise Exception("Database timeout")
        else:
            raise Exception("Unknown database error")
    return _simulate_error


# Security test fixtures
@pytest.fixture
def malicious_inputs():
    """Malicious inputs for security testing."""
    return {
        "sql_injection": "'; DROP TABLE users; --",
        "xss_script": "<script>alert('xss')</script>",
        "path_traversal": "../../../etc/passwd",
        "long_input": "A" * 10000,
        "unicode_input": "测试用户",
        "special_chars": "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    }


# Test utilities
class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user_data(**kwargs):
        """Create user data with defaults."""
        defaults = {
            "email": "test@example.com",
            "password_hash": "$2b$12$example_hash",
            "first_name": "Test",
            "last_name": "User"
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_jwt_payload(**kwargs):
        """Create JWT payload with defaults."""
        defaults = {
            "user_id": 1,
            "email": "test@example.com",
            "role": "customer",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        defaults.update(kwargs)
        return defaults


@pytest.fixture
def test_data_factory():
    """Test data factory fixture."""
    return TestDataFactory


# Coverage configuration
@pytest.fixture(autouse=True)
def configure_coverage():
    """Configure coverage settings."""
    # This fixture runs automatically for all tests
    pass


# Test markers
def pytest_configure(config):
    """Configure custom test markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "security: Security tests")
    config.addinivalue_line("markers", "performance: Performance tests")


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add unit marker to tests in test_examples.py
        if "test_examples.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to database tests
        if "database" in item.name or "repository" in item.name:
            item.add_marker(pytest.mark.integration)
        
        # Add e2e marker to complete flow tests
        if "complete" in item.name or "flow" in item.name:
            item.add_marker(pytest.mark.e2e)
        
        # Add security marker to security tests
        if "security" in item.name or "malicious" in item.name:
            item.add_marker(pytest.mark.security)


# Test reporting
def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "Authentication Examples Test Report"


def pytest_html_results_table_header(cells):
    """Customize HTML report table header."""
    cells.insert(1, html.th('Coverage'))
    cells.insert(2, html.th('Duration'))


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows."""
    cells.insert(1, html.td(report.coverage))
    cells.insert(2, html.td(report.duration))
