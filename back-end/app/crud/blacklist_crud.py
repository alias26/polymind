from sqlalchemy.orm import Session
from app.models.blacklist_token import BlacklistToken
from datetime import datetime, timedelta

def add_token_to_blacklist(db: Session, token_jti: str, user_id: str, token_type: str):
    """
    토큰을 블랙리스트에 추가
    """
    blacklist_token = BlacklistToken(
        token_jti=token_jti,
        user_id=user_id,
        token_type=token_type
    )
    db.add(blacklist_token)
    db.commit()
    db.refresh(blacklist_token)
    return blacklist_token

def is_token_blacklisted(db: Session, token_jti: str) -> bool:
    """
    토큰이 블랙리스트에 있는지 확인
    """
    token = db.query(BlacklistToken).filter(BlacklistToken.token_jti == token_jti).first()
    return token is not None

def get_user_blacklisted_tokens(db: Session, user_id: str):
    """
    특정 사용자의 블랙리스트된 토큰 조회
    """
    return db.query(BlacklistToken).filter(BlacklistToken.user_id == user_id).all()

def cleanup_expired_tokens(db: Session, days_old: int = 7):
    """
    만료된 토큰들을 블랙리스트에서 제거 (정리 작업)
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    expired_tokens = db.query(BlacklistToken).filter(
        BlacklistToken.blacklisted_on < cutoff_date
    ).all()
    
    for token in expired_tokens:
        db.delete(token)
    
    db.commit()
    return len(expired_tokens)