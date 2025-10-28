import sqlite3
import os
from typing import List, Tuple, Optional

# ❌ PROBLEMA: Hardcoded database path
DATABASE_PATH = "ecommerce.db"

def get_db_connection():
    """
    Get database connection.
    
    ❌ PROBLEMA: No pool de conexiones
    ❌ PROBLEMA: No manejo de errores
    ❌ PROBLEMA: No configuración de timeout
    ❌ PROBLEMA: No foreign keys habilitadas
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        # ❌ PROBLEMA: Foreign keys no habilitadas por defecto
        # conn.execute("PRAGMA foreign_keys = ON")  # Commented out - should be enabled
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        raise

def init_database():
    """
    Initialize database with basic schema.
    
    ❌ PROBLEMA: Schema muy básico sin constraints
    ❌ PROBLEMA: No indices para performance
    ❌ PROBLEMA: No foreign keys
    ❌ PROBLEMA: No audit fields consistentes
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ❌ PROBLEMA: Tabla muy básica sin constraints apropiadas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,                    -- ❌ REAL para dinero (precision issues)
            stock INTEGER NOT NULL DEFAULT 0,
            category TEXT,                          -- ❌ TEXT en vez de foreign key
            description TEXT,
            is_active INTEGER DEFAULT 1,           -- ❌ INTEGER en vez de BOOLEAN
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            -- ❌ PROBLEMA: No constraints de CHECK
            -- ❌ PROBLEMA: No indices para búsquedas
            -- ❌ PROBLEMA: No foreign keys
        )
        ''')
        
        # ❌ PROBLEMA: No índices para columnas consultadas frecuentemente
        # cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
        # cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)')
        # cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active)')
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📦 Inserting sample products...")
            sample_products = [
                ("Laptop HP Pavilion", 899.99, 10, "Electronics", "High performance laptop perfect for work and entertainment"),
                ("iPhone 15 Pro", 999.99, 5, "Electronics", "Latest iPhone model with advanced camera system"),
                ("Coffee Maker Deluxe", 159.99, 15, "Home", "Premium coffee maker for the perfect morning brew"),
                ("Running Shoes Pro", 129.99, 20, "Sports", "Comfortable running shoes for professional athletes"),
                ("Wireless Headphones", 79.99, 25, "Electronics", "Premium sound quality with noise cancellation"),
                ("Smart Watch", 249.99, 12, "Electronics", "Track your fitness and stay connected"),
                ("Yoga Mat Premium", 49.99, 30, "Sports", "High-quality yoga mat for your daily practice"),
                ("Ceramic Coffee Mug", 15.99, 50, "Home", "Beautiful ceramic mug for your favorite beverage"),
                ("Bluetooth Speaker", 89.99, 18, "Electronics", "Portable speaker with amazing sound quality"),
                ("Kitchen Knife Set", 199.99, 8, "Home", "Professional chef knife set for cooking enthusiasts")
            ]
            
            # ❌ PROBLEMA: INSERT sin prepared statements (aunque aquí son datos estáticos)
            cursor.executemany('''
            INSERT INTO products (name, price, stock, category, description)
            VALUES (?, ?, ?, ?, ?)
            ''', sample_products)
            
            print(f"✅ Inserted {len(sample_products)} sample products")
        
        conn.commit()
        print("✅ Products database initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_products_from_db(query: str, params: List = None) -> List[Tuple]:
    """
    Execute SELECT query and return products.
    
    ❌ PROBLEMA: SQL directo sin ORM
    ❌ PROBLEMA: No sanitización de queries
    ❌ PROBLEMA: Parámetro query permite SQL injection
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            # ❌ PROBLEMA: Ejecuta query directamente - SQL INJECTION RISK
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
        
    except Exception as e:
        print(f"❌ Database error in get_products_from_db: {e}")
        print(f"❌ Query was: {query}")
        raise
    finally:
        conn.close()

def get_product_by_id(query: str) -> Optional[Tuple]:
    """
    Get single product by executing query.
    
    ❌ PROBLEMA: Query directo como parámetro
    ❌ PROBLEMA: SQL injection vulnerable
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ❌ PROBLEMA: Ejecuta query sin sanitización
        cursor.execute(query)  # SQL INJECTION RISK!
        result = cursor.fetchone()
        return result
        
    except Exception as e:
        print(f"❌ Database error in get_product_by_id: {e}")
        print(f"❌ Query was: {query}")
        raise
    finally:
        conn.close()

def create_product_in_db(query: str) -> int:
    """
    Create product by executing INSERT query.
    
    ❌ PROBLEMA: No transacciones apropiadas
    ❌ PROBLEMA: No validaciones en DB layer
    ❌ PROBLEMA: SQL injection vulnerable
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ❌ PROBLEMA: Ejecuta INSERT directo - SQL INJECTION RISK
        cursor.execute(query)
        product_id = cursor.lastrowid
        
        # ❌ PROBLEMA: No validación del resultado
        conn.commit()
        return product_id
        
    except Exception as e:
        print(f"❌ Database error in create_product_in_db: {e}")
        print(f"❌ Query was: {query}")
        conn.rollback()
        raise
    finally:
        conn.close()

def update_product_in_db(query: str) -> int:
    """
    Update product by executing UPDATE query.
    
    ❌ PROBLEMA: No verificación de existencia
    ❌ PROBLEMA: No manejo de concurrencia
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ❌ PROBLEMA: UPDATE directo - SQL INJECTION RISK
        cursor.execute(query)
        rows_affected = cursor.rowcount
        
        conn.commit()
        return rows_affected
        
    except Exception as e:
        print(f"❌ Database error in update_product_in_db: {e}")
        print(f"❌ Query was: {query}")
        conn.rollback()
        raise
    finally:
        conn.close()

def delete_product_from_db(query: str) -> int:
    """
    Delete product by executing DELETE query.
    
    ❌ PROBLEMA: Hard delete sin verificaciones
    ❌ PROBLEMA: No verificar dependencias (órdenes)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ❌ PROBLEMA: DELETE directo - SQL INJECTION RISK
        cursor.execute(query)
        rows_affected = cursor.rowcount
        
        conn.commit()
        return rows_affected
        
    except Exception as e:
        print(f"❌ Database error in delete_product_from_db: {e}")
        print(f"❌ Query was: {query}")
        conn.rollback()
        raise
    finally:
        conn.close()

# ❌ PROBLEMA: Initialize database on import (side effect)
if not os.path.exists(DATABASE_PATH):
    print("🔧 Database not found, creating new database...")
    init_database()

# ❌ PROBLEMA: No funciones para:
# - Bulk operations
# - Transactions management
# - Connection pooling
# - Query optimization
# - Schema migrations
# - Backup/restore


