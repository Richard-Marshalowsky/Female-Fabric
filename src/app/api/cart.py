from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariant
from app.models.user import User
from app.core.deps import get_current_user_optional
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartItemResponse, CartResponse, CartSyncRequest

router = APIRouter(prefix='/api/cart', tags=['Cart'])

def get_or_create_cart(db: Session, user: Optional[User], session_id: Optional[str] = None) -> Cart:
    if user:
        cart = db.query(Cart).filter(Cart.user_id == user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart
    else:
        # Create anonymous cart
        cart = Cart()
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

def build_cart_response(cart: Cart, db: Session) -> CartResponse:
    if not cart or not cart.items:
        return CartResponse(
            id=cart.id if cart else None,
            items=[],
            total_quantity=0,
            subtotal=0.0,
            discount=0.0,
            delivery_fee=0.0,
            free_delivery_threshold=settings.FREE_SHIPPING_THRESHOLD,
            amount_left_for_free_delivery=settings.FREE_SHIPPING_THRESHOLD,
            total=0.0
        )

    items_resp = []
    total_qty = 0
    subtotal = 0.0
    discount = 0.0

    for item in cart.items:
        prod = db.query(Product).filter(Product.id == item.product_id).first()
        if not prod:
            continue
        
        # Stock checking
        stock = 10
        if item.variant_id:
            v = db.query(ProductVariant).filter(ProductVariant.id == item.variant_id).first()
            if v:
                stock = v.stock
        elif item.size or item.color:
            v = db.query(ProductVariant).filter(
                ProductVariant.product_id == item.product_id,
                ProductVariant.size == item.size if item.size else True,
                ProductVariant.color == item.color if item.color else True
            ).first()
            if v:
                stock = v.stock

        item_total = item.price * item.quantity
        subtotal += item_total
        if prod.old_price and prod.old_price > item.price:
            discount += (prod.old_price - item.price) * item.quantity

        img_url = prod.images[0].image_url if prod.images else None

        # Gather available sizes & colors for easy switching
        avail_sizes = [v.size for v in prod.variants if v.size]
        avail_colors = [{'name': v.color, 'code': v.color_code or '#000'} for v in prod.variants if v.color]

        items_resp.append(CartItemResponse(
            id=item.id,
            cart_id=cart.id,
            product_id=prod.id,
            variant_id=item.variant_id,
            product_name=prod.name,
            product_slug=prod.slug,
            image_url=img_url,
            size=item.size,
            color=item.color,
            available_sizes=list(set(avail_sizes)),
            available_colors=avail_colors,
            price=item.price,
            old_price=prod.old_price,
            quantity=item.quantity,
            total_price=item_total,
            stock_available=stock
        ))
        total_qty += item.quantity

    delivery_fee = 0.0 if subtotal >= settings.FREE_SHIPPING_THRESHOLD else (settings.DEFAULT_SHIPPING_COST if subtotal > 0 else 0.0)
    amount_left = max(0.0, settings.FREE_SHIPPING_THRESHOLD - subtotal)
    total = subtotal + delivery_fee

    return CartResponse(
        id=cart.id,
        items=items_resp,
        total_quantity=total_qty,
        subtotal=subtotal,
        discount=discount,
        delivery_fee=delivery_fee,
        free_delivery_threshold=settings.FREE_SHIPPING_THRESHOLD,
        amount_left_for_free_delivery=amount_left,
        total=total
    )

@router.get('', response_model=CartResponse)
def get_cart(
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(db, current_user, x_session_id)
    return build_cart_response(cart, db)

@router.post('/items', response_model=CartResponse)
def add_to_cart(
    item_in: CartItemAdd,
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(db, current_user, x_session_id)
    product = db.query(Product).filter(Product.id == item_in.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail='Товар не найден')

    variant = None
    if item_in.variant_id:
        variant = db.query(ProductVariant).filter(ProductVariant.id == item_in.variant_id).first()
    elif item_in.size or item_in.color:
        q = db.query(ProductVariant).filter(ProductVariant.product_id == product.id)
        if item_in.size:
            q = q.filter(ProductVariant.size == item_in.size)
        if item_in.color:
            q = q.filter(ProductVariant.color == item_in.color)
        variant = q.first()

    selected_size = item_in.size or (variant.size if variant else None)
    selected_color = item_in.color or (variant.color if variant else None)
    item_price = (variant.price_override if variant and variant.price_override else product.price)

    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product.id,
        CartItem.size == selected_size,
        CartItem.color == selected_color
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            variant_id=variant.id if variant else None,
            size=selected_size,
            color=selected_color,
            quantity=item_in.quantity,
            price=item_price
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return build_cart_response(cart, db)

@router.patch('/items/{item_id}', response_model=CartResponse)
def update_cart_item(
    item_id: int,
    update_in: CartItemUpdate,
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(db, current_user, x_session_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Позиция в корзине не найдена')

    if update_in.quantity is not None:
        if update_in.quantity <= 0:
            db.delete(item)
        else:
            item.quantity = update_in.quantity

    if update_in.size:
        item.size = update_in.size
    if update_in.color:
        item.color = update_in.color

    db.commit()
    db.refresh(cart)
    return build_cart_response(cart, db)

@router.delete('/items/{item_id}', response_model=CartResponse)
def remove_from_cart(
    item_id: int,
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(db, current_user, x_session_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if item:
        db.delete(item)
        db.commit()
        db.refresh(cart)
    return build_cart_response(cart, db)

@router.delete('', response_model=CartResponse)
def clear_cart(
    x_session_id: Optional[str] = Header(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(db, current_user, x_session_id)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(cart)
    return build_cart_response(cart, db)

@router.post('/sync', response_model=CartResponse)
def sync_cart(
    sync_data: CartSyncRequest,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if not current_user:
        return CartResponse()
    
    cart = get_or_create_cart(db, current_user)
    for s_item in sync_data.items:
        prod = db.query(Product).filter(Product.id == s_item.product_id, Product.is_active == True).first()
        if not prod:
            continue
        
        exist = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == prod.id,
            CartItem.size == s_item.size,
            CartItem.color == s_item.color
        ).first()

        if exist:
            exist.quantity += s_item.quantity
        else:
            db.add(CartItem(
                cart_id=cart.id,
                product_id=prod.id,
                variant_id=s_item.variant_id,
                size=s_item.size,
                color=s_item.color,
                quantity=s_item.quantity,
                price=prod.price
            ))
    db.commit()
    db.refresh(cart)
    return build_cart_response(cart, db)
