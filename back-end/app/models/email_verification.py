from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmailVerification(Base):
    """이메일 인증 코드 관리"""
    __tablename__ = "email_verifications"
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    email = Column(String(255), nullable=False)  # 인증할 이메일
    verification_code = Column(String(6), nullable=False)  # 6자리 인증 코드
    verification_type = Column(String(20), nullable=False)  # "register", "password_reset", "email_change"
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # 만료 시간 (5분)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # 관계 설정
    user = relationship("User", back_populates="email_verifications")

class PasswordResetToken(Base):
    """비밀번호 재설정 토큰 관리"""
    __tablename__ = "password_reset_tokens"
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    token = Column(String(100), nullable=False, unique=True)  # UUID 토큰
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # 만료 시간 (30분)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # 관계 설정
    user = relationship("User", back_populates="password_reset_tokens")