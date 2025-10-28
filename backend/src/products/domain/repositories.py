"""
Repository Interfaces - Abstract contracts for data access.

Clean Architecture: Domain layer defines interfaces that the infrastructure
layer must implement. This ensures the domain is independent of external
data sources and can be easily tested.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from .entities import Product
from .value_objects import ProductFilters, PaginationParams


class ProductRepository(ABC):
    """
    Abstract repository interface for Product aggregate.
    
    This interface defines the contract that any product data access
    implementation must follow, regardless of the underlying storage
    technology (SQLite, PostgreSQL, MongoDB, etc.).
    """
    
    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Save or update a product.
        
        Args:
            product: Product entity to save
            
        Returns:
            Saved product with generated ID if new
            
        Raises:
            ProductRepositoryError: If save operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get a product by its ID.
        
        Args:
            product_id: Product ID to search for
            
        Returns:
            Product entity if found, None otherwise
            
        Raises:
            ProductRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """
        Get a product by its SKU.
        
        Args:
            sku: Product SKU to search for
            
        Returns:
            Product entity if found, None otherwise
            
        Raises:
            ProductRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def find_all(
        self, 
        filters: ProductFilters, 
        pagination: PaginationParams
    ) -> Tuple[List[Product], int]:
        """
        Find products with filters and pagination.
        
        Args:
            filters: Search and filter criteria
            pagination: Pagination parameters
            
        Returns:
            Tuple of (products list, total count)
            
        Raises:
            ProductRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        """
        Delete a product by ID.
        
        Args:
            product_id: Product ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ProductRepositoryError: If delete operation fails
        """
        pass
    
    @abstractmethod
    async def exists(self, product_id: int) -> bool:
        """
        Check if a product exists.
        
        Args:
            product_id: Product ID to check
            
        Returns:
            True if exists, False otherwise
            
        Raises:
            ProductRepositoryError: If check operation fails
        """
        pass
    
    @abstractmethod
    async def count(self, filters: ProductFilters = None) -> int:
        """
        Count products matching filters.
        
        Args:
            filters: Optional filter criteria
            
        Returns:
            Number of products matching criteria
            
        Raises:
            ProductRepositoryError: If count operation fails
        """
        pass
    
    @abstractmethod
    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Get products with low stock.
        
        Args:
            threshold: Low stock threshold
            
        Returns:
            List of products with low stock
            
        Raises:
            ProductRepositoryError: If query operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_category(self, category: str) -> List[Product]:
        """
        Get products by category.
        
        Args:
            category: Product category
            
        Returns:
            List of products in category
            
        Raises:
            ProductRepositoryError: If query operation fails
        """
        pass


class ProductRepositoryError(Exception):
    """
    Base exception for product repository operations.
    
    This exception should be raised by repository implementations
    when data access operations fail.
    """
    pass


class ProductNotFoundError(ProductRepositoryError):
    """Raised when a product is not found"""
    pass


class ProductAlreadyExistsError(ProductRepositoryError):
    """Raised when trying to create a product that already exists"""
    pass


class ProductRepositoryConnectionError(ProductRepositoryError):
    """Raised when repository cannot connect to data source"""
    pass


class ProductRepositoryValidationError(ProductRepositoryError):
    """Raised when repository data validation fails"""
    pass
