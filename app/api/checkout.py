import random
import string
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Request, Header, status
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariant
from app.models.user import User
from app.core.deps import get_current_user_optional
from app.core.rate_limiter import order_rate_limiter
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse

router = APIRouter(prefix='/api/checkout', tags=['Checkout'])

def generate_order_number() -> str:
    year = datetime.now().year
    random_digits = ''.join(random.choices(string.digits, k=4))
    return f'FF-{year}-{random_digits}'

@router.post('', response_model=OrderResponse)
def create_order(
    order_in: OrderCreate,
    request: Request,
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    order_rate_limiter.check(request)

    # 1. Determine order items: either from user/session Cart or explicitly passed items
    items_to_order = []
    
    if current_user:
        user_cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if user_cart and user_cart.items:
            items_to_order = user_cart.items
        elif x_session_id:
            sess_cart = db.query(Cart).filter(Cart.session_id == x_session_id).first()
            if sess_cart and sess_cart.items:
                items_to_order = sess_cart.items
    elif x_session_id:
        sess_cart = db.query(Cart).filter(Cart.session_id == x_session_id).first()
        if sess_cart and sess_cart.items:
            items_to_order = sess_cart.items

    # Fallback to direct items in payload if provided
    raw_payload_items = order_in.items or []

    if not items_to_order and not raw_payload_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ваша корзина пуста. Невозможно оформить заказ.'
        )

    # 2. Calculate totals and build order items
    subtotal = 0.0
    discount = 0.0
    order_items_objs = []

    if items_to_order:
        for citem in items_to_order:
            prod = db.query(Product).filter(Product.id == citem.product_id).first()
            if not prod:
                continue
            item_price = citem.price
            item_total = item_price * citem.quantity
            subtotal += item_total
            if prod.old_price and prod.old_price > item_price:
                discount += (prod.old_price - item_price) * citem.quantity

            img_url = prod.images[0].image_url if prod.images else None

            # Deduct stock if variant exists
            if citem.variant_id:
                var = db.query(ProductVariant).filter(ProductVariant.id == citem.variant_id).first()
                if var and var.stock >= citem.quantity:
                    var.stock -= citem.quantity
            
            order_items_objs.append(OrderItem(
                product_id=prod.id,
                variant_id=citem.variant_id,
                product_name=prod.name,
                sku=prod.sku,
                size=citem.size,
                color=citem.color,
                price=item_price,
                quantity=citem.quantity,
                image_url=img_url
            ))
    else:
        for ritem in raw_payload_items:
            prod_id = ritem.get('product_id')
            qty = int(ritem.get('quantity', 1))
            prod = db.query(Product).filter(Product.id == prod_id).first()
            if not prod:
                continue
            item_price = float(ritem.get('price', prod.price))
            subtotal += item_price * qty
            if prod.old_price and prod.old_price > item_price:
                discount += (prod.old_price - item_price) * qty
            
            img_url = prod.images[0].image_url if prod.images else None
            order_items_objs.append(OrderItem(
                product_id=prod.id,
                variant_id=ritem.get('variant_id'),
                product_name=prod.name,
                sku=prod.sku,
                size=ritem.get('size'),
                color=ritem.get('color'),
                price=item_price,
                quantity=qty,
                image_url=img_url
            ))

    if not order_items_objs:
        raise HTTPException(status_code=400, detail='Не удалось обработать товары заказа')

    delivery_fee = 0.0 if subtotal >= settings.FREE_SHIPPING_THRESHOLD else settings.DEFAULT_SHIPPING_COST
    if order_in.delivery_method == 'Самовывоз':
        delivery_fee = 0.0

    total_amount = subtotal + delivery_fee
    order_num = generate_order_number()

    # Ensure unique order number
    while db.query(Order).filter(Order.order_number == order_num).first():
        order_num = generate_order_number()

    order = Order(
        order_number=order_num,
        user_id=current_user.id if current_user else None,
        status='Новый',
        total_amount=total_amount,
        subtotal_amount=subtotal,
        discount_amount=discount,
        delivery_fee=delivery_fee,
        first_name=order_in.first_name.strip(),
        last_name=order_in.last_name.strip(),
        phone=order_in.phone.strip(),
        email=order_in.email.lower().strip(),
        city=order_in.city.strip(),
        address=order_in.address.strip(),
        delivery_method=order_in.delivery_method,
        payment_method=order_in.payment_method,
        payment_status='Ожидает оплаты',
        notes=order_in.notes.strip() if order_in.notes else None
    )
    db.add(order)
    db.flush()

    for o_item in order_items_objs:
        o_item.order_id = order.id
        db.add(o_item)

    # Clear server cart
    if current_user:
        user_cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if user_cart:
            db.query(CartItem).filter(CartItem.cart_id == user_cart.id).delete()
    elif x_session_id:
        sess_cart = db.query(Cart).filter(Cart.session_id == x_session_id).first()
        if sess_cart:
            db.query(CartItem).filter(CartItem.cart_id == sess_cart.id).delete()

    db.commit()
    db.refresh(order)

    # Build response
    return OrderResponse(
        id=order.id,
        order_number=order.order_number,
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount,
        subtotal_amount=order.subtotal_amount,
        discount_amount=order.discount_amount,
        delivery_fee=order.delivery_fee,
        first_name=order.first_name,
        last_name=order.last_name,
        phone=order.phone,
        email=order.email,
        city=order.city,
        address=order.address,
        delivery_method=order.delivery_method,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
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
            ) for it in order.items
        ]
    )

@router.get('/orders/{order_number}', response_model=OrderResponse)
def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail='Заказ не найден')
    
    return OrderResponse(
        id=order.id,
        order_number=order.order_number,
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount,
        subtotal_amount=order.subtotal_amount,
        discount_amount=order.discount_amount,
        delivery_fee=order.delivery_fee,
        first_name=order.first_name,
        last_name=order.last_name,
        phone=order.phone,
        email=order.email,
        city=order.city,
        address=order.address,
        delivery_method=order.delivery_method,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
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
            ) for it in order.items
        ]
    )
