from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Annotated
from ..database import get_db
from ..models.user import User
from ..models.post import Post, Media
from ..models.comment import Comment
from ..models.reaction import Reaction
from ..schemas import PostCreate, PostResponse, User as UserSchema
from ..routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Create a new post"""
    db_post = Post(
        user_id=current_user.id,
        content=post.content,
        topic=post.topic,
        keywords=post.keywords
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Add media if provided
    if post.media:
        for media_item in post.media:
            db_media = Media(
                post_id=db_post.id,
                media_type=media_item.media_type,
                url=media_item.url
            )
            db.add(db_media)
        db.commit()
        db.refresh(db_post)
    
    # Trigger bot processing for this post (async in production)
    from ..services.bot_service import BotEngine
    bot_engine = BotEngine(db)
    bot_engine.process_single_post(db_post.id)
    
    return enrich_post_response(db_post, db)

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all posts (feed)"""
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return [enrich_post_response(post, db) for post in posts]

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return enrich_post_response(post, db)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete a post (only by owner)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return None

def enrich_post_response(post: Post, db: Session) -> dict:
    """Add counts to post response"""
    like_count = db.query(func.count(Reaction.id)).filter(
        Reaction.post_id == post.id,
        Reaction.is_like == True
    ).scalar()
    
    dislike_count = db.query(func.count(Reaction.id)).filter(
        Reaction.post_id == post.id,
        Reaction.is_like == False
    ).scalar()
    
    comment_count = db.query(func.count(Comment.id)).filter(
        Comment.post_id == post.id
    ).scalar()
    
    post_dict = {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "topic": post.topic,
        "keywords": post.keywords,
        "created_at": post.created_at,
        "user": post.user,
        "media": post.media,
        "like_count": like_count or 0,
        "dislike_count": dislike_count or 0,
        "comment_count": comment_count or 0
    }
    
    return post_dict
