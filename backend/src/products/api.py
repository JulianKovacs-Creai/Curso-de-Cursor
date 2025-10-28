from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from .models import Product
from .database import (
    get_products_from_db, 
    create_product_in_db, 
    get_product_by_id, 
    update_product_in_db, 
    delete_product_from_db
)

# ❌ PROBLEMA: Logging básico sin configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

# ❌ PROBLEMA: Lógica de negocio mezclada con presentación
@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search in product name"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip")
):
    """
    Get all products with optional filters.
    
    ❌ PROBLEMA: Business logic in controller
    ❌ PROBLEMA: SQL injection vulnerabilities
    ❌ PROBLEMA: No error handling consistency
    """
    try:
        # ❌ PROBLEMA: Query building manual y vulnerable
        query = "SELECT * FROM products WHERE is_active = 1"
        params = []
        
        # ❌ PROBLEMA: SQL injection vulnerability - string concatenation
        if category:
            query += f" AND category = '{category}'"  # VULNERABLE!
        
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
            
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
            
        if search:
            # ❌ PROBLEMA: SQL injection vulnerability
            query += f" AND name LIKE '%{search}%'"  # VULNERABLE!
        
        query += f" LIMIT {limit} OFFSET {offset}"  # ❌ También vulnerable
        
        logger.info(f"Executing query: {query}")  # ❌ PROBLEMA: Logging sensitive data
        
        # ❌ PROBLEMA: Acceso directo a base de datos
        products_data = get_products_from_db(query, params)
        
        # ❌ PROBLEMA: Transformación manual sin validación
        products = []
        for p in products_data:
            try:
                product = Product(
                    id=p[0],
                    name=p[1],
                    price=p[2],  # ❌ PROBLEMA: Float para dinero
                    stock=p[3],
                    category=p[4],
                    description=p[5] if p[5] else "",
                    is_active=bool(p[6])
                )
                products.append(product)
            except Exception as e:
                # ❌ PROBLEMA: Error silencioso
                logger.error(f"Error parsing product {p[0]}: {e}")
                continue
        
        return products
        
    except Exception as e:
        # ❌ PROBLEMA: Error handling genérico sin contexto
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """
    Get a single product by ID.
    
    ❌ PROBLEMA: No validación de input
    ❌ PROBLEMA: SQL injection vulnerability
    """
    try:
        if product_id <= 0:  # ❌ PROBLEMA: Validación básica en controller
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        # ❌ PROBLEMA: SQL directo vulnerable
        query = f"SELECT * FROM products WHERE id = {product_id} AND is_active = 1"
        product_data = get_product_by_id(query)
        
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # ❌ PROBLEMA: Mapeo manual repetido
        product = Product(
            id=product_data[0],
            name=product_data[1],
            price=product_data[2],
            stock=product_data[3],
            category=product_data[4],
            description=product_data[5] if product_data[5] else "",
            is_active=bool(product_data[6])
        )
        
        return product
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=dict, status_code=201)
async def create_product(product_data: dict):  # ❌ PROBLEMA: dict en vez de Pydantic model
    """
    Create a new product.
    
    ❌ PROBLEMA: No validación con Pydantic
    ❌ PROBLEMA: SQL injection vulnerability
    ❌ PROBLEMA: No transacciones
    """
    try:
        # ❌ PROBLEMA: Validación manual en vez de Pydantic
        name = product_data.get("name")
        price = product_data.get("price")
        stock = product_data.get("stock", 0)
        category = product_data.get("category")
        description = product_data.get("description", "")
        
        # ❌ PROBLEMA: Validaciones básicas en controller
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Product name is required")
        
        if price is None or price <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
            
        if stock < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")
            
        if not category:
            raise HTTPException(status_code=400, detail="Category is required")
        
        # ❌ PROBLEMA: SQL injection vulnerable - string formatting
        query = f"""
        INSERT INTO products (name, price, stock, category, description, is_active) 
        VALUES ('{name}', {price}, {stock}, '{category}', '{description}', 1)
        """
        
        logger.info(f"Creating product with query: {query}")  # ❌ Logging sensitive data
        
        product_id = create_product_in_db(query)
        
        return {
            "message": "Product created successfully",
            "id": product_id,
            "name": name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Error creating product")

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: int, product_data: dict):
    """
    Update an existing product.
    
    ❌ PROBLEMA: Lógica duplicada de create_product
    ❌ PROBLEMA: No verificación de existencia
    ❌ PROBLEMA: Update parcial no manejado correctamente
    """
    try:
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        # ❌ PROBLEMA: No verificar si el producto existe
        name = product_data.get("name")
        price = product_data.get("price")
        stock = product_data.get("stock")
        category = product_data.get("category")
        description = product_data.get("description")
        
        # ❌ PROBLEMA: Update parcial mal manejado
        update_fields = []
        if name:
            update_fields.append(f"name='{name}'")  # ❌ SQL injection
        if price is not None:
            update_fields.append(f"price={price}")
        if stock is not None:
            update_fields.append(f"stock={stock}")
        if category:
            update_fields.append(f"category='{category}'")  # ❌ SQL injection
        if description is not None:
            update_fields.append(f"description='{description}'")  # ❌ SQL injection
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # ❌ PROBLEMA: SQL building manual y vulnerable
        query = f"""
        UPDATE products 
        SET {', '.join(update_fields)}
        WHERE id={product_id} AND is_active=1
        """
        
        logger.info(f"Updating product with query: {query}")
        
        rows_affected = update_product_in_db(query)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "message": "Product updated successfully",
            "id": product_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating product")

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int):
    """
    Delete a product (soft delete by setting is_active=False).
    
    ❌ PROBLEMA: Hard delete sin verificaciones
    ❌ PROBLEMA: No verificar dependencias (órdenes)
    """
    try:
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        # ❌ PROBLEMA: No verificar si tiene órdenes asociadas
        # ❌ PROBLEMA: Hard delete en vez de soft delete
        query = f"DELETE FROM products WHERE id = {product_id}"  # ❌ SQL injection
        
        rows_affected = delete_product_from_db(query)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "message": "Product deleted successfully",
            "id": product_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting product")

# ❌ PROBLEMA: No endpoints para:
# - Bulk operations
# - Stock management
# - Category management
# - Product images
# - Product reviews
# - Inventory tracking