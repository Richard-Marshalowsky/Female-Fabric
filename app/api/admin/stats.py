from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.order import Order
from app.models.user import User
from app.models.product import Product, ProductVariant
from app.core.deps import require_admin
from app.schemas.order import AdminStatsResponse, OrderResponse, OrderItemResponse

router = APIRouter(prefix='/api/admin/stats', tags=['Admin Stats'])

@router.get('', response_model=AdminStatsResponse)
def get_admin_stats(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    total_rev = db.query(func.sum(Order.total_amount)).filter(Order.status != 'Отменён').scalar() or 0.0
    total_orders = db.query(Order).count()
    new_orders = db.query(Order).filter(Order.status == 'Новый').count()
    total_customers = db.query(User).filter(User.role == 'user').count()
    total_products = db.query(Product).count()

    low_stock = db.query(ProductVariant).filter(ProductVariant.stock < 5).count()

    status_counts = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    status_dict = {'Новый': 0, 'Подтверждён': 0, 'Собирается': 0, 'Отправлен': 0, 'Доставлен': 0, 'Отменён': 0}
    for st, cnt in status_counts:
        status_dict[st] = cnt

    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    recent_resp = []
    for o in recent_orders:
        recent_resp.append(OrderResponse(
            id=o.id,
            order_number=o.order_number,
            user_id=o.user_id,
            status=o.status,
            total_amount=o.total_amount,
            subtotal_amount=o.subtotal_amount,
            discount_amount=o.discount_amount,
            delivery_fee=o.delivery_fee,
            first_name=o.first_name,
            last_name=o.last_name,
            phone=o.phone,
            email=o.email,
            city=o.city,
            address=o.address,
            delivery_method=o.delivery_method,
            payment_method=o.payment_method,
            payment_status=o.payment_status,
            notes=o.notes,
            created_at=o.created_at,
            updated_at=o.updated_at,
            items=[
                OrderItemResponse(
                    id=it.id,
                    product_id=it.product_id,
                    variant_id=it.variant_id,
                    product_name=it.product_name,
                    sku=it.sku,
                    size=it.size,
                    color=it.color,
                    price=it.price,
                    quantity=it.quantity,
                    image_url=it.image_url,
                    total_price=it.price * it.quantity
                ) for it in o.items
            ]
        ))

    daily_sales = []
    now = datetime.now(timezone.utc)
    for i in range(6, -1, -1):
        day_date = (now - timedelta(days=i)).date()
        day_sales = db.query(func.sum(Order.total_amount)).filter(
            func.date(Order.created_at) == day_date,
            Order.status != 'Отменён'
        ).scalar() or 0.0
        daily_sales.append({
            'date': day_date.strftime('%d.%m'),
            'amount': float(day_sales)
        })

    return AdminStatsResponse(
        total_revenue=float(total_rev),
        total_orders=total_orders,
        new_orders=new_orders,
        total_customers=total_customers,
        total_products=total_products,
        low_stock_products=low_stock,
        recent_orders=recent_resp,
        orders_by_status=status_dict,
        daily_sales=daily_sales
    )
