from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CartItemAdd(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int = Field(default=1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    size: Optional[str] = None
    color: Optional[str] = None

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    variant_id: Optional[int] = None
    product_name: str
    product_slug: str
    image_url: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    available_sizes: List[str] = []
    available_colors: List[dict] = []
    price: float
    old_price: Optional[float] = None
    quantity: int
    total_price: float
    stock_available: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: Optional[int] = None
    items: List[CartItemResponse] = []
    total_quantity: int = 0
    subtotal: float = 0.0
    discount: float = 0.0
    delivery_fee: float = 0.0
    free_delivery_threshold: float = 5000.0
    amount_left_for_free_delivery: float = 0.0
    total: float = 0.0

class CartSyncItem(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int = 1

class CartSyncRequest(BaseModel):
    items: List[CartSyncItem]
