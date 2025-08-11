from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token_jti = Column(String, unique=True, index=True, nullable=False)  # JWT ID (jti)
    user_id = Column(String, nullable=False)  # 사용자 ID는 문자열
    blacklisted_on = Column(DateTime, default=datetime.utcnow)
    token_type = Column(String, nullable=False)  # 'access' or 'refresh'