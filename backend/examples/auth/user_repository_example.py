"""
User Repository Example - Clean Architecture

This module demonstrates a User Repository implementation using SQLite
following Clean Architecture principles.

Features:
- User CRUD operations with SQLite
- Clean Architecture separation of concerns
- Proper error handling and validation
- Database schema management
"""

import sqlite3
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """
    User entity representing a user in the system.
    
    This is a simple domain entity that contains user data
    and basic business logic.
    """
    id: Optional[int]
    email: str
    password_hash: str
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if not self.email or not self.email.strip():
            raise ValueError("Email cannot be empty")
        
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        
        if not self.password_hash or not self.password_hash.strip():
            raise ValueError("Password hash cannot be empty")
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class UserRepositoryError(Exception):
    """Base exception for user repository operations"""
    pass


class UserNotFoundError(UserRepositoryError):
    """Raised when a user is not found"""
    pass


class UserAlreadyExistsError(UserRepositoryError):
    """Raised when trying to create a user that already exists"""
    pass


class UserRepositoryConnectionError(UserRepositoryError):
    """Raised when repository cannot connect to database"""
    pass


class UserRepository:
    """
    User Repository implementation using SQLite.
    
    This repository handles all database operations for users
    following Clean Architecture principles.
    """
    
    def __init__(self, database_path: str = "example_users.db"):
        """
        Initialize user repository.
        
        Args:
            database_path: Path to SQLite database file
        """
        self.database_path = database_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure database and tables exist"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Create users table with proper schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            raise UserRepositoryConnectionError(f"Failed to initialize database: {e}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration"""
        try:
            conn = sqlite3.connect(self.database_path)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            return conn
        except Exception as e:
            raise UserRepositoryConnectionError(f"Failed to connect to database: {e}")
    
    def _user_from_row(self, row: tuple) -> User:
        """Convert database row to User entity"""
        try:
            return User(
                id=row[0],
                email=row[1],
                password_hash=row[2],
                first_name=row[3],
                last_name=row[4],
                created_at=datetime.fromisoformat(row[5]) if row[5] else None
            )
        except Exception as e:
            raise UserRepositoryError(f"Failed to convert row to User: {e}")
    
    async def create_user(self, email: str, password_hash: str, first_name: str, last_name: str) -> User:
        """
        Create a new user.
        
        Args:
            email: User email address
            password_hash: Hashed password
            first_name: User first name
            last_name: User last name
            
        Returns:
            Created user entity
            
        Raises:
            UserAlreadyExistsError: If user with email already exists
            UserRepositoryError: If creation fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                raise UserAlreadyExistsError(f"User with email {email} already exists")
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, password_hash, first_name, last_name, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password_hash, first_name, last_name, datetime.now().isoformat()))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Return created user
            return User(
                id=user_id,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                created_at=datetime.now()
            )
            
        except UserAlreadyExistsError:
            raise
        except Exception as e:
            raise UserRepositoryError(f"Failed to create user: {e}")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User entity if found, None otherwise
            
        Raises:
            UserRepositoryError: If query fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._user_from_row(row)
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to get user by email: {e}")
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            User entity if found, None otherwise
            
        Raises:
            UserRepositoryError: If query fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._user_from_row(row)
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to get user by ID: {e}")
    
    async def update_user(self, user_id: int, updates: Dict[str, Any]) -> Optional[User]:
        """
        Update a user.
        
        Args:
            user_id: User ID to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated user entity if found, None otherwise
            
        Raises:
            UserRepositoryError: If update fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                conn.close()
                return None
            
            # Build update query
            allowed_fields = ['email', 'password_hash', 'first_name', 'last_name']
            update_fields = []
            values = []
            
            for field, value in updates.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                conn.close()
                raise ValueError("No valid fields to update")
            
            # Add user_id to values
            values.append(user_id)
            
            # Execute update
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            
            # Return updated user
            return await self.get_user_by_id(user_id)
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to update user: {e}")
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            UserRepositoryError: If deletion fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to delete user: {e}")
    
    async def list_users(self, limit: int = 50, offset: int = 0) -> List[User]:
        """
        List users with pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of user entities
            
        Raises:
            UserRepositoryError: If query fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM users 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._user_from_row(row) for row in rows]
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to list users: {e}")
    
    async def count_users(self) -> int:
        """
        Count total number of users.
        
        Returns:
            Total number of users
            
        Raises:
            UserRepositoryError: If count fails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            result = cursor.fetchone()[0]
            conn.close()
            
            return result
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to count users: {e}")


# Factory function
def create_user_repository(database_path: str = "example_users.db") -> UserRepository:
    """
    Factory function to create a user repository instance.
    
    Args:
        database_path: Path to SQLite database file
        
    Returns:
        User repository instance
    """
    return UserRepository(database_path)


# Example usage
if __name__ == "__main__":
    async def main():
        # Create user repository
        user_repo = create_user_repository()
        
        # Example: Create a user
        try:
            user = await user_repo.create_user(
                email="john.doe@example.com",
                password_hash="$2b$12$example_hash_here",
                first_name="John",
                last_name="Doe"
            )
            print(f"Created user: {user.full_name} ({user.email})")
        except UserAlreadyExistsError as e:
            print(f"User already exists: {e}")
        
        # Example: Get user by email
        user = await user_repo.get_user_by_email("john.doe@example.com")
        if user:
            print(f"Found user: {user.full_name}")
        else:
            print("User not found")
        
        # Example: Update user
        if user:
            updated_user = await user_repo.update_user(
                user.id,
                {"first_name": "Johnny", "last_name": "Smith"}
            )
            if updated_user:
                print(f"Updated user: {updated_user.full_name}")
        
        # Example: List users
        users = await user_repo.list_users(limit=10)
        print(f"Total users: {len(users)}")
        
        # Example: Count users
        count = await user_repo.count_users()
        print(f"User count: {count}")
    
    # Run example
    asyncio.run(main())
