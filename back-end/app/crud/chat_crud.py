from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc
from app.models.chat import Chat
from app.models.message import Message
from app.models.message_image import MessageImage
from app.schemas.chat_schemas import ChatCreate, ChatUpdate, MessageCreate

def get_user_chats(db: Session, user_id: str, limit: int = 50):
    # 채팅 목록만 가져오기 (최근 메시지 정보 제거로 성능 개선)
    chats = db.query(Chat).filter(
        Chat.user_id == user_id
    ).order_by(desc(Chat.updated_at)).limit(limit).all()
    
    return chats

def get_chat_by_id(db: Session, chat_id: int, user_id: str):
    return db.query(Chat).options(
        joinedload(Chat.messages)
    ).filter(
        Chat.id == chat_id,
        Chat.user_id == user_id
    ).first()

def create_chat(db: Session, user_id: str, chat_data: ChatCreate):
    db_chat = Chat(
        user_id=user_id,
        title=chat_data.title,
        system_prompt=chat_data.system_prompt,
        model=chat_data.model,
        temperature=chat_data.temperature,
        max_tokens=chat_data.max_tokens
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def update_chat(db: Session, chat_id: int, user_id: str, chat_data: ChatUpdate):
    chat = get_chat_by_id(db, chat_id, user_id)
    if not chat:
        return None
    
    update_data = chat_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chat, field, value)
    
    chat.updated_at = func.now()
    db.commit()
    db.refresh(chat)
    return chat

def delete_chat(db: Session, chat_id: int, user_id: str):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == user_id
    ).first()
    
    if chat:
        db.delete(chat)
        db.commit()
        return True
    return False

def get_chat_messages(db: Session, chat_id: int, user_id: str, limit: int = None, offset: int = 0):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == user_id
    ).first()
    
    if not chat:
        return None
    
    query = db.query(Message).options(
        joinedload(Message.message_images)
    ).filter(
        Message.chat_id == chat_id
    ).order_by(Message.message_order.desc(), Message.created_at.desc())  # 최신 메시지부터 (DESC)
    
    if limit:
        query = query.offset(offset).limit(limit)
    
    return query.all()

def add_message_to_chat(db: Session, chat_id: int, user_id: str, message_data: MessageCreate):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == user_id
    ).first()
    
    if not chat:
        return None
    
    # 다음 메시지 순서 계산
    last_message = db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(desc(Message.message_order)).first()
    
    next_order = (last_message.message_order + 1) if last_message else 1
    
    db_message = Message(
        chat_id=chat_id,
        sender=message_data.sender,
        content=message_data.content,
        message_order=next_order,
        api_provider=message_data.api_provider,
        model_name=message_data.model_name,
        token_count=message_data.token_count
    )
    
    db.add(db_message)
    
    # 채팅 업데이트 시간 갱신
    chat.updated_at = func.now()
    
    db.commit()
    db.refresh(db_message)
    return db_message

def clear_chat_messages(db: Session, chat_id: int, user_id: str):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == user_id
    ).first()
    
    if not chat:
        return False
    
    db.query(Message).filter(Message.chat_id == chat_id).delete()
    chat.updated_at = func.now()
    db.commit()
    return True