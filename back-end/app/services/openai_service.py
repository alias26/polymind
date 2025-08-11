import openai
from typing import Optional, List, Dict, AsyncGenerator
from .ai_service import AIService, AIResponse

class OpenAIService(AIService):
    def __init__(self):
        pass  # API 키는 런타임에 제공받음
    
    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AIResponse:
        # API 키는 사용자가 반드시 제공해야 함
        if not api_key:
            raise Exception("OpenAI API key must be provided by user")
        
        
        try:
            client = openai.AsyncOpenAI(api_key=api_key)
            
            # 모델명 매핑 (프론트엔드에서 특정 버전 사용)
            model_mapping = {
                # 레거시 별칭들만 매핑 (프론트엔드에서 특정 버전 직접 사용)
                "GPT-4.1": "gpt-4.1",
                "GPT-4.1-mini": "gpt-4.1-mini",
                "GPT-4.1-nano": "gpt-4.1-nano",
                "GPT-4o": "gpt-4o",
                "GPT-4o-mini": "gpt-4o-mini",
                "GPT-4": "gpt-4o",
                "gpt4": "gpt-4o",
                "GPT-3.5": "gpt-3.5-turbo",
                "gpt3.5": "gpt-3.5-turbo"
            }
            
            # 모델명 매핑
            if model in model_mapping:
                actual_model = model_mapping[model]
                model = actual_model
            
            # 메시지 구성 (대화 컨텍스트 및 이미지 지원)
            if messages:
                chat_messages = messages.copy()
            else:
                chat_messages = [{"role": "user", "content": prompt}]
            
            # 이미지가 있는 경우 마지막 사용자 메시지에 이미지 추가
            if images and len(images) > 0:
                # 비전 모델로 자동 변경 (gpt-4-vision-preview 또는 gpt-4o)
                if model in ["gpt-3.5-turbo", "gpt-4"]:
                    model = "gpt-4o"  # 최신 비전 모델 사용
                
                # 마지막 사용자 메시지 찾기
                last_user_message = None
                for i in range(len(chat_messages) - 1, -1, -1):
                    if chat_messages[i]["role"] == "user":
                        last_user_message = chat_messages[i]
                        break
                
                if last_user_message:
                    # content를 배열 형태로 변환
                    if isinstance(last_user_message["content"], str):
                        content_parts = [{"type": "text", "text": last_user_message["content"]}]
                    else:
                        content_parts = last_user_message["content"] if isinstance(last_user_message["content"], list) else []
                    
                    # 이미지들을 content에 추가
                    for img in images:
                        content_parts.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{img['content_type']};base64,{img['data']}"
                            }
                        })
                    
                    last_user_message["content"] = content_parts
            
            # 시스템 프롬프트가 있는 경우 메시지 맨 앞에 추가
            if system_prompt:
                # 이미 시스템 메시지가 있는지 확인
                has_system = any(msg.get("role") == "system" for msg in chat_messages)
                if not has_system:
                    chat_messages.insert(0, {"role": "system", "content": system_prompt})
            
            # kwargs에서 OpenAI API에서 지원하지 않는 파라미터 제거
            api_kwargs = {k: v for k, v in kwargs.items() if k not in ['system_prompt']}
            
            # GPT-5 및 o1 모델들은 max_completion_tokens 사용
            if model.startswith(('gpt-5', 'o1')):
                # GPT-5/o1 모델은 temperature를 기본값(1)만 지원
                response = await client.chat.completions.create(
                    model=model,
                    messages=chat_messages,
                    max_completion_tokens=max_tokens,
                    **api_kwargs
                )
            else:
                response = await client.chat.completions.create(
                    model=model,
                    messages=chat_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **api_kwargs
                )
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider="openai",
                model=model,
                tokens_used=response.usage.total_tokens if response.usage else None
            )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        return "openai"
    
    def is_available(self, api_key: Optional[str] = None) -> bool:
        if not api_key:
            return False
        
        # OpenAI API 키 형식 검증 (sk-로 시작하고 적절한 길이)
        if not api_key.startswith('sk-'):
            return False
        
        if len(api_key) < 40:  # OpenAI API 키는 보통 50자 이상
            return False
        
        return True
    
    async def generate_text_stream(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        images: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncGenerator[AIResponse, None]:
        """OpenAI API 스트리밍"""
        if not api_key:
            raise Exception("OpenAI API key must be provided by user")
        
        try:
            client = openai.AsyncOpenAI(api_key=api_key)
            
            # 모델명 매핑
            model_mapping = {
                "GPT-4.1": "gpt-4.1",
                "GPT-4.1-mini": "gpt-4.1-mini",
                "GPT-4.1-nano": "gpt-4.1-nano",
                "GPT-4o": "gpt-4o",
                "GPT-4o-mini": "gpt-4o-mini",
                "GPT-4": "gpt-4o",
                "gpt4": "gpt-4o",
                "GPT-3.5": "gpt-3.5-turbo",
                "gpt3.5": "gpt-3.5-turbo"
            }
            
            if model in model_mapping:
                actual_model = model_mapping[model]
                model = actual_model
            
            # 메시지 구성
            if messages:
                chat_messages = messages.copy()
            else:
                chat_messages = [{"role": "user", "content": prompt}]
            
            # 이미지가 있는 경우 마지막 사용자 메시지에 이미지 추가
            if images and len(images) > 0:
                if model in ["gpt-3.5-turbo", "gpt-4"]:
                    model = "gpt-4o"  # 최신 비전 모델 사용
                
                last_user_message = None
                for i in range(len(chat_messages) - 1, -1, -1):
                    if chat_messages[i]["role"] == "user":
                        last_user_message = chat_messages[i]
                        break
                
                if last_user_message:
                    if isinstance(last_user_message["content"], str):
                        content_parts = [{"type": "text", "text": last_user_message["content"]}]
                    else:
                        content_parts = last_user_message["content"] if isinstance(last_user_message["content"], list) else []
                    
                    for img in images:
                        content_parts.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{img['content_type']};base64,{img['data']}"
                            }
                        })
                    
                    last_user_message["content"] = content_parts
            
            # 시스템 프롬프트가 있는 경우 메시지 맨 앞에 추가
            if system_prompt:
                has_system = any(msg.get("role") == "system" for msg in chat_messages)
                if not has_system:
                    chat_messages.insert(0, {"role": "system", "content": system_prompt})
            
            # kwargs에서 OpenAI API에서 지원하지 않는 파라미터 제거
            api_kwargs = {k: v for k, v in kwargs.items() if k not in ['system_prompt']}
            
            # GPT-5 및 o1 모델들은 max_completion_tokens 사용
            if model.startswith(('gpt-5', 'o1')):
                # GPT-5/o1 모델은 temperature를 기본값(1)만 지원
                # 스트리밍 요청
                stream = await client.chat.completions.create(
                    model=model,
                    messages=chat_messages,
                    max_completion_tokens=max_tokens,
                    stream=True,
                    **api_kwargs
                )
            else:
                # 스트리밍 요청
                stream = await client.chat.completions.create(
                    model=model,
                    messages=chat_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=True,
                    **api_kwargs
                )
            
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield AIResponse(
                            content=delta.content,
                            provider="openai",
                            model=model,
                            tokens_used=None  # 스트리밍 중에는 토큰 수 미제공
                        )
            
        except Exception as e:
            raise Exception(f"OpenAI streaming API error: {str(e)}")