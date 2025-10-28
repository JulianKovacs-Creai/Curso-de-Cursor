"""
User Repository Implementation with SQLite
"""
import sqlite3
from typing import Optional, List
from datetime import datetime
from src.auth.domain.entities import User
from src.auth.domain.value_objects import UserId, Email

class SQLiteUserRepository:
    """SQLite implementation of User Repository"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, user: User) -> User:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (id, email, hashed_password, first_name, last_name, is_active, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.id.value,
                user.email.value,
                user.hashed_password,
                user.first_name,
                user.last_name,
                user.is_active,
                user.is_verified
            ))
            conn.commit()
            return user
        except sqlite3.IntegrityError:
            raise ValueError("User with this email already exists")
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id: UserId) -> Optional[User]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id.value,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def get_user_by_email(self, email: Email) -> Optional[User]:
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email.value,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def update_user(self, user: User) -> User:
        """Update user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET email = ?, hashed_password = ?, first_name = ?, last_name = ?, 
                is_active = ?, is_verified = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            user.email.value,
            user.hashed_password,
            user.first_name,
            user.last_name,
            user.is_active,
            user.is_verified,
            user.id.value
        ))
        
        conn.commit()
        conn.close()
        return user
    
    def delete_user(self, user_id: UserId) -> bool:
        """Delete user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id.value,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return deleted
    
    def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List users with pagination"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_user(row) for row in rows]
    
    def _row_to_user(self, row) -> User:
        """Convert database row to User entity"""
        return User(
            id=UserId(row[0]),
            email=Email(row[1]),
            hashed_password=row[2],
            first_name=row[3],
            last_name=row[4],
            is_active=bool(row[5]),
            is_verified=bool(row[6]),
            created_at=datetime.fromisoformat(row[7]) if row[7] else datetime.now(),
            updated_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now()
        )
