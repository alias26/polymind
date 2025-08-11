from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.crud.user_preferences_crud import (
    get_user_preferences,
    update_user_preferences,
    delete_user_preferences
)
from app.schemas.user_preferences_schemas import (
    UserPreferencesUpdate,
    UserPreferencesResponse
)
from app.models.user import User

router = APIRouter(prefix="/api/v1/user/preferences", tags=["user-preferences"])

@router.get("/", response_model=UserPreferencesResponse)
def get_current_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자의 설정 조회"""
    preferences = get_user_preferences(db, current_user.id)
    if not preferences:
        # 설정이 없으면 기본값으로 생성
        from app.schemas.user_preferences_schemas import UserPreferencesCreate
        from app.crud.user_preferences_crud import create_user_preferences
        
        default_preferences = UserPreferencesCreate(
            default_system_prompt="당신은 도움이 되는 AI 어시스턴트입니다."
        )
        preferences = create_user_preferences(db, current_user.id, default_preferences)
    
    return preferences

@router.put("/", response_model=UserPreferencesResponse)
def update_current_user_preferences(
    preferences_data: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자의 설정 업데이트"""
    preferences = update_user_preferences(db, current_user.id, preferences_data)
    return preferences

@router.delete("/")
def delete_current_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자의 설정 삭제"""
    success = delete_user_preferences(db, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )
    return {"message": "User preferences deleted successfully"}