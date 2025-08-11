from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user_preferences import UserPreferences
from app.schemas.user_preferences_schemas import UserPreferencesCreate, UserPreferencesUpdate

def get_user_preferences(db: Session, user_id: str):
    """사용자 설정 조회"""
    return db.query(UserPreferences).filter(
        UserPreferences.user_id == user_id
    ).first()

def create_user_preferences(db: Session, user_id: str, preferences_data: UserPreferencesCreate):
    """사용자 설정 생성"""
    db_preferences = UserPreferences(
        user_id=user_id,
        default_system_prompt=preferences_data.default_system_prompt
    )
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def update_user_preferences(db: Session, user_id: str, preferences_data: UserPreferencesUpdate):
    """사용자 설정 업데이트"""
    preferences = get_user_preferences(db, user_id)
    
    if not preferences:
        # 설정이 없으면 새로 생성
        create_data = UserPreferencesCreate(
            default_system_prompt=preferences_data.default_system_prompt
        )
        return create_user_preferences(db, user_id, create_data)
    
    # 기존 설정 업데이트
    update_data = preferences_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)
    
    preferences.updated_at = func.now()
    db.commit()
    db.refresh(preferences)
    return preferences

def delete_user_preferences(db: Session, user_id: str):
    """사용자 설정 삭제"""
    preferences = get_user_preferences(db, user_id)
    if preferences:
        db.delete(preferences)
        db.commit()
        return True
    return False