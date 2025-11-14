from pydantic import BaseModel, ConfigDict
from datetime import datetime
from db.models.chatbot import ChatAuthorEnum

class ChatMessageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str
    author: ChatAuthorEnum

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    user_id: int
    timestamp: datetime

