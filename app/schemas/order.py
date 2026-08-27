from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int] = None
    variant_id: Optional[int] = None
    product_name: str
    sku: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    price: float
    quantity: int
    image_url: Optional[str] = None
    total_price: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=50)
    email: EmailStr
    city: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=500)
    delivery_method: str = Field(..., max_length=100)
    payment_method: str = Field(..., max_length=100)
    notes: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern=r'^(Новый|Подтверждён|Собирается|Отправлен|Доставлен|Отменён)$')

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: Optional[int] = None
    status: str
    total_amount: float
    subtotal_amount: float
    discount_amount: float
    delivery_fee: float
    first_name: str
    last_name: str
    phone: str
    email: str
    city: str
    address: str
    delivery_method: str
    payment_method: str
    payment_status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    limit: int
    pages: int

class AdminStatsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    new_orders: int
    total_customers: int
    total_products: int
    low_stock_products: int
    recent_orders: List[OrderResponse]
    orders_by_status: Dict[str, int]
    daily_sales: List[Dict[str, Any]]
