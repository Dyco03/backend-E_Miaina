from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class ChallengeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    date: date
    points: int = 10

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserChallengeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    challenge_id: int
    is_completed: bool = False

class UserChallengeCreate(UserChallengeBase):
    pass

class UserChallengeResponse(UserChallengeBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime

class ChallengeWithStatus(ChallengeResponse):
    is_completed: bool
    completed_at: Optional[datetime] = None

