from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
from typing import List, Optional, Dict, Any
from decimal import Decimal

class MessageImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    content_type: str
    data: str
    size: int
    order_index: int

class ChatCreate(BaseModel):
    title: str
    system_prompt: Optional[str] = None
    model: str
    temperature: Optional[Decimal] = Decimal("0.7")
    max_tokens: Optional[int] = 2048

class ChatUpdate(BaseModel):
    title: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[Decimal] = None
    max_tokens: Optional[int] = None

class MessageCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    sender: str
    content: str
    api_provider: Optional[str] = None
    model_name: Optional[str] = None
    token_count: Optional[int] = None

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    
    id: int
    sender: str
    content: str
    message_order: int
    api_provider: Optional[str] = None
    model_name: Optional[str] = None
    token_count: Optional[int] = None
    message_images: List[MessageImageResponse] = []
    images: Optional[List[Dict[str, Any]]] = None  # 하위 호환성을 위한 변환된 이미지 데이터
    created_at: datetime

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    
    id: int
    title: str
    system_prompt: Optional[str] = None
    model: str
    temperature: Decimal
    max_tokens: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []