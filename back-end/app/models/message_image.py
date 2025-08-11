from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class MessageImage(Base):
    __tablename__ = "message_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)  # 원본 파일명
    content_type = Column(String(100), nullable=False)  # MIME 타입 (image/jpeg, image/png 등)
    data = Column(Text, nullable=False)  # Base64로 인코딩된 이미지 데이터
    size = Column(Integer, nullable=False)  # 파일 크기 (bytes)
    order_index = Column(Integer, nullable=False, default=0)  # 이미지 순서
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # 관계 설정
    message = relationship("Message", back_populates="message_images")
    
    def __repr__(self):
        return f"<MessageImage(id={self.id}, message_id={self.message_id}, filename='{self.filename}')>"