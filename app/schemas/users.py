from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    lastName: str
    firstName: str
    email: EmailStr
    displayName: Optional[str] = None
    birthday: Optional[date] = None
    phoneNumber: Optional[str] = None
    sector: Optional[str] = None
    arrivalDetails: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    displayName: Optional[str] = None
    birthday: Optional[date] = None
    phoneNumber: Optional[str] = None
    sector: Optional[str] = None
    arrivalDetails: Optional[str] = None
    onboarding_completed: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    total_points: int
    onboarding_completed: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ResetPasswordRequest(BaseModel):
    email: EmailStr