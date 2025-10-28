"""
API Layer - FastAPI endpoints using Clean Architecture.

Clean Architecture: This layer handles HTTP concerns and delegates business
logic to the application layer through use cases.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from decimal import Decimal
import logging

from ..application.use_cases import (
    CreateProductUseCase, GetProductUseCase, UpdateProductUseCase,
    DeleteProductUseCase, SearchProductsUseCase, GetLowStockProductsUseCase,
    UpdateProductStockUseCase,
    CreateProductRequest, UpdateProductRequest, SearchProductsRequest
)
from ..infrastructure.repositories import SQLiteProductRepository
from ...shared.database import get_database_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


# Dependency injection for repository
def get_product_repository() -> SQLiteProductRepository:
    """Get product repository instance"""
    return SQLiteProductRepository(get_database_path())


# Pydantic models for API requests/responses
from pydantic import BaseModel, Field, validator
from typing import List as TypingList
from datetime import datetime


class ProductResponse(BaseModel):
    """Response model for product data"""
    id: int
    name: str
    description: str
    price: float
    currency: str
    stock_quantity: int
    stock_reserved: int
    low_stock_threshold: int
    category: str
    status: str
    tags: List[str]
    images: List[dict]
    is_available: bool
    is_low_stock: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CreateProductRequestModel(BaseModel):
    """Request model for creating a product"""
    name: str = Field(..., min_length=2, max_length=255, description="Product name")
    description: str = Field(..., min_length=10, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(..., ge=0, description="Initial stock quantity")
    category: str = Field(..., description="Product category")
    tags: Optional[List[str]] = Field(default=[], description="Product tags")
    low_stock_threshold: int = Field(default=10, ge=0, description="Low stock threshold")
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['electronics', 'clothing', 'home', 'sports', 'books', 'beauty', 'automotive', 'toys']
        if v.lower() not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v.lower()


class UpdateProductRequestModel(BaseModel):
    """Request model for updating a product"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    status: Optional[str] = Field(None, pattern='^(draft|active|inactive|discontinued)$')
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            valid_categories = ['electronics', 'clothing', 'home', 'sports', 'books', 'beauty', 'automotive', 'toys']
            if v.lower() not in valid_categories:
                raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
            return v.lower()
        return v


class ProductListResponse(BaseModel):
    """Response model for product list with pagination"""
    products: List[ProductResponse]
    total_count: int
    page: int
    limit: int
    total_pages: int


# API Endpoints

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    request: CreateProductRequestModel,
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Create a new product.
    
    This endpoint creates a new product with the provided information.
    All business rules are enforced through the domain layer.
    """
    try:
        use_case = CreateProductUseCase(repository)
        
        # Convert request to use case request
        create_request = CreateProductRequest(
            name=request.name,
            description=request.description,
            price=request.price,
            stock=request.stock,
            category=request.category,
            tags=request.tags,
            low_stock_threshold=request.low_stock_threshold
        )
        
        # Execute use case
        product = await use_case.execute(create_request)
        
        # Convert to response model
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price.amount),
            currency=product.price.currency,
            stock_quantity=product.stock.quantity,
            stock_reserved=product.stock.reserved,
            low_stock_threshold=product.stock.low_stock_threshold,
            category=product.category.value,
            status=product.status.value,
            tags=product.tags,
            images=[{
                'url': img.url,
                'alt_text': img.alt_text,
                'is_primary': img.is_primary,
                'order': img.order
            } for img in product.images],
            is_available=product.is_available,
            is_low_stock=product.is_low_stock,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Get a product by ID.
    
    Returns the product with the specified ID.
    """
    try:
        use_case = GetProductUseCase(repository)
        product = await use_case.execute(product_id)
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price.amount),
            currency=product.price.currency,
            stock_quantity=product.stock.quantity,
            stock_reserved=product.stock.reserved,
            low_stock_threshold=product.stock.low_stock_threshold,
            category=product.category.value,
            status=product.status.value,
            tags=product.tags,
            images=[{
                'url': img.url,
                'alt_text': img.alt_text,
                'is_primary': img.is_primary,
                'order': img.order
            } for img in product.images],
            is_available=product.is_available,
            is_low_stock=product.is_low_stock,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=ProductListResponse)
async def search_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search_term: Optional[str] = Query(None, description="Search in name and description"),
    tags: Optional[str] = Query(None, description="Comma-separated list of tags"),
    status: Optional[str] = Query(None, description="Filter by status"),
    in_stock_only: bool = Query(False, description="Show only products in stock"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Search and filter products.
    
    Returns a paginated list of products matching the specified criteria.
    """
    try:
        use_case = SearchProductsUseCase(repository)
        
        # Parse tags
        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Create search request
        search_request = SearchProductsRequest(
            category=category,
            min_price=min_price,
            max_price=max_price,
            search_term=search_term,
            tags=tag_list,
            status=status,
            in_stock_only=in_stock_only,
            page=page,
            limit=limit
        )
        
        # Execute use case
        products, total_count = await use_case.execute(search_request)
        
        # Convert to response models
        product_responses = []
        for product in products:
            product_responses.append(ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                price=float(product.price.amount),
                currency=product.price.currency,
                stock_quantity=product.stock.quantity,
                stock_reserved=product.stock.reserved,
                low_stock_threshold=product.stock.low_stock_threshold,
                category=product.category.value,
                status=product.status.value,
                tags=product.tags,
                images=[{
                    'url': img.url,
                    'alt_text': img.alt_text,
                    'is_primary': img.is_primary,
                    'order': img.order
                } for img in product.images],
                is_available=product.is_available,
                is_low_stock=product.is_low_stock,
                created_at=product.created_at,
                updated_at=product.updated_at
            ))
        
        total_pages = (total_count + limit - 1) // limit
        
        return ProductListResponse(
            products=product_responses,
            total_count=total_count,
            page=page,
            limit=limit,
            total_pages=total_pages
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    request: UpdateProductRequestModel,
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Update an existing product.
    
    Updates the product with the specified ID using the provided data.
    Only provided fields will be updated.
    """
    try:
        use_case = UpdateProductUseCase(repository)
        
        # Convert request to use case request
        update_request = UpdateProductRequest(
            product_id=product_id,
            name=request.name,
            description=request.description,
            price=request.price,
            stock=request.stock,
            category=request.category,
            status=request.status,
            low_stock_threshold=request.low_stock_threshold
        )
        
        # Execute use case
        product = await use_case.execute(update_request)
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price.amount),
            currency=product.price.currency,
            stock_quantity=product.stock.quantity,
            stock_reserved=product.stock.reserved,
            low_stock_threshold=product.stock.low_stock_threshold,
            category=product.category.value,
            status=product.status.value,
            tags=product.tags,
            images=[{
                'url': img.url,
                'alt_text': img.alt_text,
                'is_primary': img.is_primary,
                'order': img.order
            } for img in product.images],
            is_available=product.is_available,
            is_low_stock=product.is_low_stock,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Delete a product.
    
    Permanently deletes the product with the specified ID.
    """
    try:
        use_case = DeleteProductUseCase(repository)
        deleted = await use_case.execute(product_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product deleted successfully", "id": product_id}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/low-stock/", response_model=List[ProductResponse])
async def get_low_stock_products(
    threshold: int = Query(10, ge=0, description="Low stock threshold"),
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Get products with low stock.
    
    Returns products that have stock below the specified threshold.
    """
    try:
        use_case = GetLowStockProductsUseCase(repository)
        products = await use_case.execute(threshold)
        
        product_responses = []
        for product in products:
            product_responses.append(ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                price=float(product.price.amount),
                currency=product.price.currency,
                stock_quantity=product.stock.quantity,
                stock_reserved=product.stock.reserved,
                low_stock_threshold=product.stock.low_stock_threshold,
                category=product.category.value,
                status=product.status.value,
                tags=product.tags,
                images=[{
                    'url': img.url,
                    'alt_text': img.alt_text,
                    'is_primary': img.is_primary,
                    'order': img.order
                } for img in product.images],
                is_available=product.is_available,
                is_low_stock=product.is_low_stock,
                created_at=product.created_at,
                updated_at=product.updated_at
            ))
        
        return product_responses
        
    except Exception as e:
        logger.error(f"Error getting low stock products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: int,
    new_stock: int = Query(..., ge=0, description="New stock quantity"),
    repository: SQLiteProductRepository = Depends(get_product_repository)
):
    """
    Update product stock.
    
    Updates the stock quantity for the specified product.
    """
    try:
        use_case = UpdateProductStockUseCase(repository)
        product = await use_case.execute(product_id, new_stock)
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price.amount),
            currency=product.price.currency,
            stock_quantity=product.stock.quantity,
            stock_reserved=product.stock.reserved,
            low_stock_threshold=product.stock.low_stock_threshold,
            category=product.category.value,
            status=product.status.value,
            tags=product.tags,
            images=[{
                'url': img.url,
                'alt_text': img.alt_text,
                'is_primary': img.is_primary,
                'order': img.order
            } for img in product.images],
            is_available=product.is_available,
            is_low_stock=product.is_low_stock,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating product stock {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
