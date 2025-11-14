from sqlalchemy import Column, Integer, String, Date, Enum, TIMESTAMP, Boolean, text
from sqlalchemy.orm import relationship
from db.database import Base
import enum

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    displayName = Column(String(100), nullable=True)
    birthday = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    phoneNumber = Column(String(20), nullable=True)
    sector = Column(String(100), nullable=True)
    arrivalDetails = Column(String(500), nullable=True)
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    total_points = Column(Integer, default=0, nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )

    # Relations
    user_challenges = relationship("UserChallenge", back_populates="user")
    discussions = relationship("Discussion", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
