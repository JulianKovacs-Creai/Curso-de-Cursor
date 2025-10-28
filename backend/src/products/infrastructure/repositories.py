"""
Repository Implementations - Infrastructure layer data access.

Clean Architecture: Infrastructure layer implements the repository interfaces
defined in the domain layer. This layer handles all external concerns like
database connections, SQL queries, and data mapping.
"""

import sqlite3
import asyncio
from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime

from ..domain.entities import Product, ProductStatus, ProductCategory, Money, Stock, ProductImage
from ..domain.value_objects import ProductFilters, PaginationParams
from ..domain.repositories import (
    ProductRepository, 
    ProductRepositoryError, 
    ProductNotFoundError, 
    ProductAlreadyExistsError,
    ProductRepositoryConnectionError,
    ProductRepositoryValidationError
)


class SQLiteProductRepository(ProductRepository):
    """
    SQLite implementation of ProductRepository.
    
    This implementation handles all database operations for products
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
            
            # Create products table with proper schema
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
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_status ON products(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock_quantity)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            raise ProductRepositoryConnectionError(f"Failed to initialize database: {e}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration"""
        try:
            conn = sqlite3.connect(self.database_path)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            return conn
        except Exception as e:
            raise ProductRepositoryConnectionError(f"Failed to connect to database: {e}")
    
    def _product_from_row(self, row: Tuple) -> Product:
        """Convert database row to Product entity"""
        try:
            import json
            
            # Parse JSON fields
            tags = json.loads(row[10]) if row[10] else []
            images_data = json.loads(row[11]) if row[11] else []
            
            # Create images
            images = []
            for img_data in images_data:
                images.append(ProductImage(
                    url=img_data['url'],
                    alt_text=img_data['alt_text'],
                    is_primary=img_data.get('is_primary', False),
                    order=img_data.get('order', 0)
                ))
            
            # Create domain objects
            price = Money(Decimal(str(row[2])), row[3])
            stock = Stock(
                quantity=row[4],
                reserved=row[5],
                low_stock_threshold=row[6]
            )
            
            # Create product entity
            return Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=price,
                stock=stock,
                category=ProductCategory(row[8]),
                status=ProductStatus(row[9]),
                images=images,
                tags=tags,
                created_at=datetime.fromisoformat(row[12]) if row[12] else None,
                updated_at=datetime.fromisoformat(row[13]) if row[13] else None
            )
            
        except Exception as e:
            raise ProductRepositoryValidationError(f"Failed to convert row to Product: {e}")
    
    def _product_to_row(self, product: Product) -> Tuple:
        """Convert Product entity to database row"""
        try:
            import json
            
            # Serialize JSON fields
            tags_json = json.dumps(product.tags)
            images_json = json.dumps([
                {
                    'url': img.url,
                    'alt_text': img.alt_text,
                    'is_primary': img.is_primary,
                    'order': img.order
                }
                for img in product.images
            ])
            
            return (
                product.id,
                product.name,
                product.description,
                float(product.price.amount),
                product.price.currency,
                product.stock.quantity,
                product.stock.reserved,
                product.stock.low_stock_threshold,
                product.category.value,
                product.status.value,
                tags_json,
                images_json,
                product.created_at.isoformat() if product.created_at else None,
                product.updated_at.isoformat() if product.updated_at else None
            )
            
        except Exception as e:
            raise ProductRepositoryValidationError(f"Failed to convert Product to row: {e}")
    
    async def save(self, product: Product) -> Product:
        """Save or update a product"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if product.id is None:
                # Insert new product
                cursor.execute('''
                    INSERT INTO products (
                        name, description, price, currency, stock_quantity, stock_reserved,
                        low_stock_threshold, category, status, tags, images, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product.name,
                    product.description,
                    float(product.price.amount),
                    product.price.currency,
                    product.stock.quantity,
                    product.stock.reserved,
                    product.stock.low_stock_threshold,
                    product.category.value,
                    product.status.value,
                    json.dumps(product.tags),
                    json.dumps([
                        {
                            'url': img.url,
                            'alt_text': img.alt_text,
                            'is_primary': img.is_primary,
                            'order': img.order
                        }
                        for img in product.images
                    ]),
                    product.created_at.isoformat() if product.created_at else None,
                    product.updated_at.isoformat() if product.updated_at else None
                ))
                
                product_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                # Return product with generated ID
                return Product(
                    id=product_id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    stock=product.stock,
                    category=product.category,
                    status=product.status,
                    images=product.images,
                    tags=product.tags,
                    created_at=product.created_at,
                    updated_at=product.updated_at
                )
            else:
                # Update existing product
                cursor.execute('''
                    UPDATE products SET
                        name = ?, description = ?, price = ?, currency = ?,
                        stock_quantity = ?, stock_reserved = ?, low_stock_threshold = ?,
                        category = ?, status = ?, tags = ?, images = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    product.name,
                    product.description,
                    float(product.price.amount),
                    product.price.currency,
                    product.stock.quantity,
                    product.stock.reserved,
                    product.stock.low_stock_threshold,
                    product.category.value,
                    product.status.value,
                    json.dumps(product.tags),
                    json.dumps([
                        {
                            'url': img.url,
                            'alt_text': img.alt_text,
                            'is_primary': img.is_primary,
                            'order': img.order
                        }
                        for img in product.images
                    ]),
                    product.updated_at.isoformat() if product.updated_at else None,
                    product.id
                ))
                
                conn.commit()
                conn.close()
                return product
                
        except Exception as e:
            raise ProductRepositoryError(f"Failed to save product: {e}")
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._product_from_row(row)
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to get product by ID: {e}")
    
    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get a product by its SKU (using name as SKU for now)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM products WHERE name = ?', (sku,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._product_from_row(row)
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to get product by SKU: {e}")
    
    async def find_all(self, filters: ProductFilters, pagination: PaginationParams) -> Tuple[List[Product], int]:
        """Find products with filters and pagination"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Build WHERE clause
            where_conditions = []
            params = []
            
            if filters.category:
                where_conditions.append("category = ?")
                params.append(filters.category)
            
            if filters.min_price is not None:
                where_conditions.append("price >= ?")
                params.append(float(filters.min_price))
            
            if filters.max_price is not None:
                where_conditions.append("price <= ?")
                params.append(float(filters.max_price))
            
            if filters.search_term:
                where_conditions.append("(name LIKE ? OR description LIKE ?)")
                search_pattern = f"%{filters.search_term}%"
                params.extend([search_pattern, search_pattern])
            
            if filters.status:
                where_conditions.append("status = ?")
                params.append(filters.status)
            
            if filters.in_stock_only:
                where_conditions.append("(stock_quantity - stock_reserved) > 0")
            
            if filters.tags:
                # For simplicity, we'll check if any tag is in the tags JSON
                tag_conditions = []
                for tag in filters.tags:
                    tag_conditions.append("tags LIKE ?")
                    params.append(f'%"{tag}"%')
                where_conditions.append(f"({' OR '.join(tag_conditions)})")
            
            # Build query
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            # Count query
            count_query = f"SELECT COUNT(*) FROM products WHERE {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Data query with pagination
            data_query = f'''
                SELECT * FROM products 
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            '''
            data_params = params + [pagination.limit, pagination.offset]
            cursor.execute(data_query, data_params)
            rows = cursor.fetchall()
            conn.close()
            
            # Convert rows to products
            products = [self._product_from_row(row) for row in rows]
            
            return products, total_count
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to find products: {e}")
    
    async def delete(self, product_id: int) -> bool:
        """Delete a product by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to delete product: {e}")
    
    async def exists(self, product_id: int) -> bool:
        """Check if a product exists"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT 1 FROM products WHERE id = ?', (product_id,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to check product existence: {e}")
    
    async def count(self, filters: ProductFilters = None) -> int:
        """Count products matching filters"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if filters:
                # Build WHERE clause (same logic as find_all)
                where_conditions = []
                params = []
                
                if filters.category:
                    where_conditions.append("category = ?")
                    params.append(filters.category)
                
                if filters.min_price is not None:
                    where_conditions.append("price >= ?")
                    params.append(float(filters.min_price))
                
                if filters.max_price is not None:
                    where_conditions.append("price <= ?")
                    params.append(float(filters.max_price))
                
                if filters.search_term:
                    where_conditions.append("(name LIKE ? OR description LIKE ?)")
                    search_pattern = f"%{filters.search_term}%"
                    params.extend([search_pattern, search_pattern])
                
                if filters.status:
                    where_conditions.append("status = ?")
                    params.append(filters.status)
                
                if filters.in_stock_only:
                    where_conditions.append("(stock_quantity - stock_reserved) > 0")
                
                where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
                query = f"SELECT COUNT(*) FROM products WHERE {where_clause}"
                cursor.execute(query, params)
            else:
                cursor.execute("SELECT COUNT(*) FROM products")
            
            result = cursor.fetchone()[0]
            conn.close()
            
            return result
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to count products: {e}")
    
    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products 
                WHERE (stock_quantity - stock_reserved) <= ?
                ORDER BY (stock_quantity - stock_reserved) ASC
            ''', (threshold,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._product_from_row(row) for row in rows]
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to get low stock products: {e}")
    
    async def get_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products 
                WHERE category = ?
                ORDER BY created_at DESC
            ''', (category,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._product_from_row(row) for row in rows]
            
        except Exception as e:
            raise ProductRepositoryError(f"Failed to get products by category: {e}")
