"""
Pytest configuration and fixtures.

This module provides shared fixtures and configuration for all tests.
"""

import pytest
import asyncio
import tempfile
import os
from typing import Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock

from src.shared.database import get_database_path
from src.auth.infrastructure.repositories import SQLiteUserRepository
from src.auth.infrastructure.services import create_jwt_service, create_password_service, create_email_service
from src.products.infrastructure.repositories import SQLiteProductRepository


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_database() -> Generator[str, None, None]:
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
async def user_repository(temp_database: str) -> SQLiteUserRepository:
    """Create a user repository with temporary database."""
    return SQLiteUserRepository(temp_database)


@pytest.fixture
async def product_repository(temp_database: str) -> SQLiteProductRepository:
    """Create a product repository with temporary database."""
    return SQLiteProductRepository(temp_database)


@pytest.fixture
def jwt_service():
    """Create a JWT service for testing."""
    return create_jwt_service("test-secret-key")


@pytest.fixture
def password_service():
    """Create a password service for testing."""
    return create_password_service(rounds=4)  # Faster for testing


@pytest.fixture
def email_service():
    """Create an email service for testing."""
    return create_email_service()


@pytest.fixture
def mock_user_repository():
    """Create a mock user repository."""
    mock = AsyncMock()
    mock.save = AsyncMock()
    mock.get_by_id = AsyncMock()
    mock.get_by_email = AsyncMock()
    mock.exists_by_email = AsyncMock()
    mock.delete = AsyncMock()
    mock.find_all = AsyncMock()
    mock.count = AsyncMock()
    return mock


@pytest.fixture
def mock_jwt_service():
    """Create a mock JWT service."""
    mock = Mock()
    mock.create_token = Mock()
    mock.verify_token = Mock()
    mock.create_refresh_token = Mock()
    mock.verify_refresh_token = Mock()
    mock.revoke_token = Mock()
    mock.is_token_revoked = Mock()
    return mock


@pytest.fixture
def mock_password_service():
    """Create a mock password service."""
    mock = Mock()
    mock.hash_password = Mock()
    mock.verify_password = Mock()
    return mock


@pytest.fixture
def mock_email_service():
    """Create a mock email service."""
    mock = AsyncMock()
    mock.send_verification_email = AsyncMock()
    mock.send_password_reset_email = AsyncMock()
    return mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "A test product for testing purposes",
        "price": 99.99,
        "stock": 10,
        "category": "electronics",
        "tags": ["test", "electronics"]
    }
