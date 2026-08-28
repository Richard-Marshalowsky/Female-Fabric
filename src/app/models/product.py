from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    details_json = Column(Text, nullable=True)  # JSON string: composition, fit, season, care
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, index=True, nullable=False)
    is_featured = Column(Boolean, default=False, index=True, nullable=False)
    is_new = Column(Boolean, default=False, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = relationship('Category', back_populates='products')
    images = relationship('ProductImage', back_populates='product', cascade='all, delete-orphan', order_by='ProductImage.sort_order')
    variants = relationship('ProductVariant', back_populates='product', cascade='all, delete-orphan')
    favorites = relationship('Favorite', back_populates='product', cascade='all, delete-orphan')

class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    product = relationship('Product', back_populates='images')

class ProductVariant(Base):
    __tablename__ = 'product_variants'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    size = Column(String(20), nullable=False)       # XS, S, M, L, XL, etc.
    color = Column(String(50), nullable=False)     # Бежевый, Черный, etc.
    color_code = Column(String(20), nullable=True) # Hex: #F5F5DC
    sku = Column(String(100), unique=True, index=True, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    price_override = Column(Float, nullable=True)

    product = relationship('Product', back_populates='variants')
