from db.models.users import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import users as user_schemas 
from utils import security  

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def create_user(db: Session, user: user_schemas.UserCreate):
    # Check if user already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        db_user = User(
            lastName=user.lastName,
            firstName=user.firstName,
            email=user.email,
            password_hash=security.hash_password(user.password),
            displayName=user.displayName,
            birthday=user.birthday,
            phoneNumber=user.phoneNumber,
            sector=user.sector,
            arrivalDetails=user.arrivalDetails,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Error creating user") from e

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.password_hash):
        return False
    return user

def update_user(db: Session, user_id: int, user_update: user_schemas.UserUpdate):
    user = get_user_by_id(db, user_id)
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=400, detail="Error updating user") from e

def add_points(db: Session, user_id: int, points: int):
    user = get_user_by_id(db, user_id)
    user.total_points += points
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Error adding points: {e}")
        raise HTTPException(status_code=400, detail="Error adding points") from e