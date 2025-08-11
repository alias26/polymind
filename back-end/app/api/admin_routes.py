from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.crud.blacklist_crud import get_user_blacklisted_tokens, cleanup_expired_tokens
from app.models.user import User
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

class BlacklistTokenResponse(BaseModel):
    id: int
    token_jti: str
    user_id: str
    blacklisted_on: datetime
    token_type: str
    
    class Config:
        from_attributes = True

class CleanupResult(BaseModel):
    deleted_count: int
    message: str

@router.get("/user/blacklisted-tokens", response_model=List[BlacklistTokenResponse])
def get_my_blacklisted_tokens(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    현재 사용자의 블랙리스트된 토큰 목록 조회
    """
    tokens = get_user_blacklisted_tokens(db, current_user.id)
    return tokens

@router.delete("/cleanup/expired-tokens")
def cleanup_expired_blacklist_tokens(
    days_old: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    만료된 블랙리스트 토큰 정리 (관리자 기능)
    기본적으로 7일 이상 된 토큰들을 삭제
    """
    deleted_count = cleanup_expired_tokens(db, days_old)
    
    return CleanupResult(
        deleted_count=deleted_count,
        message=f"Successfully cleaned up {deleted_count} expired tokens older than {days_old} days"
    )