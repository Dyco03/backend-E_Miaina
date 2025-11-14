from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str

class CommentCreate(CommentBase):
    discussion_id: int

class CommentResponse(CommentBase):
    id: int
    discussion_id: int
    authorName: str
    created_at: datetime
    updated_at: datetime

class DiscussionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str

class DiscussionCreate(DiscussionBase):
    pass

class DiscussionResponse(DiscussionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    comments: List[CommentResponse] = []

