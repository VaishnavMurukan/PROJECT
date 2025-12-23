from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from ..database import get_db
from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment
from ..models.bot import Bot
from ..schemas import CommentCreate, CommentResponse
from ..routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Comments"])

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Create a comment on a post"""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return format_comment_response(db_comment)

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get all comments for a post"""
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return [format_comment_response(comment) for comment in comments]

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete a comment (only by owner)"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return None

def format_comment_response(comment: Comment) -> dict:
    """Format comment with author information"""
    if comment.user_id:
        author_name = comment.user.username
        is_bot = False
    elif comment.bot_id:
        author_name = comment.bot.name
        is_bot = True
    else:
        author_name = "Unknown"
        is_bot = False
    
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "bot_id": comment.bot_id,
        "content": comment.content,
        "created_at": comment.created_at,
        "author_name": author_name,
        "is_bot": is_bot
    }
