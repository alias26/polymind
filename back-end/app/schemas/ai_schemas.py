from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any

class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., description="텍스트 생성을 위한 프롬프트")
    provider: Literal["openai", "anthropic", "google", "all"] = Field(
        default="openai",
        description="AI 서비스 제공자"
    )
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    model: Optional[str] = Field(default=None, description="사용할 모델 (선택사항)", example=None)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ImageData(BaseModel):
    filename: str = Field(..., description="원본 파일명")
    content_type: str = Field(..., description="파일 MIME 타입")
    data: str = Field(..., description="Base64로 인코딩된 이미지 데이터", min_length=1)
    size: int = Field(default=0, description="파일 크기 (bytes)")

class ChatGenerationRequest(BaseModel):
    message: str = Field(..., description="사용자 메시지")
    images: Optional[List[ImageData]] = Field(default=None, description="첨부된 이미지들")
    provider: Literal["openai", "anthropic", "google"] = Field(
        default="openai",
        description="AI 서비스 제공자"
    )
    model: Optional[str] = Field(default=None, description="사용할 모델")
    max_tokens: Optional[int] = Field(default=None, description="최대 토큰 수")
    temperature: Optional[float] = Field(default=None, description="Temperature 값")
    system_prompt: Optional[str] = Field(default=None, description="시스템 프롬프트")
    include_history: bool = Field(default=True, description="이전 대화 내역 포함 여부")

class TextGenerationResponse(BaseModel):
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None

class MultiTextGenerationResponse(BaseModel):
    responses: List[TextGenerationResponse]
    total_tokens: int
    total_cost: Optional[float] = None

class ProviderStatusResponse(BaseModel):
    available_providers: List[str]
    total_providers: int