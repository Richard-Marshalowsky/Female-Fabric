from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool
    sort_order: int

    class Config:
        from_attributes = True

class ProductVariantBase(BaseModel):
    size: str
    color: str
    color_code: Optional[str] = '#000000'
    sku: str
    stock: int = Field(default=0, ge=0)
    price_override: Optional[float] = None

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    sku: str = Field(..., min_length=2, max_length=100)
    category_id: int
    description: Optional[str] = None
    details_json: Optional[str] = None
    price: float = Field(..., gt=0)
    old_price: Optional[float] = None
    is_active: bool = True
    is_featured: bool = False
    is_new: bool = False

class ProductCreate(ProductBase):
    images: Optional[List[str]] = [] # list of image URLs
    variants: Optional[List[ProductVariantCreate]] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    details_json: Optional[str] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_new: Optional[bool] = None
    images: Optional[List[str]] = None
    variants: Optional[List[ProductVariantCreate]] = None

class ProductListItemResponse(BaseModel):
    id: int
    name: str
    slug: str
    sku: str
    category_id: int
    category_name: Optional[str] = None
    category_slug: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    discount_percent: Optional[int] = None
    is_active: bool
    is_featured: bool
    is_new: bool
    primary_image: Optional[str] = None
    images: List[str] = []
    sizes: List[str] = []
    colors: List[Dict[str, str]] = [] # [{'name': 'Черный', 'code': '#000'}]
    total_stock: int = 0
    in_stock: bool = True
    is_favorite: Optional[bool] = False

    class Config:
        from_attributes = True

class ProductDetailResponse(ProductListItemResponse):
    description: Optional[str] = None
    details: Optional[Dict[str, Any]] = None # parsed details_json
    variants: List[ProductVariantResponse] = []
    image_objects: List[ProductImageResponse] = []
    related_products: List[ProductListItemResponse] = []

    class Config:
        from_attributes = True

class ProductListPaginationResponse(BaseModel):
    items: List[ProductListItemResponse]
    total: int
    page: int
    limit: int
    pages: int
    min_price: float
    max_price: float
    available_sizes: List[str]
    available_colors: List[Dict[str, str]]
