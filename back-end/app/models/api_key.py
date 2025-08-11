from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    provider = Column(String(20), primary_key=True)
    encrypted_key = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 관계 설정
    user = relationship("User", back_populates="api_keys")
    
    # 제약 조건
    __table_args__ = (
        CheckConstraint("provider IN ('openai', 'anthropic', 'google')", name='check_provider'),
    )