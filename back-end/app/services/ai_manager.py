from typing import Dict, List, Optional, AsyncGenerator
from .ai_service import AIService, AIResponse
from .openai_service import OpenAIService
from .anthropic_service import AnthropicService
from .gemini_service import GeminiService

class AIManager:
    def __init__(self):
        self.services: Dict[str, AIService] = {
            "openai": OpenAIService(),
            "anthropic": AnthropicService(),
            "google": GeminiService()
        }
    
    def get_service(self, provider: str) -> Optional[AIService]:
        """특정 AI 서비스 반환"""
        return self.services.get(provider)
    
    def get_available_services(self, user_api_keys: Optional[Dict[str, str]] = None) -> List[str]:
        """사용 가능한 AI 서비스 목록 반환 (사용자 API 키 고려)"""
        available = []
        for provider, service in self.services.items():
            api_key = user_api_keys.get(provider) if user_api_keys else None
            if service.is_available(api_key):
                available.append(provider)
        return available
    
    async def generate_text(
        self,
        prompt: str,
        provider: str = "openai",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AIResponse:
        """단일 AI 서비스로 텍스트 생성 (스트리밍 방식을 내부적으로 사용)"""
        # 스트리밍 메서드를 사용하여 전체 응답을 수집
        full_content = ""
        final_response = None
        
        async for chunk in self.generate_text_stream(
            prompt=prompt,
            provider=provider,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=api_key,
            messages=messages,
            images=images,
            **kwargs
        ):
            full_content += chunk.content
            final_response = chunk  # 마지막 청크의 메타데이터 사용
        
        # 최종 응답 생성
        if final_response:
            return AIResponse(
                content=full_content,
                provider=final_response.provider,
                model=final_response.model,
                tokens_used=final_response.tokens_used
            )
        else:
            raise ValueError(f"No response received from provider {provider}")
    
    async def generate_text_multi(
        self,
        prompt: str,
        providers: Optional[List[str]] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        user_api_keys: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> List[AIResponse]:
        """여러 AI 서비스로 동시 텍스트 생성 (사용자 API 키 지원)"""
        if providers is None:
            providers = self.get_available_services(user_api_keys)
        
        results = []
        for provider in providers:
            try:
                # 해당 프로바이더의 사용자 API 키 가져오기
                api_key = user_api_keys.get(provider) if user_api_keys else None
                
                response = await self.generate_text(
                    prompt=prompt,
                    provider=provider,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    api_key=api_key,  # 사용자 API 키 전달
                    **kwargs
                )
                results.append(response)
            except Exception as e:
                # 개별 서비스 실패 시 계속 진행
                continue
        
        return results
    
    async def generate_text_stream(
        self,
        prompt: str,
        provider: str = "openai",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncGenerator[AIResponse, None]:
        """스트리밍 방식으로 텍스트 생성"""
        service = self.get_service(provider)
        if not service:
            raise ValueError(f"Provider {provider} not found")
        
        if not service.is_available(api_key):
            raise ValueError(f"Provider {provider} is not available (API key missing)")
        
        async for chunk in service.generate_text_stream(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=api_key,
            messages=messages,
            images=images,
            **kwargs
        ):
            yield chunk

# 글로벌 AI 매니저 인스턴스
ai_manager = AIManager()