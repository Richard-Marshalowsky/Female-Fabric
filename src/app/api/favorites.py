from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.favorite import Favorite
from app.models.product import Product
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.product import ProductListItemResponse
from app.api.products import build_product_list_item

router = APIRouter(prefix='/api/favorites', tags=['Favorites'])

@router.get('', response_model=List[ProductListItemResponse])
def get_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favs = db.query(Favorite).filter(Favorite.user_id == current_user.id).order_by(Favorite.created_at.desc()).all()
    results = []
    for fav in favs:
        if fav.product and fav.product.is_active:
            results.append(build_product_list_item(fav.product, current_user.id, db))
    return results

@router.post('/{product_id}')
def toggle_favorite(product_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not prod:
        raise HTTPException(status_code=404, detail='Товар не найден')

    existing = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.product_id == product_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {'is_favorite': False, 'message': 'Товар удален из избранного'}
    else:
        new_fav = Favorite(user_id=current_user.id, product_id=product_id)
        db.add(new_fav)
        db.commit()
        return {'is_favorite': True, 'message': 'Товар добавлен в избранное'}
