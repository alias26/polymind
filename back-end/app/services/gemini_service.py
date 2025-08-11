import google.generativeai as genai
from typing import Optional, List, Dict, AsyncGenerator
from .ai_service import AIService, AIResponse
from ..core.config import settings

class GeminiService(AIService):
    # 2025년 현재 지원되는 Gemini 모델 목록 (2.5 버전만)
    SUPPORTED_MODELS = {
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    }
    
    # 모델명 매핑 (프론트엔드에서 특정 버전 사용)
    MODEL_MAPPING = {
        # 레거시 별칭들만 매핑 (프론트엔드에서 특정 버전 직접 사용)
        "Gemini-2.5-Pro": "gemini-2.5-pro",
        "Gemini-2.5-Flash": "gemini-2.5-flash",
        "Pro": "gemini-2.5-pro",
        "Flash": "gemini-2.5-flash",
        "Gemini": "gemini-2.5-flash"
    }
    
    def __init__(self):
        pass  # API 키는 런타임에 제공받음
    
    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        images: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        # API 키는 사용자가 반드시 제공해야 함
        if not api_key:
            raise Exception("Google API key must be provided by user")
        
        # 모델명 검증 및 매핑
        if model in self.MODEL_MAPPING:
            # 사용자 친화적 모델명을 실제 API 모델명으로 매핑
            actual_model = self.MODEL_MAPPING[model]
            model = actual_model
        elif model not in self.SUPPORTED_MODELS:
            # 지원하지 않는 모델인 경우 기본값 사용
            model = "gemini-2.5-flash"
        
        try:
            # API 키 설정
            genai.configure(api_key=api_key)
            
            # 이미지가 있는 경우 Vision 모델로 처리
            if images and len(images) > 0:
                # Vision 모델 확인 및 설정 (2.5 버전들은 모두 Vision 지원)
                if model not in ["gemini-2.5-pro", "gemini-2.5-flash"]:
                    model = "gemini-2.5-flash"  # 기본 Vision 모델
                
                # 이미지 데이터 준비
                try:
                    import base64
                    import io
                    from PIL import Image
                    
                    content_parts = [prompt]  # 텍스트 프롬프트 먼저 추가
                    
                    for img in images:
                        try:
                            # Base64 디코딩
                            image_data = base64.b64decode(img["data"])
                            
                            # PIL Image로 변환
                            pil_image = Image.open(io.BytesIO(image_data))
                            
                            # 이미지가 너무 크면 리사이즈
                            if pil_image.size[0] > 4096 or pil_image.size[1] > 4096:
                                pil_image.thumbnail((4096, 4096), Image.Resampling.LANCZOS)
                            
                            # Gemini에 이미지 추가
                            content_parts.append(pil_image)
                            
                        except Exception as img_error:
                            continue
                    
                    if len(content_parts) == 1:  # 이미지가 하나도 처리되지 않은 경우
                        raise Exception("No images could be processed successfully")
                        
                except Exception as setup_error:
                    # 이미지 처리 실패 시 텍스트만으로 처리
                    return AIResponse(
                        content=f"이미지 처리 중 오류가 발생했습니다. 텍스트만 처리합니다: {prompt}",
                        provider="google",
                        model=model,
                        tokens_used=len(prompt.split()) * 2,
                        cost=0.0
                    )
                
                # Vision 모델 인스턴스 생성
                model_instance = genai.GenerativeModel(model)
                
                # 생성 설정
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                
                # 이미지와 함께 생성
                response = model_instance.generate_content(
                    content_parts,
                    generation_config=generation_config
                )
                
                return AIResponse(
                    content=response.text,
                    provider="google",
                    model=model,
                    tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                )
            
            # 이미지가 없는 경우 기존 텍스트 처리 로직 계속
            
            # 시스템 프롬프트 처리 (새 버전에서는 다른 방식 사용)
            if system_prompt:
                model_instance = genai.GenerativeModel(model)
                # 시스템 프롬프트는 대화 시작 시 추가
            else:
                model_instance = genai.GenerativeModel(model)
            
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            # 메시지 구성 (시스템 프롬프트 포함)
            if messages:
                # 대화 컨텍스트가 있는 경우
                chat = model_instance.start_chat()
                
                # 시스템 프롬프트가 있으면 첫 메시지에 포함
                user_message = messages[-1]["content"]
                if system_prompt:
                    user_message = f"{system_prompt}\\n\\n{user_message}"
                
                response = chat.send_message(
                    user_message,
                    generation_config=generation_config
                )
            else:
                # 단일 메시지 처리
                final_prompt = prompt
                if system_prompt:
                    final_prompt = f"{system_prompt}\\n\\n{prompt}"
                    
                response = model_instance.generate_content(
                    final_prompt,
                    generation_config=generation_config
                )
            
            # 안전 필터링 확인
            if not response.candidates:
                raise Exception("응답이 안전 필터에 의해 차단되었습니다. 다른 방식으로 질문을 재구성해주세요.")
            
            candidate = response.candidates[0]
            
            # finish_reason 확인
            if candidate.finish_reason == 2:  # SAFETY
                safety_ratings = getattr(candidate, 'safety_ratings', [])
                safety_info = []
                for rating in safety_ratings:
                    if hasattr(rating, 'category') and hasattr(rating, 'probability'):
                        safety_info.append(f"{rating.category}: {rating.probability}")
                
                safety_details = f" (안전 등급: {', '.join(safety_info)})" if safety_info else ""
                raise Exception(f"내용이 안전 가이드라인에 위배되어 응답이 차단되었습니다{safety_details}. 질문을 다르게 표현해주세요.")
            elif candidate.finish_reason == 3:  # RECITATION
                raise Exception("저작권 문제로 응답이 차단되었습니다. 다른 방식으로 질문해주세요.")
            elif candidate.finish_reason == 4:  # OTHER
                raise Exception("기타 이유로 응답이 차단되었습니다. 질문을 다시 시도해주세요.")
            
            # 응답 텍스트 확인
            if not hasattr(candidate, 'content') or not candidate.content.parts:
                raise Exception("유효한 응답을 받을 수 없습니다. 질문을 다시 작성해주세요.")
            
            # 응답 텍스트 추출
            try:
                response_text = response.text
            except Exception:
                # response.text가 실패하면 직접 파트에서 추출
                if candidate.content and candidate.content.parts:
                    response_text = "".join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                else:
                    raise Exception("응답 텍스트를 추출할 수 없습니다.")
            
            if not response_text or response_text.strip() == "":
                raise Exception("빈 응답을 받았습니다. 질문을 다시 시도해주세요.")
            
            return AIResponse(
                content=response_text,
                provider="google",
                model=model,
                tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
            )
        except Exception as e:
            error_msg = str(e)
            if "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                raise Exception(error_msg)  # 안전 관련 에러는 그대로 전달
            else:
                raise Exception(f"Gemini API 오류: {error_msg}")
    
    def get_provider_name(self) -> str:
        return "google"
    
    def is_available(self, api_key: Optional[str] = None) -> bool:
        if not api_key:
            return False
        
        # Google API 키 형식 검증 (AIza로 시작하고 적절한 길이)
        if not api_key.startswith('AIza'):
            return False
        
        if len(api_key) < 20:  # Google API 키 최소 길이 완화
            return False
        
        return True
    
    async def generate_text_stream(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        images: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[AIResponse, None]:
        """Gemini API 실제 스트리밍 구현"""
        # API 키는 사용자가 반드시 제공해야 함
        if not api_key:
            raise Exception("Google API key must be provided by user")
        
        # 모델명 검증 및 매핑
        if model in self.MODEL_MAPPING:
            actual_model = self.MODEL_MAPPING[model]
            model = actual_model
        elif model not in self.SUPPORTED_MODELS:
            model = "gemini-2.5-flash"
        
        try:
            # API 키 설정
            genai.configure(api_key=api_key)
            
            # 이미지가 있는 경우 Vision 모델로 처리
            if images and len(images) > 0:
                if model not in ["gemini-2.5-pro", "gemini-2.5-flash"]:
                    model = "gemini-2.5-flash"
                
                try:
                    import base64
                    import io
                    from PIL import Image
                    
                    content_parts = [prompt]
                    
                    for img in images:
                        try:
                            image_data = base64.b64decode(img["data"])
                            pil_image = Image.open(io.BytesIO(image_data))
                            
                            if pil_image.size[0] > 4096 or pil_image.size[1] > 4096:
                                pil_image.thumbnail((4096, 4096), Image.Resampling.LANCZOS)
                            
                            content_parts.append(pil_image)
                            
                        except Exception as img_error:
                            continue
                    
                    if len(content_parts) == 1:
                        raise Exception("No images could be processed successfully")
                        
                except Exception as setup_error:
                    # 이미지 처리 실패 시 에러 반환
                    yield AIResponse(
                        content=f"이미지 처리 중 오류가 발생했습니다: {str(setup_error)}",
                        provider="google",
                        model=model,
                        tokens_used=0
                    )
                    return
                
                # Vision 모델로 스트리밍 생성
                model_instance = genai.GenerativeModel(model)
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                
                
                # 스트리밍 생성
                try:
                    response = model_instance.generate_content(
                        content_parts,
                        generation_config=generation_config,
                        stream=True
                    )
                    
                    chunk_count = 0
                    for chunk in response:
                        # 안전성 확인
                        if hasattr(chunk, 'candidates') and chunk.candidates:
                            candidate = chunk.candidates[0]
                            if hasattr(candidate, 'finish_reason') and candidate.finish_reason:
                                if candidate.finish_reason == 2:  # SAFETY
                                    yield AIResponse(
                                        content="안전 가이드라인에 의해 응답이 차단되었습니다.",
                                        provider="google",
                                        model=model,
                                        tokens_used=0
                                    )
                                    return
                        
                        if chunk.text and len(chunk.text.strip()) > 0:
                            chunk_count += 1
                            yield AIResponse(
                                content=chunk.text,
                                provider="google",
                                model=model,
                                tokens_used=None
                            )
                    
                    
                except Exception as stream_error:
                    # 에러 시 일반 생성으로 폴백
                    try:
                        response = model_instance.generate_content(content_parts, generation_config=generation_config)
                        yield AIResponse(
                            content=response.text,
                            provider="google",
                            model=model,
                            tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                        )
                    except Exception as fallback_error:
                        yield AIResponse(
                            content=f"Gemini 이미지 분석 중 오류가 발생했습니다: {str(stream_error)}",
                            provider="google",
                            model=model,
                            tokens_used=0
                        )
                return
            
            # 텍스트 전용 스트리밍
            model_instance = genai.GenerativeModel(model)
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            # 메시지 구성
            if messages:
                # 대화 컨텍스트가 있는 경우
                chat = model_instance.start_chat()
                
                # 시스템 프롬프트가 있으면 첫 메시지에 포함
                user_message = messages[-1]["content"]
                if system_prompt:
                    user_message = f"{system_prompt}\n\n{user_message}"
                
                
                try:
                    response = chat.send_message(
                        user_message,
                        generation_config=generation_config,
                        stream=True
                    )
                    
                    chunk_count = 0
                    for chunk in response:
                        # 안전성 확인
                        if hasattr(chunk, 'candidates') and chunk.candidates:
                            candidate = chunk.candidates[0]
                            if hasattr(candidate, 'finish_reason') and candidate.finish_reason:
                                if candidate.finish_reason == 2:  # SAFETY
                                    yield AIResponse(
                                        content="안전 가이드라인에 의해 응답이 차단되었습니다.",
                                        provider="google",
                                        model=model,
                                        tokens_used=0
                                    )
                                    return
                        
                        if chunk.text and len(chunk.text.strip()) > 0:
                            chunk_count += 1
                            yield AIResponse(
                                content=chunk.text,
                                provider="google",
                                model=model,
                                tokens_used=None
                            )
                    
                    
                except Exception as stream_error:
                    # 에러 시 일반 생성으로 폴백
                    try:
                        response = chat.send_message(user_message, generation_config=generation_config)
                        yield AIResponse(
                            content=response.text,
                            provider="google",
                            model=model,
                            tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                        )
                    except Exception as fallback_error:
                        yield AIResponse(
                            content=f"Gemini 채팅 응답 생성 중 오류가 발생했습니다: {str(stream_error)}",
                            provider="google",
                            model=model,
                            tokens_used=0
                        )
            else:
                # 단일 메시지 처리
                final_prompt = prompt
                if system_prompt:
                    final_prompt = f"{system_prompt}\n\n{prompt}"
                
                
                try:
                    response = model_instance.generate_content(
                        final_prompt,
                        generation_config=generation_config,
                        stream=True
                    )
                    
                    chunk_count = 0
                    for chunk in response:
                        # 안전성 확인
                        if hasattr(chunk, 'candidates') and chunk.candidates:
                            candidate = chunk.candidates[0]
                            if hasattr(candidate, 'finish_reason') and candidate.finish_reason:
                                if candidate.finish_reason == 2:  # SAFETY
                                    yield AIResponse(
                                        content="안전 가이드라인에 의해 응답이 차단되었습니다.",
                                        provider="google",
                                        model=model,
                                        tokens_used=0
                                    )
                                    return
                        
                        if chunk.text and len(chunk.text.strip()) > 0:
                            chunk_count += 1
                            yield AIResponse(
                                content=chunk.text,
                                provider="google",
                                model=model,
                                tokens_used=None
                            )
                    
                    
                except Exception as stream_error:
                    # 에러 시 일반 생성으로 폴백
                    try:
                        response = model_instance.generate_content(final_prompt, generation_config=generation_config)
                        yield AIResponse(
                            content=response.text,
                            provider="google",
                            model=model,
                            tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                        )
                    except Exception as fallback_error:
                        yield AIResponse(
                            content=f"Gemini 응답 생성 중 오류가 발생했습니다: {str(stream_error)}",
                            provider="google",
                            model=model,
                            tokens_used=0
                        )
                    
        except Exception as e:
            error_msg = str(e)
            if "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                yield AIResponse(
                    content=f"안전 필터로 인해 응답이 차단되었습니다: {error_msg}",
                    provider="google",
                    model=model,
                    tokens_used=0
                )
            else:
                yield AIResponse(
                    content=f"Gemini 스트리밍 오류: {error_msg}",
                    provider="google",
                    model=model,
                    tokens_used=0
                )