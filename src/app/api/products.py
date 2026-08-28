import json
import math
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc, func
from app.database import get_db
from app.models.product import Product, ProductImage, ProductVariant
from app.models.category import Category
from app.models.favorite import Favorite
from app.models.user import User
from app.core.deps import get_current_user_optional
from app.schemas.product import (
    ProductListItemResponse,
    ProductDetailResponse,
    ProductListPaginationResponse,
    ProductVariantResponse,
    ProductImageResponse
)

router = APIRouter(prefix='/api/products', tags=['Products'])

def build_product_list_item(product: Product, user_id: Optional[int] = None, db: Optional[Session] = None) -> ProductListItemResponse:
    primary_img = None
    all_imgs = []
    if product.images:
        for img in product.images:
            all_imgs.append(img.image_url)
            if img.is_primary and not primary_img:
                primary_img = img.image_url
        if not primary_img and all_imgs:
            primary_img = all_imgs[0]
    
    # Extract unique sizes and colors
    sizes_set = []
    colors_dict = {}
    total_stock = 0
    if product.variants:
        for v in product.variants:
            total_stock += v.stock
            if v.size and v.size not in sizes_set:
                sizes_set.append(v.size)
            if v.color and v.color not in colors_dict:
                colors_dict[v.color] = v.color_code or '#000000'
    
    colors_list = [{'name': name, 'code': code} for name, code in colors_dict.items()]

    discount_percent = None
    if product.old_price and product.old_price > product.price:
        discount_percent = int(round((product.old_price - product.price) / product.old_price * 100))

    is_fav = False
    if user_id and db:
        fav_exists = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.product_id == product.id).first()
        is_fav = fav_exists is not None

    return ProductListItemResponse(
        id=product.id,
        name=product.name,
        slug=product.slug,
        sku=product.sku,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None,
        category_slug=product.category.slug if product.category else None,
        price=product.price,
        old_price=product.old_price,
        discount_percent=discount_percent,
        is_active=product.is_active,
        is_featured=product.is_featured,
        is_new=product.is_new,
        primary_image=primary_img or 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80',
        images=all_imgs,
        sizes=sizes_set,
        colors=colors_list,
        total_stock=total_stock,
        in_stock=(total_stock > 0),
        is_favorite=is_fav
    )

@router.get('', response_model=ProductListPaginationResponse)
def get_products(
    category_slug: Optional[str] = None,
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sizes: Optional[str] = None,     # Comma-separated: 'S,M,L'
    colors: Optional[str] = None,   # Comma-separated
    in_stock: Optional[bool] = None,
    on_sale: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    is_new: Optional[bool] = None,
    sort_by: Optional[str] = 'newest', # 'newest', 'price_asc', 'price_desc', 'popular', 'discount'
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_active == True)

    if category_slug:
        cat = db.query(Category).filter(Category.slug == category_slug, Category.is_active == True).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)
        else:
            return ProductListPaginationResponse(
                items=[], total=0, page=page, limit=limit, pages=0,
                min_price=0, max_price=0, available_sizes=[], available_colors=[]
            )

    if q:
        search_pattern = f'%{q.strip()}%'
        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.sku.ilike(search_pattern)
            )
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if on_sale:
        query = query.filter(Product.old_price != None, Product.old_price > Product.price)

    if is_featured:
        query = query.filter(Product.is_featured == True)

    if is_new:
        query = query.filter(Product.is_new == True)

    # Variant filters (size, color, in_stock)
    variant_conditions = []
    if sizes:
        size_list = [s.strip() for s in sizes.split(',') if s.strip()]
        if size_list:
            variant_conditions.append(ProductVariant.size.in_(size_list))
    if colors:
        color_list = [c.strip() for c in colors.split(',') if c.strip()]
        if color_list:
            variant_conditions.append(ProductVariant.color.in_(color_list))
    if in_stock is True:
        variant_conditions.append(ProductVariant.stock > 0)

    if variant_conditions:
        query = query.join(Product.variants).filter(*variant_conditions).distinct()

    # Calculate aggregations from full matched products
    all_matched = query.all()
    total = len(all_matched)
    
    global_min_price = min([p.price for p in all_matched], default=0.0)
    global_max_price = max([p.price for p in all_matched], default=0.0)

    sizes_collected = []
    colors_collected = {}
    for p in all_matched:
        for v in p.variants:
            if v.size and v.size not in sizes_collected:
                sizes_collected.append(v.size)
            if v.color and v.color not in colors_collected:
                colors_collected[v.color] = v.color_code or '#000000'
    
    avail_colors = [{'name': name, 'code': code} for name, code in colors_collected.items()]

    # Sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'popular':
        query = query.order_by(Product.is_featured.desc(), Product.created_at.desc())
    elif sort_by == 'discount':
        query = query.order_by((Product.old_price - Product.price).desc().nullslast())
    else: # newest default
        query = query.order_by(Product.is_new.desc(), Product.created_at.desc())

    # Pagination
    offset = (page - 1) * limit
    paged_products = query.offset(offset).limit(limit).all()
    pages_count = math.ceil(total / limit) if total > 0 else 1

    user_id = current_user.id if current_user else None
    items = [build_product_list_item(p, user_id, db) for p in paged_products]

    return ProductListPaginationResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages_count,
        min_price=global_min_price,
        max_price=global_max_price,
        available_sizes=sizes_collected,
        available_colors=avail_colors
    )

@router.get('/featured/list', response_model=List[ProductListItemResponse])
def get_featured_products(
    limit: int = 8,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.is_active == True, Product.is_featured == True).limit(limit).all()
    user_id = current_user.id if current_user else None
    return [build_product_list_item(p, user_id, db) for p in products]

@router.get('/new/list', response_model=List[ProductListItemResponse])
def get_new_products(
    limit: int = 8,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.is_active == True, Product.is_new == True).order_by(Product.created_at.desc()).limit(limit).all()
    user_id = current_user.id if current_user else None
    return [build_product_list_item(p, user_id, db) for p in products]

@router.get('/{slug_or_id}', response_model=ProductDetailResponse)
def get_product_detail(
    slug_or_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if slug_or_id.isdigit():
        prod = db.query(Product).filter(Product.id == int(slug_or_id), Product.is_active == True).first()
    else:
        prod = db.query(Product).filter(Product.slug == slug_or_id, Product.is_active == True).first()

    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Товар не найден')

    user_id = current_user.id if current_user else None
    base_item = build_product_list_item(prod, user_id, db)

    # Parse details json
    details_dict = {}
    if prod.details_json:
        try:
            details_dict = json.loads(prod.details_json)
        except Exception:
            details_dict = {'description': prod.details_json}

    # Variants
    variants_resp = [ProductVariantResponse.model_validate(v) for v in prod.variants]
    images_resp = [ProductImageResponse.model_validate(img) for img in prod.images]

    # Related products from same category
    related = db.query(Product).filter(
        Product.category_id == prod.category_id,
        Product.id != prod.id,
        Product.is_active == True
    ).limit(4).all()
    related_resp = [build_product_list_item(r, user_id, db) for r in related]

    return ProductDetailResponse(
        **base_item.model_dump(),
        description=prod.description,
        details=details_dict,
        variants=variants_resp,
        image_objects=images_resp,
        related_products=related_resp
    )
