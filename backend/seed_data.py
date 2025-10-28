#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de prueba
"""

import sqlite3
import json
from datetime import datetime

def create_sample_products():
    """Crear productos de ejemplo"""
    products = [
        {
            "name": "iPhone 15 Pro",
            "description": "El iPhone más avanzado con chip A17 Pro",
            "price": 999.99,
            "compare_at_price": 1099.99,
            "sku": "IPH15PRO-001",
            "category": "Electrónicos",
            "brand": "Apple",
            "inventory": {
                "quantity": 50,
                "track_quantity": True,
                "allow_backorder": False,
                "low_stock_threshold": 10
            },
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=300&h=200&fit=crop",
                    "alt": "iPhone 15 Pro",
                    "is_primary": True
                }
            ],
            "tags": ["smartphone", "apple", "premium"],
            "featured": True
        },
        {
            "name": "MacBook Air M2",
            "description": "Laptop ultradelgada con chip M2",
            "price": 1199.99,
            "compare_at_price": 1299.99,
            "sku": "MBA-M2-001",
            "category": "Computadoras",
            "brand": "Apple",
            "inventory": {
                "quantity": 25,
                "track_quantity": True,
                "allow_backorder": True,
                "low_stock_threshold": 5
            },
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=300&h=200&fit=crop",
                    "alt": "MacBook Air M2",
                    "is_primary": True
                }
            ],
            "tags": ["laptop", "apple", "m2"],
            "featured": True
        },
        {
            "name": "Samsung Galaxy S24",
            "description": "Smartphone Android con IA integrada",
            "price": 799.99,
            "compare_at_price": 899.99,
            "sku": "SGS24-001",
            "category": "Electrónicos",
            "brand": "Samsung",
            "inventory": {
                "quantity": 75,
                "track_quantity": True,
                "allow_backorder": False,
                "low_stock_threshold": 15
            },
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=200&fit=crop",
                    "alt": "Samsung Galaxy S24",
                    "is_primary": True
                }
            ],
            "tags": ["smartphone", "samsung", "android"],
            "featured": False
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "Auriculares inalámbricos con cancelación de ruido",
            "price": 399.99,
            "compare_at_price": 449.99,
            "sku": "SONY-WH1000XM5",
            "category": "Audio",
            "brand": "Sony",
            "inventory": {
                "quantity": 30,
                "track_quantity": True,
                "allow_backorder": True,
                "low_stock_threshold": 8
            },
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=200&fit=crop",
                    "alt": "Sony WH-1000XM5",
                    "is_primary": True
                }
            ],
            "tags": ["auriculares", "sony", "noise-cancelling"],
            "featured": True
        },
        {
            "name": "Nike Air Max 270",
            "description": "Zapatillas deportivas con tecnología Air Max",
            "price": 150.00,
            "compare_at_price": 180.00,
            "sku": "NIKE-AM270-001",
            "category": "Calzado",
            "brand": "Nike",
            "inventory": {
                "quantity": 100,
                "track_quantity": True,
                "allow_backorder": False,
                "low_stock_threshold": 20
            },
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=200&fit=crop",
                    "alt": "Nike Air Max 270",
                    "is_primary": True
                }
            ],
            "tags": ["zapatillas", "nike", "deportivas"],
            "featured": False
        }
    ]
    return products

def seed_database():
    """Poblar la base de datos con datos de prueba"""
    conn = sqlite3.connect('ecommerce_clean.db')
    cursor = conn.cursor()
    
    # Crear tabla de productos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            compare_at_price REAL,
            sku TEXT UNIQUE,
            category TEXT,
            brand TEXT,
            inventory TEXT,  -- JSON string
            images TEXT,     -- JSON string
            tags TEXT,       -- JSON string
            featured BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar productos de ejemplo
    products = create_sample_products()
    
    for product in products:
        cursor.execute('''
            INSERT OR REPLACE INTO products 
            (name, description, price, compare_at_price, sku, category, brand, 
             inventory, images, tags, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['name'],
            product['description'],
            product['price'],
            product['compare_at_price'],
            product['sku'],
            product['category'],
            product['brand'],
            json.dumps(product['inventory']),
            json.dumps(product['images']),
            json.dumps(product['tags']),
            product['featured']
        ))
    
    conn.commit()
    conn.close()
    print("✅ Base de datos poblada con productos de ejemplo")

if __name__ == "__main__":
    seed_database()
