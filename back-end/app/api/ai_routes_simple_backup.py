from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.core.rate_limiter import limiter, RateLimits

router = APIRouter(prefix="/api/v1/ai", tags=["AI Services"])

@router.get("/providers")
async def get_available_providers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용 가능한 AI 서비스 제공자 목록"""
    # 임시로 빈 목록 반환 (추후 구현)
    return {
        "available_providers": [],
        "total_providers": 0
    }

@router.get("/health")
async def health_check():
    """AI 서비스 상태 체크"""
    return {
        "status": "healthy",
        "message": "AI services are operational"
    }