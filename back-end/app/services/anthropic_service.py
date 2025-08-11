import anthropic
from typing import Optional, List, Dict, AsyncGenerator
from .ai_service import AIService, AIResponse
from ..core.config import settings

class AnthropicService(AIService):
    def __init__(self):
        pass  # API 키는 런타임에 제공받음
    
    def get_provider_name(self) -> str:
        return "anthropic"
    
    def is_available(self, api_key: Optional[str] = None) -> bool:
        if not api_key:
            return False
        
        # Anthropic API 키 형식 검증
        if not api_key.startswith('sk-ant-'):
            return False
        
        if len(api_key) < 50:
            return False
        
        return True
    
    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AIResponse:
        # API 키는 사용자가 반드시 제공해야 함
        if not api_key:
            raise Exception("Anthropic API key must be provided by user")
        
        try:
            client = anthropic.AsyncAnthropic(api_key=api_key)
            
            # 메시지 구성
            if messages:
                chat_messages = messages.copy()
            else:
                chat_messages = [{"role": "user", "content": prompt}]
            
            # 모델명 매핑 (프론트엔드에서 특정 버전 사용)
            model_mapping = {
                # 레거시 별칭들만 매핑 (프론트엔드에서 특정 버전 직접 사용)
                "Opus4.1": "claude-opus-4-1-20250805",
                "Opus4": "claude-opus-4-20250514",
                "Sonnet4": "claude-sonnet-4-20250514",
                "Sonnet3.7": "claude-3-7-sonnet-20250219",
                "Sonnet3.5": "claude-3-5-sonnet-20241022",
                "Haiku3.5": "claude-3-5-haiku-20241022",
                "Haiku3": "claude-3-haiku-20240307",
                "Opus": "claude-opus-4-1-20250805",
                "Sonnet": "claude-sonnet-4-20250514",
                "Haiku": "claude-3-5-haiku-20241022"
            }
            
            # 모델명 매핑 및 검증
            if model in model_mapping:
                actual_model = model_mapping[model]
                model = actual_model
            elif model not in ['claude-opus-4-1-20250805', 'claude-opus-4-20250514', 'claude-sonnet-4-20250514', 
                              'claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-20241022', 
                              'claude-3-5-haiku-20241022', 'claude-3-haiku-20240307']:
                model = "claude-sonnet-4-20250514"
            
            # API 호출 파라미터 구성
            api_params = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": chat_messages,
                **kwargs
            }
            
            # 시스템 프롬프트가 있으면 추가
            if system_prompt:
                api_params["system"] = system_prompt
            
            message = await client.messages.create(**api_params)
            
            return AIResponse(
                content=message.content[0].text,
                provider="anthropic",
                model=model,
                tokens_used=message.usage.input_tokens + message.usage.output_tokens if message.usage else None
            )
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def generate_text_stream(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncGenerator[AIResponse, None]:
        """Anthropic API 스트리밍"""
        if not api_key:
            raise Exception("Anthropic API key must be provided by user")
        
        try:
            client = anthropic.AsyncAnthropic(api_key=api_key)
            
            # 메시지 구성
            if messages:
                chat_messages = []
                for i, msg in enumerate(messages):
                    # 마지막 사용자 메시지이면서 이미지가 있는 경우 특별 처리
                    if i == len(messages) - 1 and msg["role"] == "user" and images:
                        # 이미지가 있는 메시지는 content를 배열 형태로 구성
                        content_parts = []
                        
                        # 텍스트가 있으면 추가
                        if msg["content"] and msg["content"].strip():
                            content_parts.append({"type": "text", "text": msg["content"]})
                        
                        # 이미지들 추가
                        for img in images:
                            content_parts.append({
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": img.get("content_type", "image/jpeg"),
                                    "data": img["data"]
                                }
                            })
                        
                        # 텍스트가 없고 이미지만 있는 경우에도 허용 (Anthropic API 요구사항에 따라)
                        
                        chat_messages.append({
                            "role": msg["role"],
                            "content": content_parts
                        })
                    else:
                        # 일반 텍스트 메시지
                        if msg["content"] and msg["content"].strip():
                            chat_messages.append(msg)
            else:
                chat_messages = [{"role": "user", "content": prompt}]
            
            # 모델명 매핑
            model_mapping = {
                "Opus4.1": "claude-opus-4-1-20250805",
                "Opus4": "claude-opus-4-20250514",
                "Sonnet4": "claude-sonnet-4-20250514",
                "Sonnet3.7": "claude-3-7-sonnet-20250219",
                "Sonnet3.5": "claude-3-5-sonnet-20241022",
                "Haiku3.5": "claude-3-5-haiku-20241022",
                "Haiku3": "claude-3-haiku-20240307",
                "Opus": "claude-opus-4-1-20250805",
                "Sonnet": "claude-sonnet-4-20250514",
                "Haiku": "claude-3-5-haiku-20241022"
            }
            
            if model in model_mapping:
                actual_model = model_mapping[model]
                model = actual_model
            elif model not in ['claude-opus-4-1-20250805', 'claude-opus-4-20250514', 'claude-sonnet-4-20250514', 
                              'claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-20241022', 
                              'claude-3-5-haiku-20241022', 'claude-3-haiku-20240307']:
                model = "claude-sonnet-4-20250514"
            
            # API 호출 파라미터 구성 (stream 파라미터 제거)
            api_params = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": chat_messages,
                **kwargs
            }
            
            # 시스템 프롬프트가 있으면 추가
            if system_prompt:
                api_params["system"] = system_prompt
            
            async with client.messages.stream(**api_params) as stream:
                async for text in stream.text_stream:
                    yield AIResponse(
                        content=text,
                        provider="anthropic",
                        model=model,
                        tokens_used=None  # 스트리밍 중에는 토큰 수 미제공
                    )
            
        except Exception as e:
            raise Exception(f"Anthropic streaming API error: {str(e)}")