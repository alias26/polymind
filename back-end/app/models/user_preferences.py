from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    default_system_prompt = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 관계 설정
    user = relationship("User", back_populates="preferences")