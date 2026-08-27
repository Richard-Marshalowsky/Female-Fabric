import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.core.deps import require_admin
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix='/api/admin/categories', tags=['Admin Categories'])

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text or 'category'

@router.get('')
def get_all_admin_categories(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.sort_order.asc(), Category.id.asc()).all()
    counts = db.query(Product.category_id, func.count(Product.id)).group_by(Product.category_id).all()
    count_map = {cat_id: c for cat_id, c in counts}

    results = []
    for cat in categories:
        results.append({
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'description': cat.description,
            'image_url': cat.image_url,
            'sort_order': cat.sort_order,
            'is_active': cat.is_active,
            'created_at': cat.created_at,
            'products_count': count_map.get(cat.id, 0)
        })
    return results

@router.post('', response_model=CategoryResponse)
def create_category(
    cat_in: CategoryCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    slug = cat_in.slug or slugify(cat_in.name)
    existing = db.query(Category).filter(Category.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail='Категория с таким slug уже существует')

    cat = Category(
        name=cat_in.name.strip(),
        slug=slug,
        description=cat_in.description,
        image_url=cat_in.image_url,
        sort_order=cat_in.sort_order,
        is_active=cat_in.is_active
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.put('/{category_id}', response_model=CategoryResponse)
def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail='Категория не найдена')

    if cat_in.name is not None:
        cat.name = cat_in.name.strip()
    if cat_in.slug is not None:
        cat.slug = cat_in.slug.strip()
    if cat_in.description is not None:
        cat.description = cat_in.description
    if cat_in.image_url is not None:
        cat.image_url = cat_in.image_url
    if cat_in.sort_order is not None:
        cat.sort_order = cat_in.sort_order
    if cat_in.is_active is not None:
        cat.is_active = cat_in.is_active

    db.commit()
    db.refresh(cat)
    return cat

@router.delete('/{category_id}')
def delete_category(
    category_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    
    prod_count = db.query(Product).filter(Product.category_id == cat.id).count()
    if prod_count > 0:
        raise HTTPException(status_code=400, detail=f'В категории есть {prod_count} товаров. Сначала удалите или переместите товары.')
    
    db.delete(cat)
    db.commit()
    return {'message': 'Категория удалена'}
