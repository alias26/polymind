from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.schemas.auth_schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    # 사용자 ID 중복 확인
    existing_user_by_id = get_user_by_id(db, user.id)
    if existing_user_by_id:
        raise ValueError("User ID already exists")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=user.id,  # 사용자가 입력한 ID 사용
        email=user.email,
        password=hashed_password,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, identifier: str, password: str):
    import re
    
    # 이메일 형식 정규식 검증
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # identifier가 이메일인지 ID인지 판단
    if re.match(email_pattern, identifier):
        # 이메일로 로그인
        user = get_user_by_email(db, identifier)
    else:
        # ID로 로그인 (이메일 형식이 아닌 경우)
        user = get_user_by_id(db, identifier)
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def update_user_last_login(db: Session, user_id: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.updated_at = func.now()
        db.commit()
        db.refresh(user)
    return user

def update_user_info(db: Session, user_id: str, user_update: UserUpdate):
    """사용자 정보 업데이트"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # 이메일 중복 확인 (다른 사용자가 이미 사용 중인지)
    if user_update.email and user_update.email != user.email:
        existing_user = get_user_by_email(db, user_update.email)
        if existing_user:
            raise ValueError("Email already exists")
    
    # 업데이트할 필드들 적용
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.name is not None:
        user.name = user_update.name
    
    user.updated_at = func.now()
    db.commit()
    db.refresh(user)
    return user

def change_user_password(db: Session, user_id: str, current_password: str, new_password: str, is_reset: bool = False):
    """사용자 비밀번호 변경"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    # 비밀번호 재설정이 아닌 경우에만 현재 비밀번호 확인
    if not is_reset:
        if not verify_password(current_password, user.password):
            return False
    
    # 새 비밀번호가 현재 비밀번호와 같은지 확인
    if verify_password(new_password, user.password):
        raise ValueError('새 비밀번호는 현재 비밀번호와 달라야 합니다.')
    
    # 새 비밀번호로 업데이트
    user.password = get_password_hash(new_password)
    user.updated_at = func.now()
    db.commit()
    db.refresh(user)
    return True