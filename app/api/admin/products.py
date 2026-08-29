import json
import re
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.product import Product, ProductImage, ProductVariant
from app.models.category import Category
from app.models.user import User
from app.core.deps import require_admin
from app.schemas.product import ProductCreate, ProductUpdate

router = APIRouter(prefix='/api/admin/products', tags=['Admin Products'])

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text or 'product'

@router.get('')
def get_all_admin_products(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if q:
        search_term = f'%{q.strip()}%'
        query = query.filter(or_(Product.name.ilike(search_term), Product.sku.ilike(search_term)))
    if category_id:
        query = query.filter(Product.category_id == category_id)

    products = query.order_by(Product.id.desc()).all()
    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'sku': p.sku,
            'category_id': p.category_id,
            'category_name': p.category.name if p.category else 'Без категории',
            'price': p.price,
            'old_price': p.old_price,
            'is_active': p.is_active,
            'is_featured': p.is_featured,
            'is_new': p.is_new,
            'description': p.description,
            'details_json': p.details_json,
            'total_stock': sum(v.stock for v in p.variants),
            'primary_image': p.images[0].image_url if p.images else None,
            'images': [img.image_url for img in p.images],
            'variants': [{'id': v.id, 'size': v.size, 'color': v.color, 'color_code': v.color_code, 'stock': v.stock, 'sku': v.sku, 'price_override': v.price_override} for v in p.variants],
            'created_at': p.created_at
        })
    return results

@router.post('')
def create_product(
    prod_in: ProductCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == prod_in.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail='Категория не найдена')
    
    slug = prod_in.slug or slugify(prod_in.name)
    existing_slug = db.query(Product).filter(Product.slug == slug).first()
    if existing_slug:
        slug = f'{slug}-{db.query(Product).count() + 1}'

    existing_sku = db.query(Product).filter(Product.sku == prod_in.sku).first()
    if existing_sku:
        raise HTTPException(status_code=400, detail='Товар с таким артикулом (SKU) уже существует')

    prod = Product(
        name=prod_in.name.strip(),
        slug=slug,
        sku=prod_in.sku.strip(),
        category_id=prod_in.category_id,
        description=prod_in.description,
        details_json=prod_in.details_json,
        price=prod_in.price,
        old_price=prod_in.old_price,
        is_active=prod_in.is_active,
        is_featured=prod_in.is_featured,
        is_new=prod_in.is_new
    )
    db.add(prod)
    db.flush()

    if prod_in.images:
        for idx, img_url in enumerate(prod_in.images):
            db.add(ProductImage(
                product_id=prod.id,
                image_url=img_url.strip(),
                is_primary=(idx == 0),
                sort_order=idx
            ))

    if prod_in.variants:
        for idx, v in enumerate(prod_in.variants):
            var_sku = v.sku if v.sku else f"{prod.sku}-{v.size}-{v.color}"
            if db.query(ProductVariant).filter(ProductVariant.sku == var_sku).first():
                var_sku = f"{prod.sku}-{v.size}-{v.color}-{prod.id or idx}"
            db.add(ProductVariant(
                product_id=prod.id,
                size=v.size,
                color=v.color,
                color_code=v.color_code or '#000000',
                sku=var_sku,
                stock=v.stock,
                price_override=v.price_override
            ))
    else:
        db.add(ProductVariant(
            product_id=prod.id,
            size='One Size',
            color='Універсальний',
            color_code='#000000',
            sku=f'{prod.sku}-STD-{prod.id or 1}',
            stock=10
        ))

    db.commit()
    db.refresh(prod)
    return {'id': prod.id, 'message': 'Товар успішно створено', 'slug': prod.slug}

@router.put('/{product_id}')
def update_product(
    product_id: int,
    prod_in: ProductUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail='Товар не знайдено')

    if prod_in.name is not None:
        prod.name = prod_in.name.strip()
    if prod_in.slug is not None:
        prod.slug = prod_in.slug.strip()
    if prod_in.sku is not None:
        prod.sku = prod_in.sku.strip()
    if prod_in.category_id is not None:
        prod.category_id = prod_in.category_id
    if prod_in.description is not None:
        prod.description = prod_in.description
    if prod_in.details_json is not None:
        prod.details_json = prod_in.details_json
    if prod_in.price is not None:
        prod.price = prod_in.price
    if prod_in.old_price is not None:
        prod.old_price = prod_in.old_price
    if prod_in.is_active is not None:
        prod.is_active = prod_in.is_active
    if prod_in.is_featured is not None:
        prod.is_featured = prod_in.is_featured
    if prod_in.is_new is not None:
        prod.is_new = prod_in.is_new

    if prod_in.images is not None:
        db.query(ProductImage).filter(ProductImage.product_id == prod.id).delete()
        for idx, img_url in enumerate(prod_in.images):
            db.add(ProductImage(
                product_id=prod.id,
                image_url=img_url.strip(),
                is_primary=(idx == 0),
                sort_order=idx
            ))

    if prod_in.variants is not None:
        db.query(ProductVariant).filter(ProductVariant.product_id == prod.id).delete()
        for idx, v in enumerate(prod_in.variants):
            var_sku = v.sku if v.sku else f"{prod.sku}-{v.size}-{v.color}"
            if db.query(ProductVariant).filter(ProductVariant.sku == var_sku).first():
                var_sku = f"{prod.sku}-{v.size}-{v.color}-{prod.id}-{idx}"
            db.add(ProductVariant(
                product_id=prod.id,
                size=v.size,
                color=v.color,
                color_code=v.color_code or '#000000',
                sku=var_sku,
                stock=v.stock,
                price_override=v.price_override
            ))

    db.commit()
    db.refresh(prod)
    return {'id': prod.id, 'message': 'Товар успішно оновлено', 'slug': prod.slug}

@router.patch('/{product_id}/status')
def toggle_product_status(
    product_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail='Товар не найден')
    prod.is_active = not prod.is_active
    db.commit()
    return {'id': prod.id, 'is_active': prod.is_active, 'message': f'Статус товара изменен на {"Активен" if prod.is_active else "Скрыт"}'}

@router.delete('/{product_id}')
def delete_product(
    product_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail='Товар не найден')
    db.delete(prod)
    db.commit()
    return {'message': 'Товар успешно удален'}
