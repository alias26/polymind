from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, AsyncGenerator
from pydantic import BaseModel

class AIResponse(BaseModel):
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None

class AIService(ABC):
    """AI 서비스 추상화 인터페이스"""
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        **kwargs
    ) -> AIResponse:
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        pass
    
    @abstractmethod
    def is_available(self, api_key: Optional[str] = None) -> bool:
        pass
    
    async def generate_text_stream(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncGenerator[AIResponse, None]:
        """스트리밍 방식으로 텍스트 생성 (기본 구현: 일반 generate_text 사용)"""
        # 기본적으로 일반 generate_text를 사용하고 한 번에 반환
        # 각 서비스에서 실제 스트리밍을 구현하려면 이 메소드를 오버라이드
        response = await self.generate_text(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=api_key,
            messages=messages,
            **kwargs
        )
        yield response