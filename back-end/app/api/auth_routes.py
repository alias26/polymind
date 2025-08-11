from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import create_access_token, create_refresh_token, get_current_user, blacklist_token
from app.crud.user_crud import create_user, authenticate_user, get_user_by_email
from app.schemas.auth_schemas import (
    UserCreate, UserLogin, UserResponse, Token, UserUpdate, PasswordChange,
    EmailVerificationRequest, EmailVerificationVerify, PasswordResetRequest, 
    PasswordResetVerify, FindUserIdRequest, FindUserIdResponse
)
from pydantic import BaseModel
from app.models.user import User
from app.core.rate_limiter import limiter, RateLimits

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

class PasswordVerify(BaseModel):
    current_password: str

@router.post("/register", response_model=UserResponse)
@limiter.limit(RateLimits.AUTH_REGISTER)
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # 사용자 생성
    try:
        db_user = create_user(db=db, user=user)
        return db_user
    except ValueError as e:
        if "User ID already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User ID already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
@limiter.limit(RateLimits.AUTH_LOGIN)
def login(request: Request, user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.identifier, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect ID/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30분
    }

@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    로그아웃 - 현재 액세스 토큰을 블랙리스트에 추가
    """
    access_token = credentials.credentials
    
    # 토큰을 블랙리스트에 추가
    if blacklist_token(access_token, current_user.id, "access", db):
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to logout"
        )

@router.get("/user", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    from app.core.auth import verify_token
    
    token_data = verify_token(refresh_token, db)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # 기존 리프레시 토큰을 블랙리스트에 추가 (보안 강화)
    blacklist_token(refresh_token, token_data.user_id, "refresh", db)
    
    access_token = create_access_token(data={"sub": str(token_data.user_id)})
    new_refresh_token = create_refresh_token(data={"sub": str(token_data.user_id)})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }

@router.put("/user", response_model=UserResponse)
def update_user_info(
    user_update: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 정보 업데이트"""
    from app.crud.user_crud import update_user_info
    
    try:
        updated_user = update_user_info(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/change-password")
@limiter.limit(RateLimits.AUTH_PASSWORD_CHANGE)
def change_password(
    request: Request,
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """비밀번호 변경"""
    from app.crud.user_crud import change_user_password
    
    try:
        success = change_user_password(
            db, 
            current_user.id, 
            password_change.current_password, 
            password_change.new_password
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/verify-password")
def verify_current_password(
    password_verify: PasswordVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 비밀번호 검증"""
    from app.crud.user_crud import verify_password
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # 현재 비밀번호가 맞는지 검증
    if not pwd_context.verify(password_verify.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    return {"message": "Password is correct"}

# ==============================================================================
# 이메일 인증 및 비밀번호 찾기 관련 엔드포인트
# ==============================================================================

@router.post("/send-verification-email")
@limiter.limit("5/minute")  # 이메일 발송 제한
def send_verification_email(
    request: Request,
    email_request: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """이메일 인증 코드 발송"""
    from app.services.email_service import email_service
    
    # 해당 이메일로 등록된 사용자가 있는지 확인
    user = get_user_by_email(db, email_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록된 사용자를 찾을 수 없습니다."
        )
    
    # 이미 인증된 사용자인 경우
    if user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 이메일 인증이 완료된 사용자입니다."
        )
    
    # 인증 이메일 발송
    try:
        email_service.send_verification_email(db, user, "register")
        return {"message": "인증 코드가 이메일로 발송되었습니다. (개발 환경에서는 콘솔을 확인하세요)"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="이메일 발송 중 오류가 발생했습니다."
        )

@router.post("/verify-email")
@limiter.limit("10/minute")  # 인증 시도 제한
def verify_email(
    request: Request,
    verify_request: EmailVerificationVerify,
    db: Session = Depends(get_db)
):
    """이메일 인증 코드 검증"""
    from app.services.email_service import email_service
    
    user = email_service.verify_code(db, verify_request.email, verify_request.code, "register")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="유효하지 않거나 만료된 인증 코드입니다."
        )
    
    return {"message": "이메일 인증이 완료되었습니다."}

@router.post("/find-user-id", response_model=FindUserIdResponse)
@limiter.limit("3/minute")  # 아이디 찾기 제한
def find_user_id(
    request: Request,
    find_request: FindUserIdRequest,
    db: Session = Depends(get_db)
):
    """이메일로 사용자 ID 찾기"""
    users = db.query(User).filter(User.email == find_request.email).all()
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 이메일로 등록된 사용자를 찾을 수 없습니다."
        )
    
    found_ids = [user.id for user in users]
    
    # 개발 환경에서 콘솔에 출력
    print("\n" + "="*50)
    print("🔍 USER ID LOOKUP (개발 환경)")
    print("="*50)
    print(f"이메일: {find_request.email}")
    print(f"찾은 사용자 ID: {', '.join(found_ids)}")
    print("="*50 + "\n")
    
    return FindUserIdResponse(found_ids=found_ids)

@router.post("/request-password-reset")
@limiter.limit("3/minute")  # 비밀번호 재설정 요청 제한
def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """비밀번호 재설정 요청"""
    from app.services.email_service import email_service
    
    user = get_user_by_email(db, reset_request.email)
    if not user:
        # 보안을 위해 사용자가 없어도 성공 메시지 반환
        return {"message": "해당 이메일로 비밀번호 재설정 링크가 발송되었습니다. (개발 환경에서는 콘솔을 확인하세요)"}
    
    # 비밀번호 재설정 이메일 발송
    try:
        email_service.send_password_reset_email(db, user)
        return {"message": "해당 이메일로 비밀번호 재설정 링크가 발송되었습니다. (개발 환경에서는 콘솔을 확인하세요)"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="이메일 발송 중 오류가 발생했습니다."
        )

@router.post("/reset-password")
@limiter.limit("5/minute")  # 비밀번호 재설정 제한
def reset_password(
    request: Request,
    reset_verify: PasswordResetVerify,
    db: Session = Depends(get_db)
):
    """비밀번호 재설정 실행"""
    from app.services.email_service import email_service
    from app.crud.user_crud import change_user_password
    
    # 토큰 검증
    user = email_service.verify_reset_token(db, reset_verify.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="유효하지 않거나 만료된 재설정 토큰입니다."
        )
    
    # 비밀번호 변경
    try:
        success = change_user_password(db, user.id, None, reset_verify.new_password, is_reset=True)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호 변경 중 오류가 발생했습니다."
            )
        
        # 토큰 사용 처리
        email_service.use_reset_token(db, reset_verify.token)
        
        return {"message": "비밀번호가 성공적으로 변경되었습니다."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )