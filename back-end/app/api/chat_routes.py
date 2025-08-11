from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.crud.chat_crud import (
    get_user_chats,
    get_chat_by_id,
    create_chat,
    update_chat,
    delete_chat,
    get_chat_messages,
    add_message_to_chat,
    clear_chat_messages
)
from app.schemas.chat_schemas import (
    ChatCreate,
    ChatUpdate,
    ChatResponse,
    MessageCreate,
    MessageResponse
)
from app.models.user import User

router = APIRouter(prefix="/api/v1/chats", tags=["chats"])

@router.get("/", response_model=List[ChatResponse])
def get_chats(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_chats(db, current_user.id, limit)

@router.post("/", response_model=ChatResponse)
def create_new_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_chat(db, current_user.id, chat_data)

@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = get_chat_by_id(db, chat_id, current_user.id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat

@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat_info(
    chat_id: int,
    chat_data: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = update_chat(db, chat_id, current_user.id, chat_data)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat

@router.delete("/{chat_id}")
def delete_chat_by_id(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_chat(db, chat_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return {"message": "Chat deleted successfully"}

@router.get("/{chat_id}/messages")
def get_chat_messages_list(
    chat_id: int,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    messages = get_chat_messages(db, chat_id, current_user.id, limit=limit, offset=offset)
    if messages is None:
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # 응답 변환: message_images를 images 형태로 변환
    response_messages = []
    for msg in messages:
        # 이미지 데이터 변환
        images_data = [
            {
                "filename": img.filename,
                "content_type": img.content_type,
                "data": img.data,
                "size": img.size
            }
            for img in msg.message_images
        ]
        
        # 직접 딕셔너리 형태로 응답 구성
        message_dict = {
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.content, 
            "message_order": msg.message_order,
            "api_provider": msg.api_provider,
            "model_name": msg.model_name,
            "token_count": msg.token_count,
            "images": images_data,  # 변환된 이미지 데이터
            "created_at": msg.created_at.isoformat()
        }
        response_messages.append(message_dict)
    
    return response_messages

@router.post("/{chat_id}/messages", response_model=MessageResponse)
def add_message(
    chat_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Add message request: chat_id={chat_id}, user={current_user.id}")
    print(f"Message data: sender={message_data.sender}, content={message_data.content[:50]}...")
    
    # sender 유효성 검사
    if message_data.sender not in ["user", "ai"]:
        print(f"Invalid sender: {message_data.sender}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender must be 'user' or 'ai'"
        )
    
    message = add_message_to_chat(db, chat_id, current_user.id, message_data)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return message

@router.delete("/{chat_id}/messages")
def clear_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = clear_chat_messages(db, chat_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return {"message": "Chat messages cleared successfully"}