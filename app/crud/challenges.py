from db.models.challenges import Challenge, UserChallenge
from db.models.users import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import challenges as challenge_schemas
from datetime import date, datetime
from typing import List

def get_challenge_by_id(db: Session, challenge_id: int):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge

def get_all_challenges(db: Session):
    challenges = db.query(Challenge).all()
    return challenges

def get_daily_challenge(db: Session, challenge_date: date = None):
    if challenge_date is None:
        challenge_date = date.today()
    
    challenge = db.query(Challenge).filter(Challenge.date == challenge_date).first()
    return challenge

def create_challenge(db: Session, challenge: challenge_schemas.ChallengeCreate):
    try:
        db_challenge = Challenge(
            title=challenge.title,
            description=challenge.description,
            date=challenge.date,
            points=challenge.points,
        )
        db.add(db_challenge)
        db.commit()
        db.refresh(db_challenge)
        return db_challenge
    except Exception as e:
        db.rollback()
        print(f"Error creating challenge: {e}")
        raise HTTPException(status_code=400, detail="Error creating challenge") from e

def get_user_challenge(db: Session, user_id: int, challenge_id: int):
    user_challenge = db.query(UserChallenge).filter(
        UserChallenge.user_id == user_id,
        UserChallenge.challenge_id == challenge_id
    ).first()
    return user_challenge

def create_user_challenge(db: Session, user_id: int, challenge_id: int):
    # Check if already exists
    existing = get_user_challenge(db, user_id, challenge_id)
    if existing:
        return existing
    
    try:
        user_challenge = UserChallenge(
            user_id=user_id,
            challenge_id=challenge_id,
            is_completed=False,
        )
        db.add(user_challenge)
        db.commit()
        db.refresh(user_challenge)
        return user_challenge
    except Exception as e:
        db.rollback()
        print(f"Error creating user challenge: {e}")
        raise HTTPException(status_code=400, detail="Error creating user challenge") from e

def complete_challenge(db: Session, user_id: int, challenge_id: int):
    user_challenge = get_user_challenge(db, user_id, challenge_id)
    if not user_challenge:
        # Create if doesn't exist
        user_challenge = create_user_challenge(db, user_id, challenge_id)
    
    if user_challenge.is_completed:
        raise HTTPException(
            status_code=400,
            detail="Challenge already completed"
        )
    
    # Get challenge to get points
    challenge = get_challenge_by_id(db, challenge_id)
    
    try:
        user_challenge.is_completed = True
        user_challenge.completed_at = datetime.utcnow()
        
        # Add points to user
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_points += challenge.points
        
        db.commit()
        db.refresh(user_challenge)
        return user_challenge
    except Exception as e:
        db.rollback()
        print(f"Error completing challenge: {e}")
        raise HTTPException(status_code=400, detail="Error completing challenge") from e

def get_completed_challenges(db: Session, user_id: int):
    user_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == user_id,
        UserChallenge.is_completed == True
    ).all()
    return user_challenges

def get_challenges_with_status(db: Session, user_id: int):
    """Get all challenges with completion status for a user"""
    challenges = get_all_challenges(db)
    result = []
    
    for challenge in challenges:
        user_challenge = get_user_challenge(db, user_id, challenge.id)
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "date": challenge.date,
            "points": challenge.points,
            "is_completed": user_challenge.is_completed if user_challenge else False,
            "completed_at": user_challenge.completed_at if user_challenge else None,
            "created_at": challenge.created_at,
            "updated_at": challenge.updated_at,
        })
    
    return result

def get_total_points(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.total_points

