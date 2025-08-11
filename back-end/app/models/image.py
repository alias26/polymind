from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)  # 원본 파일명
    content_type = Column(String(100), nullable=False)  # MIME 타입 (image/jpeg, image/png 등)
    file_size = Column(Integer, nullable=False)  # 파일 크기 (bytes)
    image_data = Column(Text, nullable=False)  # Base64로 인코딩된 이미지 데이터
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 업로드한 사용자
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="images")
    
    def __repr__(self):
        return f"<Image(id={self.id}, filename='{self.filename}', user_id={self.user_id})>"