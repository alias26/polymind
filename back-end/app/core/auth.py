from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user_crud import get_user_by_id
from app.crud.blacklist_crud import is_token_blacklisted, add_token_to_blacklist
from app.schemas.auth_schemas import TokenData
from app.core.config import settings

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    # JWT ID 추가 (블랙리스트용)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "jti": jti})
    
    encoded_jwt = jwt.encode(to_encode, settings.get_secret_key(), algorithm=settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    # JWT ID 추가 (블랙리스트용)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "jti": jti})
    
    encoded_jwt = jwt.encode(to_encode, settings.get_secret_key(), algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, db: Session = None):
    try:
        payload = jwt.decode(token, settings.get_secret_key(), algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        jti: str = payload.get("jti")
        
        if user_id is None or jti is None:
            return None
            
        # 블랙리스트 확인
        if db and is_token_blacklisted(db, jti):
            return None
            
        token_data = TokenData(user_id=user_id, jti=jti)
        return token_data
    except JWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, db)
    if token_data is None:
        raise credentials_exception
    
    user = get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    
    return user

def blacklist_token(token: str, user_id: str, token_type: str, db: Session):
    """
    토큰을 블랙리스트에 추가
    """
    try:
        payload = jwt.decode(token, settings.get_secret_key(), algorithms=[settings.algorithm])
        jti = payload.get("jti")
        
        if jti:
            add_token_to_blacklist(db, jti, user_id, token_type)
            return True
    except JWTError:
        pass
    return False