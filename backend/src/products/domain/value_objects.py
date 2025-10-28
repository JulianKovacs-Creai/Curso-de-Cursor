"""
Value Objects - Immutable objects that represent concepts in the domain.

Value Objects are defined by their attributes, not by their identity.
They are immutable and contain no business logic that changes state.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List
import re


@dataclass(frozen=True)
class ProductName:
    """
    Value Object for product name with validation.
    
    Ensures product names follow business rules and are properly formatted.
    """
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Product name cannot be empty")
        
        if len(self.value.strip()) < 2:
            raise ValueError("Product name must be at least 2 characters")
        
        if len(self.value) > 255:
            raise ValueError("Product name cannot exceed 255 characters")
        
        # Remove extra whitespace
        object.__setattr__(self, 'value', self.value.strip())
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ProductDescription:
    """
    Value Object for product description with validation.
    """
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Product description cannot be empty")
        
        if len(self.value.strip()) < 10:
            raise ValueError("Product description must be at least 10 characters")
        
        if len(self.value) > 1000:
            raise ValueError("Product description cannot exceed 1000 characters")
        
        # Remove extra whitespace
        object.__setattr__(self, 'value', self.value.strip())
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class SKU:
    """
    Value Object for Stock Keeping Unit (SKU).
    
    SKU must follow specific format and be unique within the system.
    """
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("SKU cannot be empty")
        
        # SKU format: 3-8 characters, alphanumeric, uppercase
        sku_pattern = r'^[A-Z0-9]{3,8}$'
        if not re.match(sku_pattern, self.value.strip().upper()):
            raise ValueError(
                "SKU must be 3-8 characters, alphanumeric, uppercase. "
                "Format: ABC123 or ABC12345"
            )
        
        # Normalize to uppercase
        object.__setattr__(self, 'value', self.value.strip().upper())
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Barcode:
    """
    Value Object for product barcode.
    
    Supports common barcode formats (UPC, EAN, etc.)
    """
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Barcode cannot be empty")
        
        # Remove any non-digit characters
        digits_only = re.sub(r'[^0-9]', '', self.value.strip())
        
        if len(digits_only) not in [8, 12, 13, 14]:  # Common barcode lengths
            raise ValueError(
                "Barcode must be 8, 12, 13, or 14 digits long"
            )
        
        object.__setattr__(self, 'value', digits_only)
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Weight:
    """
    Value Object for product weight.
    """
    value: Decimal
    unit: str = "kg"
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Weight cannot be negative")
        
        if self.unit not in ["kg", "g", "lb", "oz"]:
            raise ValueError("Weight unit must be kg, g, lb, or oz")
    
    def __str__(self) -> str:
        return f"{self.value} {self.unit}"


@dataclass(frozen=True)
class Dimensions:
    """
    Value Object for product dimensions.
    """
    length: Decimal
    width: Decimal
    height: Decimal
    unit: str = "cm"
    
    def __post_init__(self):
        if any(dim < 0 for dim in [self.length, self.width, self.height]):
            raise ValueError("Dimensions cannot be negative")
        
        if self.unit not in ["cm", "m", "in", "ft"]:
            raise ValueError("Dimension unit must be cm, m, in, or ft")
    
    @property
    def volume(self) -> Decimal:
        """Calculate volume"""
        return self.length * self.width * self.height
    
    def __str__(self) -> str:
        return f"{self.length}x{self.width}x{self.height} {self.unit}"


@dataclass(frozen=True)
class ProductTag:
    """
    Value Object for product tags.
    """
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Product tag cannot be empty")
        
        if len(self.value.strip()) < 2:
            raise ValueError("Product tag must be at least 2 characters")
        
        if len(self.value) > 50:
            raise ValueError("Product tag cannot exceed 50 characters")
        
        # Normalize: lowercase, no special characters except hyphens
        normalized = re.sub(r'[^a-zA-Z0-9\s-]', '', self.value.strip().lower())
        normalized = re.sub(r'\s+', '-', normalized)  # Replace spaces with hyphens
        
        object.__setattr__(self, 'value', normalized)
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ProductFilters:
    """
    Value Object for product search and filtering criteria.
    """
    category: str = None
    min_price: Decimal = None
    max_price: Decimal = None
    search_term: str = None
    tags: List[str] = None
    status: str = None
    in_stock_only: bool = False
    
    def __post_init__(self):
        if self.min_price is not None and self.min_price < 0:
            raise ValueError("Minimum price cannot be negative")
        
        if self.max_price is not None and self.max_price < 0:
            raise ValueError("Maximum price cannot be negative")
        
        if (self.min_price is not None and self.max_price is not None and 
            self.min_price > self.max_price):
            raise ValueError("Minimum price cannot be greater than maximum price")
        
        if self.search_term and len(self.search_term.strip()) < 2:
            raise ValueError("Search term must be at least 2 characters")
        
        if self.tags:
            # Validate and normalize tags
            normalized_tags = []
            for tag in self.tags:
                if tag and tag.strip():
                    try:
                        normalized_tag = ProductTag(tag.strip())
                        normalized_tags.append(str(normalized_tag))
                    except ValueError:
                        continue  # Skip invalid tags
            object.__setattr__(self, 'tags', normalized_tags)


@dataclass(frozen=True)
class PaginationParams:
    """
    Value Object for pagination parameters.
    """
    page: int = 1
    limit: int = 20
    
    def __post_init__(self):
        if self.page < 1:
            raise ValueError("Page must be greater than 0")
        
        if self.limit < 1 or self.limit > 100:
            raise ValueError("Limit must be between 1 and 100")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.limit
    
    def __str__(self) -> str:
        return f"Page {self.page}, Limit {self.limit}"
