"""
Domain Entities - Core business objects with business logic.

Clean Architecture: Domain layer contains the core business logic
and is independent of external concerns like databases, APIs, etc.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductStatus(Enum):
    """Product status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class ProductCategory(Enum):
    """Product category enumeration"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    SPORTS = "sports"
    BOOKS = "books"
    BEAUTY = "beauty"
    AUTOMOTIVE = "automotive"
    TOYS = "toys"


@dataclass(frozen=True)
class Money:
    """
    Value Object for money with currency.
    
    Ensures precision in financial calculations and prevents
    floating-point errors common with float types.
    """
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter code")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, multiplier: float) -> 'Money':
        return Money(self.amount * Decimal(str(multiplier)), self.currency)
    
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class Stock:
    """
    Value Object for inventory management.
    
    Encapsulates stock-related business rules and calculations.
    """
    quantity: int
    reserved: int = 0
    low_stock_threshold: int = 10
    
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        if self.reserved < 0:
            raise ValueError("Reserved quantity cannot be negative")
        if self.reserved > self.quantity:
            raise ValueError("Reserved quantity cannot exceed available quantity")
        if self.low_stock_threshold < 0:
            raise ValueError("Low stock threshold cannot be negative")
    
    @property
    def available(self) -> int:
        """Available stock for sale"""
        return self.quantity - self.reserved
    
    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below threshold"""
        return self.available <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self) -> bool:
        """Check if product is out of stock"""
        return self.available <= 0
    
    def can_reserve(self, quantity: int) -> bool:
        """Check if we can reserve the requested quantity"""
        return quantity > 0 and quantity <= self.available
    
    def reserve(self, quantity: int) -> 'Stock':
        """Create new stock with additional reserved quantity"""
        if not self.can_reserve(quantity):
            raise ValueError(f"Cannot reserve {quantity} units. Available: {self.available}")
        return Stock(
            quantity=self.quantity,
            reserved=self.reserved + quantity,
            low_stock_threshold=self.low_stock_threshold
        )
    
    def release_reservation(self, quantity: int) -> 'Stock':
        """Release reserved quantity"""
        if quantity > self.reserved:
            raise ValueError(f"Cannot release {quantity} units. Reserved: {self.reserved}")
        return Stock(
            quantity=self.quantity,
            reserved=self.reserved - quantity,
            low_stock_threshold=self.low_stock_threshold
        )


@dataclass(frozen=True)
class ProductImage:
    """Value Object for product images"""
    url: str
    alt_text: str
    is_primary: bool = False
    order: int = 0
    
    def __post_init__(self):
        if not self.url or not self.url.strip():
            raise ValueError("Image URL cannot be empty")
        if not self.alt_text or not self.alt_text.strip():
            raise ValueError("Alt text cannot be empty")
        if self.order < 0:
            raise ValueError("Image order cannot be negative")


@dataclass
class Product:
    """
    Domain Entity for Product.
    
    Contains core business logic and rules for product management.
    This is the heart of the domain and should be independent of
    external concerns like databases or APIs.
    """
    id: Optional[int]
    name: str
    description: str
    price: Money
    stock: Stock
    category: ProductCategory
    status: ProductStatus
    images: List[ProductImage] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Product name cannot exceed 255 characters")
        if not self.description or not self.description.strip():
            raise ValueError("Product description cannot be empty")
        if len(self.description) > 1000:
            raise ValueError("Product description cannot exceed 1000 characters")
        if self.price.amount <= 0:
            raise ValueError("Product price must be greater than zero")
    
    @property
    def is_available(self) -> bool:
        """Check if product is available for purchase"""
        return (self.status == ProductStatus.ACTIVE and 
                not self.stock.is_out_of_stock)
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product has low stock"""
        return self.stock.is_low_stock
    
    @property
    def primary_image(self) -> Optional[ProductImage]:
        """Get the primary image or first image"""
        primary = next((img for img in self.images if img.is_primary), None)
        return primary or (self.images[0] if self.images else None)
    
    def can_be_purchased(self, quantity: int) -> bool:
        """Check if the requested quantity can be purchased"""
        return (self.is_available and 
                quantity > 0 and 
                quantity <= self.stock.available)
    
    def apply_discount(self, discount_percentage: float) -> 'Product':
        """Apply discount to product price"""
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        discount_multiplier = Decimal(str(1 - discount_percentage / 100))
        new_price = self.price * float(discount_multiplier)
        
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=new_price,
            stock=self.stock,
            category=self.category,
            status=self.status,
            images=self.images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def update_stock(self, new_stock: Stock) -> 'Product':
        """Update product stock"""
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=new_stock,
            category=self.category,
            status=self.status,
            images=self.images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def activate(self) -> 'Product':
        """Activate the product"""
        if self.status == ProductStatus.DISCONTINUED:
            raise ValueError("Cannot activate discontinued product")
        
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=self.stock,
            category=self.category,
            status=ProductStatus.ACTIVE,
            images=self.images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def deactivate(self) -> 'Product':
        """Deactivate the product"""
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=self.stock,
            category=self.category,
            status=ProductStatus.INACTIVE,
            images=self.images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def discontinue(self) -> 'Product':
        """Discontinue the product"""
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=self.stock,
            category=self.category,
            status=ProductStatus.DISCONTINUED,
            images=self.images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def add_image(self, image: ProductImage) -> 'Product':
        """Add an image to the product"""
        if image in self.images:
            raise ValueError("Image already exists")
        
        new_images = self.images + [image]
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=self.stock,
            category=self.category,
            status=self.status,
            images=new_images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def remove_image(self, image_url: str) -> 'Product':
        """Remove an image from the product"""
        new_images = [img for img in self.images if img.url != image_url]
        if len(new_images) == len(self.images):
            raise ValueError("Image not found")
        
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            stock=self.stock,
            category=self.category,
            status=self.status,
            images=new_images,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
