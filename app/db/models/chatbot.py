from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey, text
from sqlalchemy.orm import relationship
from db.database import Base
import enum

class ChatAuthorEnum(enum.Enum):
    user = "user"
    bot = "bot"

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = Column(Enum(ChatAuthorEnum), nullable=False)
    content = Column(String(2000), nullable=False)
    timestamp = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )

    # Relations
    user = relationship("User", back_populates="chat_messages")

