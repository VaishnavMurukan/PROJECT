from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..models.user import User
from ..models.post import Post
from ..models.reaction import Reaction
from ..schemas import ReactionCreate, ReactionResponse
from ..routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Reactions"])

@router.post("/{post_id}/reactions", response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
def create_reaction(
    post_id: int,
    reaction: ReactionCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Create or update a reaction on a post"""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already reacted
    existing_reaction = db.query(Reaction).filter(
        Reaction.post_id == post_id,
        Reaction.user_id == current_user.id
    ).first()
    
    if existing_reaction:
        # Update existing reaction
        existing_reaction.is_like = reaction.is_like
        db.commit()
        db.refresh(existing_reaction)
        return existing_reaction
    
    # Create new reaction
    db_reaction = Reaction(
        post_id=post_id,
        user_id=current_user.id,
        is_like=reaction.is_like
    )
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    
    return db_reaction

@router.delete("/{post_id}/reactions", status_code=status.HTTP_204_NO_CONTENT)
def delete_reaction(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Remove reaction from a post"""
    reaction = db.query(Reaction).filter(
        Reaction.post_id == post_id,
        Reaction.user_id == current_user.id
    ).first()
    
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    
    db.delete(reaction)
    db.commit()
    return None
