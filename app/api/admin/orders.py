from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.order import Order
from app.models.user import User
from app.core.deps import require_admin
from app.schemas.order import OrderResponse, OrderItemResponse, OrderStatusUpdate

router = APIRouter(prefix='/api/admin/orders', tags=['Admin Orders'])

@router.get('')
def get_admin_orders(
    status_filter: Optional[str] = None,
    q: Optional[str] = None,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    if q:
        search_pattern = f'%{q.strip()}%'
        query = query.filter(
            or_(
                Order.order_number.ilike(search_pattern),
                Order.first_name.ilike(search_pattern),
                Order.last_name.ilike(search_pattern),
                Order.phone.ilike(search_pattern),
                Order.email.ilike(search_pattern)
            )
        )

    orders = query.order_by(Order.created_at.desc()).all()
    results = []
    for o in orders:
        results.append({
            'id': o.id,
            'order_number': o.order_number,
            'user_id': o.user_id,
            'status': o.status,
            'total_amount': o.total_amount,
            'subtotal_amount': o.subtotal_amount,
            'discount_amount': o.discount_amount,
            'delivery_fee': o.delivery_fee,
            'first_name': o.first_name,
            'last_name': o.last_name,
            'phone': o.phone,
            'email': o.email,
            'city': o.city,
            'address': o.address,
            'delivery_method': o.delivery_method,
            'payment_method': o.payment_method,
            'payment_status': o.payment_status,
            'notes': o.notes,
            'created_at': o.created_at,
            'updated_at': o.updated_at,
            'items_count': sum(it.quantity for it in o.items),
            'items': [
                {
                    'id': it.id,
                    'product_id': it.product_id,
                    'product_name': it.product_name,
                    'sku': it.sku,
                    'size': it.size,
                    'color': it.color,
                    'price': it.price,
                    'quantity': it.quantity,
                    'image_url': it.image_url,
                    'total_price': it.price * it.quantity
                } for it in o.items
            ]
        })
    return results

@router.get('/{order_id}')
def get_order_detail(
    order_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail='Заказ не найден')
    
    return {
        'id': o.id,
        'order_number': o.order_number,
        'user_id': o.user_id,
        'status': o.status,
        'total_amount': o.total_amount,
        'subtotal_amount': o.subtotal_amount,
        'discount_amount': o.discount_amount,
        'delivery_fee': o.delivery_fee,
        'first_name': o.first_name,
        'last_name': o.last_name,
        'phone': o.phone,
        'email': o.email,
        'city': o.city,
        'address': o.address,
        'delivery_method': o.delivery_method,
        'payment_method': o.payment_method,
        'payment_status': o.payment_status,
        'notes': o.notes,
        'created_at': o.created_at,
        'updated_at': o.updated_at,
        'items': [
            {
                'id': it.id,
                'product_id': it.product_id,
                'product_name': it.product_name,
                'sku': it.sku,
                'size': it.size,
                'color': it.color,
                'price': it.price,
                'quantity': it.quantity,
                'image_url': it.image_url,
                'total_price': it.price * it.quantity
            } for it in o.items
        ]
    }

@router.patch('/{order_id}/status')
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Заказ не найден')

    valid_statuses = ['Новый', 'Подтверждён', 'Собирается', 'Отправлен', 'Доставлен', 'Отменён']
    if status_in.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f'Недопустимый статус. Разрешены: {", ".join(valid_statuses)}')

    order.status = status_in.status
    if status_in.status == 'Доставлен':
        order.payment_status = 'Оплачен'
    elif status_in.status == 'Отменён':
        order.payment_status = 'Отменён'

    db.commit()
    db.refresh(order)
    return {'id': order.id, 'status': order.status, 'message': f'Статус заказа изменен на "{order.status}"'}
