from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ❌ PROBLEMA: Solo Pydantic básico sin Domain Models
# ❌ PROBLEMA: No value objects
# ❌ PROBLEMA: No business logic en models
# ❌ PROBLEMA: No validation rules complejas

class Product(BaseModel):
    """
    Basic Product model - LEGACY VERSION with problems
    
    ❌ PROBLEMA: Float para dinero (precision issues)
    ❌ PROBLEMA: String simple para category (should be enum/foreign key)
    ❌ PROBLEMA: No business rules
    ❌ PROBLEMA: No value objects (Price, Stock, etc.)
    """
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)  # ❌ PROBLEMA: Float para dinero
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1)  # ❌ PROBLEMA: String en vez de enum
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = Field(default=True)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # ❌ PROBLEMA: No validation rules avanzadas
    # ❌ PROBLEMA: No business logic methods
    # ❌ PROBLEMA: No computed properties
    
    class Config:
        """Pydantic configuration"""
        # ❌ PROBLEMA: Configuración muy básica
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        
        schema_extra = {
            "example": {
                "name": "Smartphone XYZ Pro",
                "price": 899.99,
                "stock": 25,
                "category": "Electronics",
                "description": "Latest smartphone with AI features and advanced camera system"
            }
        }

# ❌ PROBLEMA: No otros models importantes:
# - Category model
# - ProductImage model  
# - ProductVariant model
# - Price history model
# - Stock movement model

# ❌ PROBLEMA: No request/response DTOs separados
class ProductCreateRequest(BaseModel):
    """Request model for creating products - BASIC VERSION"""
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)  # ❌ Float para dinero
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=1000)

class ProductUpdateRequest(BaseModel):
    """Request model for updating products - BASIC VERSION"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)  # ❌ Float para dinero
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None

# ❌ PROBLEMA: No response models específicos
# ❌ PROBLEMA: No pagination models
# ❌ PROBLEMA: No filter models estructurados
# ❌ PROBLEMA: No error models consistentes


