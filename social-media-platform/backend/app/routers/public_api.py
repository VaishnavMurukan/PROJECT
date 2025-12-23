from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models.post import Post
from ..models.comment import Comment
from ..models.reaction import Reaction
from ..schemas import PublicPost, PublicComment

router = APIRouter(prefix="/public", tags=["Public API"])

@router.get("/posts", response_model=List[PublicPost])
def get_public_posts(
    skip: int = 0,
    limit: int = 100,
    language: Optional[str] = Query(None, description="Filter by language (not implemented)"),
    date_from: Optional[datetime] = Query(None, description="Filter posts from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter posts until this date"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    db: Session = Depends(get_db)
):
    """
    Public API endpoint for external services (like sentiment analysis engine).
    Returns posts with comments in a standardized format.
    """
    query = db.query(Post)
    
    # Apply filters
    if date_from:
        query = query.filter(Post.created_at >= date_from)
    if date_to:
        query = query.filter(Post.created_at <= date_to)
    if topic:
        query = query.filter(Post.topic.ilike(f"%{topic}%"))
    
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        # Get likes and dislikes count
        likes = db.query(Reaction).filter(
            Reaction.post_id == post.id,
            Reaction.is_like == True
        ).count()
        
        dislikes = db.query(Reaction).filter(
            Reaction.post_id == post.id,
            Reaction.is_like == False
        ).count()
        
        # Get comments
        comments = db.query(Comment).filter(Comment.post_id == post.id).all()
        public_comments = [
            PublicComment(
                id=comment.id,
                content=comment.content,
                created_at=comment.created_at,
                is_bot=comment.bot_id is not None
            )
            for comment in comments
        ]
        
        result.append(
            PublicPost(
                id=post.id,
                content=post.content,
                topic=post.topic,
                created_at=post.created_at,
                likes=likes,
                dislikes=dislikes,
                comments=public_comments
            )
        )
    
    return result

@router.get("/comments")
def get_public_comments(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all comments (standalone endpoint for sentiment analysis).
    Returns just the comment texts.
    """
    query = db.query(Comment)
    
    if date_from:
        query = query.filter(Comment.created_at >= date_from)
    if date_to:
        query = query.filter(Comment.created_at <= date_to)
    
    comments = query.order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "is_bot": comment.bot_id is not None
        }
        for comment in comments
    ]

@router.get("/stats")
def get_platform_stats(db: Session = Depends(get_db)):
    """Get platform statistics"""
    from ..models.user import User
    from ..models.bot import Bot
    
    total_posts = db.query(Post).count()
    total_comments = db.query(Comment).count()
    total_reactions = db.query(Reaction).count()
    total_users = db.query(User).count()
    total_bots = db.query(Bot).count()
    active_bots = db.query(Bot).filter(Bot.is_active == True).count()
    
    return {
        "total_posts": total_posts,
        "total_comments": total_comments,
        "total_reactions": total_reactions,
        "total_users": total_users,
        "total_bots": total_bots,
        "active_bots": active_bots
    }
