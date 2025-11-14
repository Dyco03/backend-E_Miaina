from db.models.chatbot import ChatMessage, ChatAuthorEnum
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas import chatbot as chatbot_schemas
from typing import List

def get_chat_message_by_id(db: Session, message_id: int):
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Chat message not found")
    return message

def get_user_messages(db: Session, user_id: int, limit: int = 50):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
    return list(reversed(messages))  # Return in chronological order

def create_chat_message(db: Session, message: chatbot_schemas.ChatMessageCreate, user_id: int):
    try:
        db_message = ChatMessage(
            user_id=user_id,
            author=message.author,
            content=message.content,
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        print(f"Error creating chat message: {e}")
        raise HTTPException(status_code=400, detail="Error creating chat message") from e

def create_bot_response(db: Session, user_id: int, content: str):
    """Helper function to create a bot response message"""
    try:
        db_message = ChatMessage(
            user_id=user_id,
            author=ChatAuthorEnum.bot,
            content=content,
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        print(f"Error creating bot response: {e}")
        raise HTTPException(status_code=400, detail="Error creating bot response") from e

