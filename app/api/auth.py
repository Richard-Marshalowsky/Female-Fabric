from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.core.security import hash_password, verify_password, create_access_token, generate_random_token
from app.core.deps import get_current_user
from app.core.rate_limiter import auth_rate_limiter

router = APIRouter(prefix='/api/auth', tags=['Auth'])

@router.post('/register', response_model=Token)
def register(user_in: UserCreate, request: Request, response: Response, db: Session = Depends(get_db)):
    auth_rate_limiter.check(request)
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким email уже зарегистрирован'
        )
    
    user = User(
        email=user_in.email.lower(),
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name.strip(),
        phone=user_in.phone.strip() if user_in.phone else None,
        role='user',
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={'sub': str(user.id), 'role': user.role, 'email': user.email})
    response.set_cookie(
        key='access_token',
        value=f'Bearer {token}',
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite='lax'
    )
    return Token(access_token=token, token_type='bearer', user=UserResponse.model_validate(user))

@router.post('/login', response_model=Token)
def login(login_in: UserLogin, request: Request, response: Response, db: Session = Depends(get_db)):
    auth_rate_limiter.check(request)
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный email или пароль'
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Ваш аккаунт деактивирован'
        )

    token = create_access_token(data={'sub': str(user.id), 'role': user.role, 'email': user.email})
    response.set_cookie(
        key='access_token',
        value=f'Bearer {token}',
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite='lax'
    )
    return Token(access_token=token, token_type='bearer', user=UserResponse.model_validate(user))

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('access_token')
    return {'message': 'Успешный выход из системы'}

@router.get('/me', response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post('/forgot-password')
def forgot_password(req: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    auth_rate_limiter.check(request)
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user:
        # Generic message for security
        return {'message': 'Если аккаунт с указанным email существует, инструкции по сбросу пароля отправлены.'}
    
    reset_token = generate_random_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=2)
    db.commit()
    # In real world email is sent. For seamless testing, return token or confirmation
    return {
        'message': 'Инструкция по сбросу пароля отправлена на ваш email.',
        'reset_token': reset_token # Provided for easy testing in demonstration mode
    }

@router.post('/reset-password')
def reset_password(req: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    auth_rate_limiter.check(request)
    user = db.query(User).filter(User.reset_token == req.token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Недействительный или просроченный токен сброса пароля'
        )
    
    user.password_hash = hash_password(req.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    return {'message': 'Пароль успешно изменен. Теперь вы можете войти в аккаунт.'}
