from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryResponse

router = APIRouter(prefix='/api/categories', tags=['Categories'])

@router.get('', response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order.asc()).all()
    
    # Calculate product count per category
    counts = db.query(Product.category_id, func.count(Product.id)).filter(Product.is_active == True).group_by(Product.category_id).all()
    count_map = {cat_id: c for cat_id, c in counts}

    results = []
    for cat in categories:
        c_dict = {
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'description': cat.description,
            'image_url': cat.image_url,
            'sort_order': cat.sort_order,
            'is_active': cat.is_active,
            'created_at': cat.created_at,
            'products_count': count_map.get(cat.id, 0)
        }
        results.append(CategoryResponse(**c_dict))
    return results

@router.get('/{slug}', response_model=CategoryResponse)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.slug == slug, Category.is_active == True).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')
    
    count = db.query(Product).filter(Product.category_id == cat.id, Product.is_active == True).count()
    return CategoryResponse(
        id=cat.id,
        name=cat.name,
        slug=cat.slug,
        description=cat.description,
        image_url=cat.image_url,
        sort_order=cat.sort_order,
        is_active=cat.is_active,
        created_at=cat.created_at,
        products_count=count
    )
