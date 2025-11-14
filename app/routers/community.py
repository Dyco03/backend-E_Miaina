from fastapi import APIRouter, Depends, Path
from schemas import community as community_schemas
from sqlalchemy.orm import Session
from db.database import get_db
from crud import community as community_crud
from utils.auth import get_current_user
from utils.helpers import get_user_display_name
from db.models.users import User

router = APIRouter(
    prefix="/community",
    tags=["community"]
)

@router.get("/discussions", response_model=list[community_schemas.DiscussionResponse])
def get_discussions(db: Session = Depends(get_db)):
    """Get all discussions"""
    discussions = community_crud.get_all_discussions(db)
    result = []
    for discussion in discussions:
        user = db.query(User).filter(User.id == discussion.user_id).first()
        # Get comments with author names
        comments_data = []
        for comment in discussion.comments:
            comment_user = db.query(User).filter(User.id == comment.user_id).first()
            comments_data.append(community_schemas.CommentResponse(
                id=comment.id,
                discussion_id=comment.discussion_id,
                authorName=get_user_display_name(comment_user) if comment_user else "Unknown",
                message=comment.message,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            ))
        
        result.append(community_schemas.DiscussionResponse(
            id=discussion.id,
            title=discussion.title,
            description=discussion.description,
            user_id=discussion.user_id,
            created_at=discussion.created_at,
            updated_at=discussion.updated_at,
            comments=comments_data,
        ))
    return result

@router.get("/discussions/{discussion_id}", response_model=community_schemas.DiscussionResponse)
def get_discussion(
    discussion_id: int = Path(),
    db: Session = Depends(get_db)
):
    """Get a specific discussion with comments"""
    discussion = community_crud.get_discussion_with_comments(db, discussion_id)
    # Add author names to comments
    comments_data = []
    for comment in discussion.comments:
        comment_user = db.query(User).filter(User.id == comment.user_id).first()
        comments_data.append(community_schemas.CommentResponse(
            id=comment.id,
            discussion_id=comment.discussion_id,
            authorName=get_user_display_name(comment_user) if comment_user else "Unknown",
            message=comment.message,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        ))
    
    return community_schemas.DiscussionResponse(
        id=discussion.id,
        title=discussion.title,
        description=discussion.description,
        user_id=discussion.user_id,
        created_at=discussion.created_at,
        updated_at=discussion.updated_at,
        comments=comments_data,
    )

@router.post("/discussions", response_model=community_schemas.DiscussionResponse)
def create_discussion(
    discussion: community_schemas.DiscussionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new discussion"""
    db_discussion = community_crud.create_discussion(db, discussion, current_user.id)
    return community_schemas.DiscussionResponse(
        id=db_discussion.id,
        title=db_discussion.title,
        description=db_discussion.description,
        user_id=db_discussion.user_id,
        created_at=db_discussion.created_at,
        updated_at=db_discussion.updated_at,
        comments=[],
    )

@router.post("/comments", response_model=community_schemas.CommentResponse)
def create_comment(
    comment: community_schemas.CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new comment on a discussion"""
    db_comment = community_crud.create_comment(db, comment, current_user.id)
    author_name = get_user_display_name(current_user)
    return community_schemas.CommentResponse(
        id=db_comment.id,
        discussion_id=db_comment.discussion_id,
        authorName=author_name,
        message=db_comment.message,
        created_at=db_comment.created_at,
        updated_at=db_comment.updated_at,
    )

@router.get("/discussions/{discussion_id}/comments", response_model=list[community_schemas.CommentResponse])
def get_comments(
    discussion_id: int = Path(),
    db: Session = Depends(get_db)
):
    """Get all comments for a discussion"""
    comments = community_crud.get_comments_by_discussion(db, discussion_id)
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append(community_schemas.CommentResponse(
            id=comment.id,
            discussion_id=comment.discussion_id,
            authorName=get_user_display_name(user) if user else "Unknown",
            message=comment.message,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        ))
    return result

