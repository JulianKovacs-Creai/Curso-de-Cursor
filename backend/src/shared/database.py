"""
Shared Database Utilities - Clean Architecture compatible.

This module provides database connection utilities that work with
the Clean Architecture pattern, supporting dependency injection.
"""

import sqlite3
import os
from typing import Optional
from pathlib import Path


def get_database_path() -> str:
    """
    Get the database path for the current environment.
    
    Returns:
        Database file path
    """
    # Get database path from environment or use default
    db_path = os.getenv("DATABASE_PATH", "ecommerce_clean.db")
    
    # Ensure directory exists
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    return db_path


def get_connection() -> sqlite3.Connection:
    """
    Get a database connection with proper configuration.
    
    Returns:
        Configured SQLite connection
        
    Raises:
        ConnectionError: If connection fails
    """
    try:
        db_path = get_database_path()
        conn = sqlite3.connect(db_path)
        
        # Configure connection for better performance and reliability
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA cache_size = 10000")
        conn.execute("PRAGMA temp_store = MEMORY")
        
        return conn
        
    except Exception as e:
        raise ConnectionError(f"Failed to connect to database: {e}")


def check_database_health() -> dict:
    """
    Check database health and return status information.
    
    Returns:
        Dictionary with health status and metrics
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test basic connectivity
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        # Get database info
        cursor.execute("PRAGMA database_list")
        db_info = cursor.fetchall()
        
        # Get table count
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        table_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "healthy",
            "database_path": get_database_path(),
            "connection_test": "passed",
            "table_count": table_count,
            "database_info": db_info
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_path": get_database_path()
        }


def initialize_database():
    """
    Initialize the database with required tables.
    
    This function ensures all necessary tables exist with proper
    schema for the Clean Architecture implementation.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create products table with Clean Architecture schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                currency TEXT DEFAULT 'USD',
                stock_quantity INTEGER NOT NULL DEFAULT 0,
                stock_reserved INTEGER NOT NULL DEFAULT 0,
                low_stock_threshold INTEGER NOT NULL DEFAULT 10,
                category TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                tags TEXT,  -- JSON array of tags
                images TEXT,  -- JSON array of image objects
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Constraints
                CHECK (price > 0),
                CHECK (stock_quantity >= 0),
                CHECK (stock_reserved >= 0),
                CHECK (stock_reserved <= stock_quantity),
                CHECK (low_stock_threshold >= 0),
                CHECK (status IN ('draft', 'active', 'inactive', 'discontinued'))
            )
        ''')
        
        # Create indexes for performance
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)',
            'CREATE INDEX IF NOT EXISTS idx_products_status ON products(status)',
            'CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)',
            'CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock_quantity)',
            'CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)',
            'CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at)'
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized with Clean Architecture schema")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


def reset_database():
    """
    Reset the database by dropping and recreating all tables.
    
    WARNING: This will delete all data!
    """
    try:
        db_path = get_database_path()
        
        if os.path.exists(db_path):
            print("⚠️  WARNING: Deleting existing database...")
            os.remove(db_path)
        
        print("🔧 Recreating database with Clean Architecture schema...")
        initialize_database()
        print("✅ Database reset completed")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        raise