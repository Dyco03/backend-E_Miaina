from db.models.users import User
from db.models.community import Discussion, Comment
from sqlalchemy.orm import Session

def get_user_display_name(user: User) -> str:
    """Get display name for a user"""
    return user.displayName or f"{user.firstName} {user.lastName}"

def add_author_names_to_comments(comments: list[Comment], db: Session) -> list[dict]:
    """Convert comments to dict with author names"""
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        author_name = get_user_display_name(user) if user else "Unknown"
        result.append({
            "id": comment.id,
            "discussion_id": comment.discussion_id,
            "authorName": author_name,
            "message": comment.message,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
        })
    return result

def add_author_names_to_discussions(discussions: list[Discussion], db: Session) -> list[dict]:
    """Convert discussions to dict with author names and comments"""
    result = []
    for discussion in discussions:
        user = db.query(User).filter(User.id == discussion.user_id).first()
        author_name = get_user_display_name(user) if user else "Unknown"
        
        # Get comments with author names
        comments = add_author_names_to_comments(discussion.comments, db)
        
        result.append({
            "id": discussion.id,
            "title": discussion.title,
            "description": discussion.description,
            "user_id": discussion.user_id,
            "created_at": discussion.created_at,
            "updated_at": discussion.updated_at,
            "comments": comments,
        })
    return result

