from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import Optional
import re

class UserCreate(BaseModel):
    id: str  # 사용자 입력 ID (예: nifol123)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('이름은 공백일 수 없습니다.')
        if len(v.strip()) < 1:
            raise ValueError('이름은 최소 1자 이상이어야 합니다.')
        if len(v.strip()) > 100:
            raise ValueError('이름은 최대 100자까지 가능합니다.')
        # 특수문자 제한 (한글, 영문, 공백만 허용)
        if not re.match(r'^[가-힣a-zA-Z\s]+$', v.strip()):
            raise ValueError('이름은 한글, 영문, 공백만 사용 가능합니다.')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('비밀번호는 최소 8자 이상이어야 합니다.')
        if len(v) > 128:
            raise ValueError('비밀번호는 최대 128자까지 가능합니다.')
        
        # 비밀번호 강도 검사
        if not re.search(r'[a-z]', v):
            raise ValueError('비밀번호에는 소문자가 포함되어야 합니다.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('비밀번호에는 대문자가 포함되어야 합니다.')
        if not re.search(r'\d', v):
            raise ValueError('비밀번호에는 숫자가 포함되어야 합니다.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('비밀번호에는 특수문자가 포함되어야 합니다.')
        
        return v

    @validator('id')
    def validate_user_id(cls, v):
        if len(v) < 3:
            raise ValueError('사용자 ID는 3자 이상이어야 합니다.')
        if len(v) > 50:
            raise ValueError('사용자 ID는 50자 이하여야 합니다.')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('사용자 ID는 영문, 숫자, 언더스코어(_)만 사용 가능합니다.')
        return v

class UserLogin(BaseModel):
    identifier: str  # ID 또는 이메일
    password: str

class UserResponse(BaseModel):
    id: str  # 사용자 입력 ID
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None  # 사용자 ID는 이제 문자열
    jti: Optional[str] = None  # JWT ID (블랙리스트용)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('이름은 공백일 수 없습니다.')
            if len(v.strip()) < 1:
                raise ValueError('이름은 최소 1자 이상이어야 합니다.')
            if len(v.strip()) > 100:
                raise ValueError('이름은 최대 100자까지 가능합니다.')
            # 특수문자 제한 (한글, 영문, 공백만 허용)
            if not re.match(r'^[가-힣a-zA-Z\s]+$', v.strip()):
                raise ValueError('이름은 한글, 영문, 공백만 사용 가능합니다.')
        return v.strip() if v else v

class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator('current_password')
    def validate_current_password(cls, v):
        if not v.strip():
            raise ValueError('현재 비밀번호를 입력해주세요.')
        return v

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('새 비밀번호는 최소 8자 이상이어야 합니다.')
        if len(v) > 128:
            raise ValueError('새 비밀번호는 최대 128자까지 가능합니다.')
        
        # 비밀번호 강도 검사
        if not re.search(r'[a-z]', v):
            raise ValueError('새 비밀번호에는 소문자가 포함되어야 합니다.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('새 비밀번호에는 대문자가 포함되어야 합니다.')
        if not re.search(r'\d', v):
            raise ValueError('새 비밀번호에는 숫자가 포함되어야 합니다.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('새 비밀번호에는 특수문자가 포함되어야 합니다.')
        
        return v

# 이메일 인증 관련 스키마
class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationVerify(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('인증 코드는 숫자만 입력해주세요.')
        if len(v) != 6:
            raise ValueError('인증 코드는 6자리 숫자입니다.')
        return v

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('새 비밀번호는 최소 8자 이상이어야 합니다.')
        if len(v) > 128:
            raise ValueError('새 비밀번호는 최대 128자까지 가능합니다.')
        
        # 비밀번호 강도 검사
        if not re.search(r'[a-z]', v):
            raise ValueError('새 비밀번호에는 소문자가 포함되어야 합니다.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('새 비밀번호에는 대문자가 포함되어야 합니다.')
        if not re.search(r'\d', v):
            raise ValueError('새 비밀번호에는 숫자가 포함되어야 합니다.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('새 비밀번호에는 특수문자가 포함되어야 합니다.')
        
        return v

class FindUserIdRequest(BaseModel):
    email: EmailStr

class FindUserIdResponse(BaseModel):
    found_ids: list[str]  # 해당 이메일로 등록된 사용자 ID 목록