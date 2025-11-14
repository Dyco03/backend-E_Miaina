from fastapi import APIRouter, Depends, Query
from schemas import chatbot as chatbot_schemas
from sqlalchemy.orm import Session
from db.database import get_db
from crud import chatbot as chatbot_crud
from utils.auth import get_current_user
from db.models.users import User
from db.models.chatbot import ChatAuthorEnum

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

@router.get("/messages", response_model=list[chatbot_schemas.ChatMessageResponse])
def get_messages(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat messages for current user"""
    messages = chatbot_crud.get_user_messages(db, current_user.id, limit)
    return messages

@router.post("/messages", response_model=chatbot_schemas.ChatMessageResponse)
def send_message(
    message: chatbot_schemas.ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to the chatbot"""
    # Ensure the message is from the user
    message.author = ChatAuthorEnum.user
    
    db_message = chatbot_crud.create_chat_message(db, message, current_user.id)
    
    # TODO: Implement actual chatbot logic here
    # For now, just return a simple response
    bot_response_content = "Merci pour votre message. Je suis là pour vous aider avec vos questions sur le savoir-vivre à Madagascar."
    bot_response = chatbot_crud.create_bot_response(db, current_user.id, bot_response_content)
    
    return db_message

