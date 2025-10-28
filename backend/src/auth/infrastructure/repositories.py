"""
Repository Implementations - Authentication infrastructure layer data access.

Clean Architecture: Infrastructure layer implements the repository interfaces
defined in the domain layer. This layer handles all external concerns like
database connections, SQL queries, and data mapping.
"""

import sqlite3
import asyncio
from typing import List, Optional
from datetime import datetime

from ..domain.entities import User, UserRole, UserStatus
from ..domain.value_objects import Email
from ..domain.repositories import (
    UserRepository, 
    UserRepositoryError, 
    UserNotFoundError, 
    UserAlreadyExistsError,
    UserRepositoryConnectionError,
    UserRepositoryValidationError
)


class SQLiteUserRepository(UserRepository):
    """
    SQLite implementation of UserRepository.
    
    This implementation handles all database operations for users
    using SQLite as the storage backend.
    """
    
    def __init__(self, database_path: str):
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
                    role TEXT NOT NULL DEFAULT 'customer',
                    status TEXT NOT NULL DEFAULT 'pending_verification',
                    is_email_verified INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login_at TIMESTAMP,
                    
                    -- Constraints
                    CHECK (role IN ('admin', 'customer', 'seller', 'moderator')),
                    CHECK (status IN ('active', 'inactive', 'suspended', 'pending_verification')),
                    CHECK (is_email_verified IN (0, 1))
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_status ON users(status)')
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
                role=UserRole(row[5]),
                status=UserStatus(row[6]),
                is_email_verified=bool(row[7]),
                created_at=datetime.fromisoformat(row[8]) if row[8] else None,
                updated_at=datetime.fromisoformat(row[9]) if row[9] else None,
                last_login_at=datetime.fromisoformat(row[10]) if row[10] else None
            )
        except Exception as e:
            raise UserRepositoryValidationError(f"Failed to convert row to User: {e}")
    
    async def save(self, user: User) -> User:
        """Save or update a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if user.id is None:
                # Insert new user
                cursor.execute('''
                    INSERT INTO users (
                        email, password_hash, first_name, last_name, role, status,
                        is_email_verified, created_at, updated_at, last_login_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user.email,
                    user.password_hash,
                    user.first_name,
                    user.last_name,
                    user.role.value,
                    user.status.value,
                    int(user.is_email_verified),
                    user.created_at.isoformat() if user.created_at else None,
                    user.updated_at.isoformat() if user.updated_at else None,
                    user.last_login_at.isoformat() if user.last_login_at else None
                ))
                
                user_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                # Return user with generated ID
                return User(
                    id=user_id,
                    email=user.email,
                    password_hash=user.password_hash,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=user.role,
                    status=user.status,
                    is_email_verified=user.is_email_verified,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    last_login_at=user.last_login_at
                )
            else:
                # Update existing user
                cursor.execute('''
                    UPDATE users SET
                        email = ?, password_hash = ?, first_name = ?, last_name = ?,
                        role = ?, status = ?, is_email_verified = ?, updated_at = ?, last_login_at = ?
                    WHERE id = ?
                ''', (
                    user.email,
                    user.password_hash,
                    user.first_name,
                    user.last_name,
                    user.role.value,
                    user.status.value,
                    int(user.is_email_verified),
                    user.updated_at.isoformat() if user.updated_at else None,
                    user.last_login_at.isoformat() if user.last_login_at else None,
                    user.id
                ))
                
                conn.commit()
                conn.close()
                return user
                
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise UserAlreadyExistsError(f"User with email {user.email} already exists")
            raise UserRepositoryError(f"Database constraint error: {e}")
        except Exception as e:
            raise UserRepositoryError(f"Failed to save user: {e}")
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by its ID"""
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
    
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get a user by email address"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email.value,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._user_from_row(row)
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to get user by email: {e}")
    
    async def exists_by_email(self, email: Email) -> bool:
        """Check if a user exists with the given email"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT 1 FROM users WHERE email = ?', (email.value,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to check user existence: {e}")
    
    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID"""
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
    
    async def find_all(self, limit: int = 50, offset: int = 0) -> List[User]:
        """Find all users with pagination"""
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
            raise UserRepositoryError(f"Failed to find users: {e}")
    
    async def count(self) -> int:
        """Count total number of users"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            result = cursor.fetchone()[0]
            conn.close()
            
            return result
            
        except Exception as e:
            raise UserRepositoryError(f"Failed to count users: {e}")
