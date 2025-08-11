from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Request
from fastapi.responses import StreamingResponse
from typing import List, Optional, AsyncGenerator
import asyncio
import json
import base64
from sqlalchemy.orm import Session
from app.schemas.ai_schemas import (
    TextGenerationRequest,
    TextGenerationResponse,
    MultiTextGenerationResponse,
    ProviderStatusResponse,
    ChatGenerationRequest,
    ChatMessage
)
from app.services.ai_manager import ai_manager
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.core.rate_limiter import limiter, RateLimits
from app.models.chat import Chat
from app.models.message import Message
from app.models.message_image import MessageImage
from app.crud.api_key_crud import get_api_key, decrypt_api_key

router = APIRouter(prefix="/api/v1/ai", tags=["AI Services"])

@router.get("/providers", response_model=ProviderStatusResponse)
async def get_available_providers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용 가능한 AI 서비스 제공자 목록"""
    try:
        # 사용자의 API 키들을 가져와서 확인
        user_api_keys = {}
        
        # OpenAI API 키 확인
        openai_key = get_api_key(db, current_user.id, "openai")
        if openai_key:
            try:
                decrypted_key = decrypt_api_key(openai_key.encrypted_key)
                user_api_keys["openai"] = decrypted_key
            except Exception:
                pass  # 복호화 실패 시 해당 키는 사용 불가
        
        # Anthropic API 키 확인  
        anthropic_key = get_api_key(db, current_user.id, "anthropic")
        if anthropic_key:
            try:
                decrypted_key = decrypt_api_key(anthropic_key.encrypted_key)
                user_api_keys["anthropic"] = decrypted_key
            except Exception:
                pass
            
        # Google API 키 확인
        google_key = get_api_key(db, current_user.id, "google")
        if google_key:
            try:
                decrypted_key = decrypt_api_key(google_key.encrypted_key)
                user_api_keys["google"] = decrypted_key
            except Exception:
                pass
        
        # AI 매니저를 통해 사용 가능한 서비스 확인
        available_providers = ai_manager.get_available_services(user_api_keys)
        
        return ProviderStatusResponse(
            available_providers=available_providers,
            total_providers=len(available_providers)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get providers: {str(e)}")

@router.post("/generate", response_model=TextGenerationResponse)
@limiter.limit(RateLimits.AI_GENERATE)
async def generate_text(
    request: Request,
    generation_request: TextGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """단일 AI 서비스로 텍스트 생성"""
    try:
        # 사용자의 API 키를 가져와서 AI 매니저에 전달
        user_api_keys = {}
        
        # 요청된 제공자에 따라 API 키 가져오기
        provider_key = None
        if generation_request.provider == "openai":
            api_key_record = get_api_key(db, current_user.id, "openai")
            if api_key_record:
                provider_key = decrypt_api_key(api_key_record.encrypted_key)
                user_api_keys["openai"] = provider_key
        elif generation_request.provider == "anthropic":
            api_key_record = get_api_key(db, current_user.id, "anthropic")
            if api_key_record:
                provider_key = decrypt_api_key(api_key_record.encrypted_key)
                user_api_keys["anthropic"] = provider_key
        elif generation_request.provider == "google":
            api_key_record = get_api_key(db, current_user.id, "google")
            if api_key_record:
                provider_key = decrypt_api_key(api_key_record.encrypted_key)
                user_api_keys["google"] = provider_key
        
        if not provider_key:
            raise HTTPException(
                status_code=400,
                detail=f"No API key found for provider {generation_request.provider}"
            )
        
        # AI 매니저를 통해 텍스트 생성
        response = await ai_manager.generate_text(
            prompt=generation_request.prompt,
            provider=generation_request.provider,
            max_tokens=generation_request.max_tokens,
            temperature=generation_request.temperature,
            model=generation_request.model,
            api_key=provider_key,
            system_prompt=generation_request.system_prompt
        )
        
        return TextGenerationResponse(
            content=response.content,
            provider=response.provider,
            model=response.model,
            tokens_used=response.tokens_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")

@router.post("/generate-multi", response_model=MultiTextGenerationResponse)
@limiter.limit(RateLimits.AI_GENERATE_MULTI)
async def generate_text_multi(
    request: Request,
    generation_request: TextGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """여러 AI 서비스로 동시 텍스트 생성"""
    try:
        # 사용자의 API 키들을 가져와서 확인
        user_api_keys = {}
        
        # OpenAI API 키 확인
        openai_key = get_api_key(db, current_user.id, "openai")
        if openai_key:
            decrypted_key = decrypt_api_key(openai_key.encrypted_key)
            user_api_keys["openai"] = decrypted_key
        
        # Anthropic API 키 확인  
        anthropic_key = get_api_key(db, current_user.id, "anthropic")
        if anthropic_key:
            decrypted_key = decrypt_api_key(anthropic_key.encrypted_key)
            user_api_keys["anthropic"] = decrypted_key
            
        # Google API 키 확인
        google_key = get_api_key(db, current_user.id, "google")
        if google_key:
            decrypted_key = decrypt_api_key(google_key.encrypted_key)
            user_api_keys["google"] = decrypted_key
        
        if not user_api_keys:
            raise HTTPException(
                status_code=400,
                detail="No API keys found. Please add at least one AI service API key."
            )
        
        # AI 매니저를 통해 여러 서비스로 동시 생성
        responses = await ai_manager.generate_text_multi(
            prompt=generation_request.prompt,
            max_tokens=generation_request.max_tokens,
            temperature=generation_request.temperature,
            user_api_keys=user_api_keys,
            system_prompt=generation_request.system_prompt
        )
        
        return MultiTextGenerationResponse(responses=responses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-text generation failed: {str(e)}")

# 모든 채팅 요청은 이제 스트리밍 방식만 지원

@router.post("/chat/{chat_id}")
async def chat_response(
    request: Request,
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """실시간 스트리밍 채팅 응답 생성"""
    
    # 요청 본문을 미리 읽어서 파싱
    try:
        content_type = request.headers.get("content-type", "")
        
        if content_type.startswith("multipart/form-data"):
            # FormData로 온 경우 - 이미지가 포함된 요청
            form = await request.form()
            generation_request = ChatGenerationRequest(
                message=form.get("message"),
                provider=form.get("provider", "openai"),
                model=form.get("model"),
                max_tokens=int(form.get("max_tokens", 1000)),
                temperature=float(form.get("temperature", 0.7)),
                system_prompt=form.get("system_prompt"),
                include_history=form.get("include_history", "true").lower() == "true"
            )
            images = form.getlist("images") if "images" in form else None
        else:
            # JSON으로 온 경우 - 텍스트만
            body = await request.json()
            
            # 기본값 설정
            body.setdefault('max_tokens', 1000)
            body.setdefault('temperature', 0.7)
            body.setdefault('provider', 'openai')
            body.setdefault('include_history', True)
            
            generation_request = ChatGenerationRequest(**body)
            images = None
        
    except Exception as parse_error:
        # 파싱 에러 시 에러 응답 반환
        error_message = f"Request parsing error: {str(parse_error)}"
        async def error_generator():
            yield f"data: {json.dumps({'type': 'error', 'error': error_message})}\n\n"
        return StreamingResponse(
            error_generator(), 
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
    
    async def generate():
        try:
            
            # 채팅 존재 및 권한 확인
            chat = db.query(Chat).filter(
                Chat.id == chat_id,
                Chat.user_id == current_user.id
            ).first()
            
            if not chat:
                yield f"data: {json.dumps({'error': 'Chat not found'})}\n\n"
                return
            
            # 사용자의 API 키 가져오기
            provider_key = None
            if generation_request.provider == "openai":
                api_key_record = get_api_key(db, current_user.id, "openai")
                if api_key_record:
                    provider_key = decrypt_api_key(api_key_record.encrypted_key)
            elif generation_request.provider == "anthropic":
                api_key_record = get_api_key(db, current_user.id, "anthropic")
                if api_key_record:
                    provider_key = decrypt_api_key(api_key_record.encrypted_key)
            elif generation_request.provider == "google":
                api_key_record = get_api_key(db, current_user.id, "google")
                if api_key_record:
                    provider_key = decrypt_api_key(api_key_record.encrypted_key)
            
            if not provider_key:
                yield f"data: {json.dumps({'error': f'No API key found for provider {generation_request.provider}'})}\n\n"
                return
            
            # 채팅 메시지 히스토리 가져오기 (최근 20개)
            messages = db.query(Message).filter(
                Message.chat_id == chat_id
            ).order_by(Message.created_at.desc()).limit(20).all()
            messages.reverse()  # 시간순 정렬
            
            # 메시지를 AI API 형식으로 변환 (빈 메시지 필터링)
            chat_messages = []
            for msg in messages:
                # 빈 메시지는 제외 (Anthropic API 요구사항)
                if not msg.content or not msg.content.strip():
                    continue
                    
                role = "user" if msg.sender == "user" else "assistant"
                chat_messages.append({
                    "role": role,
                    "content": msg.content
                })
            
            # 이미지 처리 (먼저 처리해서 빈 메시지 체크에서 사용)
            image_data = []
            # FormData에서 온 이미지들 처리
            if images:
                for image in images:
                    if image.filename:
                        # 이미지 읽기 및 base64 인코딩
                        image_bytes = await image.read()
                        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                        
                        image_data.append({
                            'data': image_b64,
                            'content_type': image.content_type,
                            'filename': image.filename
                        })
            
            # JSON 요청에서 온 이미지들 처리 (ChatGenerationRequest에 images 필드가 있는 경우)
            elif hasattr(generation_request, 'images') and generation_request.images:
                for img in generation_request.images:
                    # 이미지 데이터 검증
                    if img.data and img.data.strip():  # 빈 문자열이 아닌지 확인
                        image_data.append({
                            'data': img.data,
                            'content_type': img.content_type,
                            'filename': img.filename
                        })
                    # 빈 이미지 데이터는 건너뛰기
                    pass
            
            # 새로운 사용자 메시지 추가
            # 이미지만 있고 텍스트가 없는 경우도 허용 (Claude API는 별도 처리)
            if generation_request.message and generation_request.message.strip():
                # 텍스트 메시지가 있는 경우
                message_content = generation_request.message.strip()
            elif image_data:
                # 이미지만 있는 경우 - 빈 텍스트로 처리 (Claude는 서비스에서 처리)
                message_content = ""
            else:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Message content or images required'})}\\n\\n"
                return
            
            chat_messages.append({
                "role": "user",
                "content": message_content
            })
            
            # 사용자 메시지를 데이터베이스에 저장
            last_message = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.message_order.desc()).first()
            next_order = (last_message.message_order + 1) if last_message else 1
            
            user_message = Message(
                chat_id=chat_id,
                sender="user",
                content=generation_request.message,
                message_order=next_order,
                api_provider=generation_request.provider,
                model_name=generation_request.model
            )
            db.add(user_message)
            db.commit()
            db.refresh(user_message)
            
            # 이미지가 있다면 저장
            if image_data:
                for i, img in enumerate(image_data):
                    message_image = MessageImage(
                        message_id=user_message.id,
                        filename=img['filename'],
                        content_type=img['content_type'],
                        size=len(base64.b64decode(img['data'])),
                        data=img['data'],
                        order_index=i
                    )
                    db.add(message_image)
                db.commit()
            
            # 스트리밍 시작 이벤트
            yield f"data: {json.dumps({'type': 'start', 'message': 'Streaming started'})}\n\n"
            
            # AI 서비스를 통해 스트리밍 응답 생성
            full_response = ""
            async for chunk in ai_manager.generate_text_stream(
                prompt=generation_request.message,
                provider=generation_request.provider,
                max_tokens=generation_request.max_tokens,
                temperature=generation_request.temperature,
                model=generation_request.model,
                api_key=provider_key,
                messages=chat_messages,
                images=image_data if image_data else None,
                system_prompt=generation_request.system_prompt
            ):
                full_response += chunk.content
                # 스트리밍 청크 전송
                chunk_data = json.dumps({'type': 'chunk', 'content': chunk.content})
                yield f"data: {chunk_data}\n\n"
            
            # AI 응답을 데이터베이스에 저장
            ai_message = Message(
                chat_id=chat_id,
                sender="ai",
                content=full_response,
                message_order=next_order + 1,
                api_provider=generation_request.provider,
                model_name=generation_request.model
            )
            db.add(ai_message)
            db.commit()
            
            # 스트리밍 완료 이벤트
            yield f"data: {json.dumps({'type': 'end', 'full_content': full_response})}\n\n"
            
        except Exception as e:
            db.rollback()
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # nginx 버퍼링 비활성화
        }
    )

@router.get("/health")
async def health_check():
    """AI 서비스 상태 체크"""
    return {
        "status": "healthy",
        "message": "AI services are operational"
    }