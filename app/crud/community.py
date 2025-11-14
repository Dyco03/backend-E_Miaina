from db.models.community import Discussion, Comment
from db.models.users import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import community as community_schemas
from utils.helpers import get_user_display_name
from typing import List

def get_discussion_by_id(db: Session, discussion_id: int):
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return discussion

def get_all_discussions(db: Session):
    discussions = db.query(Discussion).order_by(Discussion.created_at.desc()).all()
    return discussions

def create_discussion(db: Session, discussion: community_schemas.DiscussionCreate, user_id: int):
    try:
        db_discussion = Discussion(
            title=discussion.title,
            description=discussion.description,
            user_id=user_id,
        )
        db.add(db_discussion)
        db.commit()
        db.refresh(db_discussion)
        return db_discussion
    except Exception as e:
        db.rollback()
        print(f"Error creating discussion: {e}")
        raise HTTPException(status_code=400, detail="Error creating discussion") from e

def get_comment_by_id(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

def get_comments_by_discussion(db: Session, discussion_id: int):
    comments = db.query(Comment).filter(
        Comment.discussion_id == discussion_id
    ).order_by(Comment.created_at.asc()).all()
    return comments

def create_comment(db: Session, comment: community_schemas.CommentCreate, user_id: int):
    # Verify discussion exists
    discussion = get_discussion_by_id(db, comment.discussion_id)
    
    # Get user for author name
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db_comment = Comment(
            discussion_id=comment.discussion_id,
            user_id=user_id,
            message=comment.message,
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        db.rollback()
        print(f"Error creating comment: {e}")
        raise HTTPException(status_code=400, detail="Error creating comment") from e

def get_discussion_with_comments(db: Session, discussion_id: int):
    discussion = get_discussion_by_id(db, discussion_id)
    comments = get_comments_by_discussion(db, discussion_id)
    discussion.comments = comments
    return discussion

