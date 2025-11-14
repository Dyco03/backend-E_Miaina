from fastapi import APIRouter, Depends, Path, Query, HTTPException
from schemas import challenges as challenge_schemas
from sqlalchemy.orm import Session
from db.database import get_db
from crud import challenges as challenge_crud
from utils.auth import get_current_user
from db.models.users import User
from datetime import date

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"]
)

@router.get("/", response_model=list[challenge_schemas.ChallengeWithStatus])
def get_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all challenges with completion status for current user"""
    challenges = challenge_crud.get_challenges_with_status(db, current_user.id)
    return challenges

@router.get("/daily", response_model=challenge_schemas.ChallengeWithStatus)
def get_daily_challenge(
    challenge_date: date = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get daily challenge for a specific date (defaults to today)"""
    challenge = challenge_crud.get_daily_challenge(db, challenge_date)
    if not challenge:
        raise HTTPException(status_code=404, detail="No challenge found for this date")
    
    user_challenge = challenge_crud.get_user_challenge(db, current_user.id, challenge.id)
    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description,
        "date": challenge.date,
        "points": challenge.points,
        "is_completed": user_challenge.is_completed if user_challenge else False,
        "completed_at": user_challenge.completed_at if user_challenge else None,
        "created_at": challenge.created_at,
        "updated_at": challenge.updated_at,
    }

@router.get("/{challenge_id}", response_model=challenge_schemas.ChallengeWithStatus)
def get_challenge(
    challenge_id: int = Path(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific challenge with completion status"""
    challenge = challenge_crud.get_challenge_by_id(db, challenge_id)
    user_challenge = challenge_crud.get_user_challenge(db, current_user.id, challenge.id)
    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description,
        "date": challenge.date,
        "points": challenge.points,
        "is_completed": user_challenge.is_completed if user_challenge else False,
        "completed_at": user_challenge.completed_at if user_challenge else None,
        "created_at": challenge.created_at,
        "updated_at": challenge.updated_at,
    }

@router.post("/{challenge_id}/complete", response_model=challenge_schemas.UserChallengeResponse)
def complete_challenge(
    challenge_id: int = Path(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete a challenge and earn points"""
    user_challenge = challenge_crud.complete_challenge(db, current_user.id, challenge_id)
    return user_challenge

@router.get("/completed/all", response_model=list[challenge_schemas.UserChallengeResponse])
def get_completed_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all completed challenges for current user"""
    completed = challenge_crud.get_completed_challenges(db, current_user.id)
    return completed

@router.get("/points/total")
def get_total_points(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get total points for current user"""
    total = challenge_crud.get_total_points(db, current_user.id)
    return {"total_points": total}

# Admin routes (add admin check if needed)
@router.post("/", response_model=challenge_schemas.ChallengeResponse)
def create_challenge(
    challenge: challenge_schemas.ChallengeCreate,
    db: Session = Depends(get_db)
):
    """Create a new challenge (admin only)"""
    db_challenge = challenge_crud.create_challenge(db, challenge)
    return db_challenge

