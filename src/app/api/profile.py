from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.address import Address
from app.core.deps import get_current_user
from app.core.security import verify_password, hash_password
from app.schemas.user import UserResponse, UserUpdate, PasswordChange
from app.schemas.order import OrderResponse, OrderItemResponse
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse

router = APIRouter(prefix='/api/profile', tags=['Profile'])

@router.get('', response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put('', response_model=UserResponse)
def update_profile(
    update_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if update_in.full_name is not None:
        current_user.full_name = update_in.full_name.strip()
    if update_in.phone is not None:
        current_user.phone = update_in.phone.strip()
    if update_in.email is not None and update_in.email.lower() != current_user.email:
        exist = db.query(User).filter(User.email == update_in.email.lower(), User.id != current_user.id).first()
        if exist:
            raise HTTPException(status_code=400, detail='Этот email уже занят')
        current_user.email = update_in.email.lower()
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post('/password')
def change_password(
    pass_in: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(pass_in.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail='Текущий пароль указан неверно')
    
    current_user.password_hash = hash_password(pass_in.new_password)
    db.commit()
    return {'message': 'Пароль успешно обновлен'}

@router.get('/orders', response_model=List[OrderResponse])
def get_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    results = []
    for o in orders:
        results.append(OrderResponse(
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
    return results

@router.get('/addresses', response_model=List[AddressResponse])
def get_addresses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Address).filter(Address.user_id == current_user.id).order_by(Address.is_default.desc(), Address.created_at.desc()).all()

@router.post('/addresses', response_model=AddressResponse)
def add_address(
    addr_in: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if addr_in.is_default:
        db.query(Address).filter(Address.user_id == current_user.id).update({'is_default': False})
    
    addr = Address(
        user_id=current_user.id,
        title=addr_in.title,
        city=addr_in.city.strip(),
        address=addr_in.address.strip(),
        postal_code=addr_in.postal_code,
        is_default=addr_in.is_default
    )
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr

@router.put('/addresses/{address_id}', response_model=AddressResponse)
def update_address(
    address_id: int,
    addr_in: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    addr = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if not addr:
        raise HTTPException(status_code=404, detail='Адрес не найден')
    
    if addr_in.is_default:
        db.query(Address).filter(Address.user_id == current_user.id).update({'is_default': False})
        addr.is_default = True

    if addr_in.title:
        addr.title = addr_in.title
    if addr_in.city:
        addr.city = addr_in.city.strip()
    if addr_in.address:
        addr.address = addr_in.address.strip()
    if addr_in.postal_code is not None:
        addr.postal_code = addr_in.postal_code

    db.commit()
    db.refresh(addr)
    return addr

@router.delete('/addresses/{address_id}')
def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    addr = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if addr:
        db.delete(addr)
        db.commit()
    return {'message': 'Адрес удален'}
