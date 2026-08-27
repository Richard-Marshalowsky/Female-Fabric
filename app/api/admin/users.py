from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.core.deps import require_admin

router = APIRouter(prefix='/api/admin/users', tags=['Admin Users'])

@router.get('')
def get_all_users(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    results = []
    for u in users:
        order_count = db.query(Order).filter(Order.user_id == u.id).count()
        total_spent = db.query(func.sum(Order.total_amount)).filter(Order.user_id == u.id, Order.status != 'Отменён').scalar() or 0.0
        results.append({
            'id': u.id,
            'email': u.email,
            'full_name': u.full_name,
            'phone': u.phone,
            'role': u.role,
            'is_active': u.is_active,
            'created_at': u.created_at,
            'orders_count': order_count,
            'total_spent': float(total_spent)
        })
    return results

@router.patch('/{user_id}/status')
def toggle_user_status(user_id: int, admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail='Нельзя заблокировать самого себя')
    
    user.is_active = not user.is_active
    db.commit()
    return {'id': user.id, 'is_active': user.is_active, 'message': f'Пользователь {"активирован" if user.is_active else "заблокирован"}'}

@router.patch('/{user_id}/role')
def change_user_role(user_id: int, role: str, admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if role not in ['user', 'admin']:
        raise HTTPException(status_code=400, detail='Недопустимая роль')
    
    user.role = role
    db.commit()
    return {'id': user.id, 'role': user.role, 'message': f'Роль изменена на {user.role}'}
