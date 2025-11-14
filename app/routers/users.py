from fastapi import APIRouter, Depends, Path, HTTPException, status
from schemas import users as user_schemas
from sqlalchemy.orm import Session
from db.database import get_db
from crud import users as user_crud
from utils import security
from utils.auth import get_current_user
from db.models.users import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=user_schemas.UserResponse)
def register(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = user_crud.create_user(db, user)
    return db_user

@router.post("/login", response_model=user_schemas.LoginResponse)
def login(login_data: user_schemas.LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = user_crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info"""
    return current_user


@router.put("/me", response_model=user_schemas.UserResponse)
def update_current_user(
    user_update: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    updated_user = user_crud.update_user(db, current_user.id, user_update)
    return updated_user

@router.post("/reset-password")
def reset_password(
    reset_data: user_schemas.ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Request password reset (placeholder - implement email sending)"""
    user = user_crud.get_user_by_email(db, reset_data.email)
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a password reset link has been sent"}
    # TODO: Implement email sending with reset token
    return {"message": "If the e-mail exists, a password reset link has been sent"}

@router.get("/all", response_model=list[user_schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users (admin only - add admin check if needed)"""
    users = user_crud.get_all_users(db)
    return users

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user_by_id(user_id: int = Path(), db: Session = Depends(get_db)):
    """Get user by ID"""
    user = user_crud.get_user_by_id(db, user_id)
    return user