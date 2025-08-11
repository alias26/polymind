from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.api_key import ApiKey
from app.schemas.api_key_schemas import ApiKeyCreate
from cryptography.fernet import Fernet
import os

# 암호화 키 생성 (환경변수에서 로드)
from app.core.config import settings

# 고정된 암호화 키 (개발용)
_FIXED_KEY = None

def get_cipher_suite():
    global _FIXED_KEY
    
    encryption_key = settings.encryption_key
    if not encryption_key:
        # 환경변수에 없으면 고정된 키 사용 (개발용)
        if _FIXED_KEY is None:
            # 개발용 고정 키 생성 (실제 배포 시에는 환경변수 사용 필수)
            import base64
            _FIXED_KEY = base64.urlsafe_b64encode(b'dev_key_32bytes_for_encryption_!')
        encryption_key = _FIXED_KEY
    elif isinstance(encryption_key, str):
        encryption_key = encryption_key.encode()
    
    return Fernet(encryption_key)

def encrypt_api_key(api_key: str) -> str:
    cipher_suite = get_cipher_suite()
    return cipher_suite.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    cipher_suite = get_cipher_suite()
    return cipher_suite.decrypt(encrypted_key.encode()).decode()

def get_api_key(db: Session, user_id: str, provider: str):
    return db.query(ApiKey).filter(
        ApiKey.user_id == user_id,
        ApiKey.provider == provider
    ).first()

def get_all_user_api_keys(db: Session, user_id: str):
    return db.query(ApiKey).filter(ApiKey.user_id == user_id).all()

def create_or_update_api_key(db: Session, user_id: str, api_key_data: ApiKeyCreate):
    encrypted_key = encrypt_api_key(api_key_data.apiKey)
    
    existing_key = get_api_key(db, user_id, api_key_data.provider)
    
    if existing_key:
        existing_key.encrypted_key = encrypted_key
        existing_key.updated_at = func.now()
        existing_key.is_active = True
        db.commit()
        db.refresh(existing_key)
        return existing_key
    else:
        db_api_key = ApiKey(
            user_id=user_id,
            provider=api_key_data.provider,
            encrypted_key=encrypted_key
        )
        db.add(db_api_key)
        db.commit()
        db.refresh(db_api_key)
        return db_api_key

def delete_api_key(db: Session, user_id: str, provider: str):
    api_key = get_api_key(db, user_id, provider)
    if api_key:
        db.delete(api_key)
        db.commit()
        return True
    return False

def delete_all_user_api_keys(db: Session, user_id: str):
    result = db.query(ApiKey).filter(ApiKey.user_id == user_id).delete()
    db.commit()
    return result