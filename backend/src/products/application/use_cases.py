"""
Use Cases - Application layer business logic.

Clean Architecture: Application layer contains use cases that orchestrate
the domain entities and coordinate with infrastructure through interfaces.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime

from ..domain.entities import Product, ProductStatus, ProductCategory, Money, Stock, ProductImage
from ..domain.value_objects import ProductFilters, PaginationParams, ProductName, ProductDescription
from ..domain.repositories import ProductRepository, ProductNotFoundError, ProductAlreadyExistsError


class CreateProductUseCase:
    """
    Use case for creating a new product.
    
    Orchestrates the creation of a product with business rule validation.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, request: 'CreateProductRequest') -> Product:
        """
        Create a new product.
        
        Args:
            request: Product creation request
            
        Returns:
            Created product
            
        Raises:
            ProductAlreadyExistsError: If product with same name already exists
            ValueError: If business rules are violated
        """
        # Validate business rules
        if request.price <= 0:
            raise ValueError("Product price must be greater than zero")
        
        if request.stock < 0:
            raise ValueError("Product stock cannot be negative")
        
        # Check if product with same name already exists
        existing_products = await self.product_repository.find_all(
            ProductFilters(search_term=request.name),
            PaginationParams(page=1, limit=1)
        )
        
        if existing_products[0]:  # If any products found
            raise ProductAlreadyExistsError(f"Product with name '{request.name}' already exists")
        
        # Create domain objects
        name = ProductName(request.name)
        description = ProductDescription(request.description)
        price = Money(Decimal(str(request.price)))
        stock = Stock(quantity=request.stock, low_stock_threshold=request.low_stock_threshold)
        
        # Create product entity
        product = Product(
            id=None,  # Will be set by repository
            name=str(name),
            description=str(description),
            price=price,
            stock=stock,
            category=ProductCategory(request.category),
            status=ProductStatus.ACTIVE,
            images=[],
            tags=request.tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save through repository
        return await self.product_repository.save(product)


class GetProductUseCase:
    """
    Use case for retrieving a product by ID.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int) -> Product:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Product entity
            
        Raises:
            ProductNotFoundError: If product not found
        """
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        return product


class UpdateProductUseCase:
    """
    Use case for updating an existing product.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, request: 'UpdateProductRequest') -> Product:
        """
        Update an existing product.
        
        Args:
            request: Product update request
            
        Returns:
            Updated product
            
        Raises:
            ProductNotFoundError: If product not found
            ValueError: If business rules are violated
        """
        # Get existing product
        existing_product = await self.product_repository.get_by_id(request.product_id)
        if not existing_product:
            raise ProductNotFoundError(f"Product with ID {request.product_id} not found")
        
        # Apply updates
        updated_product = existing_product
        
        if request.name is not None:
            name = ProductName(request.name)
            updated_product = Product(
                id=updated_product.id,
                name=str(name),
                description=updated_product.description,
                price=updated_product.price,
                stock=updated_product.stock,
                category=updated_product.category,
                status=updated_product.status,
                images=updated_product.images,
                tags=updated_product.tags,
                created_at=updated_product.created_at,
                updated_at=datetime.now()
            )
        
        if request.description is not None:
            description = ProductDescription(request.description)
            updated_product = Product(
                id=updated_product.id,
                name=updated_product.name,
                description=str(description),
                price=updated_product.price,
                stock=updated_product.stock,
                category=updated_product.category,
                status=updated_product.status,
                images=updated_product.images,
                tags=updated_product.tags,
                created_at=updated_product.created_at,
                updated_at=datetime.now()
            )
        
        if request.price is not None:
            if request.price <= 0:
                raise ValueError("Product price must be greater than zero")
            price = Money(Decimal(str(request.price)))
            updated_product = Product(
                id=updated_product.id,
                name=updated_product.name,
                description=updated_product.description,
                price=price,
                stock=updated_product.stock,
                category=updated_product.category,
                status=updated_product.status,
                images=updated_product.images,
                tags=updated_product.tags,
                created_at=updated_product.created_at,
                updated_at=datetime.now()
            )
        
        if request.stock is not None:
            if request.stock < 0:
                raise ValueError("Product stock cannot be negative")
            new_stock = Stock(quantity=request.stock, low_stock_threshold=request.low_stock_threshold or 10)
            updated_product = updated_product.update_stock(new_stock)
        
        if request.category is not None:
            updated_product = Product(
                id=updated_product.id,
                name=updated_product.name,
                description=updated_product.description,
                price=updated_product.price,
                stock=updated_product.stock,
                category=ProductCategory(request.category),
                status=updated_product.status,
                images=updated_product.images,
                tags=updated_product.tags,
                created_at=updated_product.created_at,
                updated_at=datetime.now()
            )
        
        if request.status is not None:
            status = ProductStatus(request.status)
            if status == ProductStatus.ACTIVE:
                updated_product = updated_product.activate()
            elif status == ProductStatus.INACTIVE:
                updated_product = updated_product.deactivate()
            elif status == ProductStatus.DISCONTINUED:
                updated_product = updated_product.discontinue()
        
        # Save updated product
        return await self.product_repository.save(updated_product)


class DeleteProductUseCase:
    """
    Use case for deleting a product.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int) -> bool:
        """
        Delete a product.
        
        Args:
            product_id: Product ID to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ProductNotFoundError: If product not found
        """
        # Check if product exists
        if not await self.product_repository.exists(product_id):
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        # Delete product
        return await self.product_repository.delete(product_id)


class SearchProductsUseCase:
    """
    Use case for searching and filtering products.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, request: 'SearchProductsRequest') -> Tuple[List[Product], int]:
        """
        Search products with filters and pagination.
        
        Args:
            request: Search request with filters and pagination
            
        Returns:
            Tuple of (products list, total count)
        """
        filters = ProductFilters(
            category=request.category,
            min_price=Decimal(str(request.min_price)) if request.min_price else None,
            max_price=Decimal(str(request.max_price)) if request.max_price else None,
            search_term=request.search_term,
            tags=request.tags,
            status=request.status,
            in_stock_only=request.in_stock_only
        )
        
        pagination = PaginationParams(
            page=request.page,
            limit=request.limit
        )
        
        return await self.product_repository.find_all(filters, pagination)


class GetLowStockProductsUseCase:
    """
    Use case for getting products with low stock.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, threshold: int = 10) -> List[Product]:
        """
        Get products with low stock.
        
        Args:
            threshold: Low stock threshold
            
        Returns:
            List of products with low stock
        """
        return await self.product_repository.get_low_stock_products(threshold)


class UpdateProductStockUseCase:
    """
    Use case for updating product stock.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int, new_stock: int) -> Product:
        """
        Update product stock.
        
        Args:
            product_id: Product ID
            new_stock: New stock quantity
            
        Returns:
            Updated product
            
        Raises:
            ProductNotFoundError: If product not found
            ValueError: If stock is negative
        """
        if new_stock < 0:
            raise ValueError("Stock cannot be negative")
        
        # Get existing product
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        # Update stock
        new_stock_obj = Stock(quantity=new_stock, low_stock_threshold=product.stock.low_stock_threshold)
        updated_product = product.update_stock(new_stock_obj)
        
        # Save updated product
        return await self.product_repository.save(updated_product)


# Request/Response DTOs for Use Cases

class CreateProductRequest:
    """Request DTO for creating a product"""
    def __init__(self, name: str, description: str, price: float, stock: int, 
                 category: str, tags: List[str] = None, low_stock_threshold: int = 10):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.tags = tags
        self.low_stock_threshold = low_stock_threshold


class UpdateProductRequest:
    """Request DTO for updating a product"""
    def __init__(self, product_id: int, name: str = None, description: str = None,
                 price: float = None, stock: int = None, category: str = None,
                 status: str = None, low_stock_threshold: int = None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.status = status
        self.low_stock_threshold = low_stock_threshold


class SearchProductsRequest:
    """Request DTO for searching products"""
    def __init__(self, category: str = None, min_price: float = None, max_price: float = None,
                 search_term: str = None, tags: List[str] = None, status: str = None,
                 in_stock_only: bool = False, page: int = 1, limit: int = 20):
        self.category = category
        self.min_price = min_price
        self.max_price = max_price
        self.search_term = search_term
        self.tags = tags
        self.status = status
        self.in_stock_only = in_stock_only
        self.page = page
        self.limit = limit
