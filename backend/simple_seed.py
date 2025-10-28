#!/usr/bin/env python3
"""
Script simple para poblar la base de datos
"""

import sqlite3
import json

def seed_simple_products():
    """Crear productos simples"""
    conn = sqlite3.connect('ecommerce_clean.db')
    cursor = conn.cursor()
    
    # Productos simples
    products = [
        ("iPhone 15 Pro", "El iPhone más avanzado", 999.99, "Electrónicos", "Apple", 50),
        ("MacBook Air M2", "Laptop ultradelgada", 1199.99, "Computadoras", "Apple", 25),
        ("Samsung Galaxy S24", "Smartphone Android", 799.99, "Electrónicos", "Samsung", 75),
        ("Sony WH-1000XM5", "Auriculares inalámbricos", 399.99, "Audio", "Sony", 30),
        ("Nike Air Max 270", "Zapatillas deportivas", 150.00, "Calzado", "Nike", 100)
    ]
    
    for name, description, price, category, brand, quantity in products:
        try:
            cursor.execute('''
                INSERT INTO products (name, description, price, category, brand, inventory_quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, price, category, brand, quantity))
        except sqlite3.OperationalError as e:
            print(f"Error con {name}: {e}")
            # Intentar con estructura mínima
            cursor.execute('''
                INSERT INTO products (name, price)
                VALUES (?, ?)
            ''', (name, price))
    
    conn.commit()
    conn.close()
    print("✅ Productos agregados a la base de datos")

if __name__ == "__main__":
    seed_simple_products()
