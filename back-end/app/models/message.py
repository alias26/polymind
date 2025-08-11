from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(10), nullable=False)
    content = Column(String, nullable=False)
    message_order = Column(Integer, nullable=False)
    
    # AI 메시지 전용 필드들
    api_provider = Column(String(20))
    model_name = Column(String(100))
    token_count = Column(Integer)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # 관계 설정
    chat = relationship("Chat", back_populates="messages")
    message_images = relationship("MessageImage", back_populates="message", cascade="all, delete-orphan")
    
    # 제약 조건
    __table_args__ = (
        CheckConstraint("sender IN ('user', 'ai')", name='check_sender'),
        UniqueConstraint('chat_id', 'message_order', name='uq_chat_message_order'),
    )