from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    status = Column(String(50), default='Новый', index=True, nullable=False)
    # Статусы: 'Новый', 'Подтверждён', 'Собирается', 'Отправлен', 'Доставлен', 'Отменён'
    
    total_amount = Column(Float, nullable=False)
    subtotal_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    delivery_fee = Column(Float, default=0.0, nullable=False)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    delivery_method = Column(String(100), nullable=False) # 'Курьер до двери', 'СДЭК / ПВЗ', 'Почта России', 'Самовывоз'
    payment_method = Column(String(100), nullable=False)  # 'Картой онлайн', 'СБП', 'При получении', 'Долями'
    payment_status = Column(String(50), default='Ожидает оплаты', nullable=False)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    variant_id = Column(Integer, ForeignKey('product_variants.id', ondelete='SET NULL'), nullable=True)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=True)
    size = Column(String(20), nullable=True)
    color = Column(String(50), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    image_url = Column(String(500), nullable=True)

    order = relationship('Order', back_populates='items')
