"""
Repository Interfaces - Authentication data access contracts.

Clean Architecture: Domain layer defines interfaces that the infrastructure
layer must implement. This ensures the domain is independent of external
data sources and can be easily tested.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from .entities import User
from .value_objects import Email


class UserRepository(ABC):
    """
    Abstract repository interface for User aggregate.
    
    This interface defines the contract that any user data access
    implementation must follow, regardless of the underlying storage
    technology (SQLite, PostgreSQL, MongoDB, etc.).
    """
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """
        Save or update a user.
        
        Args:
            user: User entity to save
            
        Returns:
            Saved user with generated ID if new
            
        Raises:
            UserRepositoryError: If save operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by its ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            User entity if found, None otherwise
            
        Raises:
            UserRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        """
        Get a user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User entity if found, None otherwise
            
        Raises:
            UserRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """
        Check if a user exists with the given email.
        
        Args:
            email: Email address to check
            
        Returns:
            True if user exists, False otherwise
            
        Raises:
            UserRepositoryError: If check operation fails
        """
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            UserRepositoryError: If delete operation fails
        """
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 50, offset: int = 0) -> List[User]:
        """
        Find all users with pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of user entities
            
        Raises:
            UserRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Count total number of users.
        
        Returns:
            Total number of users
            
        Raises:
            UserRepositoryError: If count operation fails
        """
        pass


class UserRepositoryError(Exception):
    """
    Base exception for user repository operations.
    
    This exception should be raised by repository implementations
    when data access operations fail.
    """
    pass


class UserNotFoundError(UserRepositoryError):
    """Raised when a user is not found"""
    pass


class UserAlreadyExistsError(UserRepositoryError):
    """Raised when trying to create a user that already exists"""
    pass


class UserRepositoryConnectionError(UserRepositoryError):
    """Raised when repository cannot connect to data source"""
    pass


class UserRepositoryValidationError(UserRepositoryError):
    """Raised when repository data validation fails"""
    pass
