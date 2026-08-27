from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login', auto_error=False)

def get_token_from_request(request: Request, bearer_token: Optional[str] = Depends(oauth2_scheme)) -> Optional[str]:
    if bearer_token:
        return bearer_token
    # Also check cookies
    cookie_token = request.cookies.get('access_token')
    if cookie_token:
        if cookie_token.startswith('Bearer '):
            return cookie_token[7:]
        return cookie_token
    return None

def get_current_user_optional(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or 'sub' not in payload:
        return None
    user_id = payload.get('sub')
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        return None
    return user

def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional)
) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Требуется авторизация для выполнения действия',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user

def require_admin(
    user: User = Depends(get_current_user)
) -> User:
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступ запрещен. Требуются права администратора.',
        )
    return user
