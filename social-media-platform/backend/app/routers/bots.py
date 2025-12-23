from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.bot import Bot, BotProfile
from ..schemas import BotCreate, BotResponse

router = APIRouter(prefix="/bots", tags=["Bots"])

@router.post("/", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
def create_bot(bot: BotCreate, db: Session = Depends(get_db)):
    """Create a new bot with profile"""
    # Check if bot name exists
    existing_bot = db.query(Bot).filter(Bot.name == bot.name).first()
    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot name already exists"
        )
    
    # Create bot
    db_bot = Bot(name=bot.name)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    
    # Create bot profile
    db_profile = BotProfile(
        bot_id=db_bot.id,
        age_group=bot.profile.age_group,
        profession=bot.profile.profession,
        region=bot.profile.region,
        interests=bot.profile.interests,
        emotional_bias=bot.profile.emotional_bias,
        like_probability=bot.profile.like_probability,
        dislike_probability=bot.profile.dislike_probability,
        comment_probability=bot.profile.comment_probability,
        min_response_delay=bot.profile.min_response_delay,
        max_response_delay=bot.profile.max_response_delay
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_bot)
    
    return db_bot

@router.get("/", response_model=List[BotResponse])
def get_bots(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get all bots"""
    bots = db.query(Bot).offset(skip).limit(limit).all()
    return bots

@router.get("/{bot_id}", response_model=BotResponse)
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    """Get a specific bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

@router.patch("/{bot_id}/toggle", response_model=BotResponse)
def toggle_bot_status(bot_id: int, db: Session = Depends(get_db)):
    """Toggle bot active/inactive status"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    bot.is_active = not bot.is_active
    db.commit()
    db.refresh(bot)
    
    return bot

@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    """Delete a bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    db.delete(bot)
    db.commit()
    return None

@router.post("/process-posts", status_code=status.HTTP_200_OK)
def trigger_bot_processing(hours: int = 24, db: Session = Depends(get_db)):
    """Manually trigger bot processing for recent posts"""
    from ..services.bot_service import BotEngine
    
    bot_engine = BotEngine(db)
    results = bot_engine.process_recent_posts(hours=hours)
    
    return {
        "message": f"Bot processing triggered for posts from last {hours} hours",
        "posts_processed": results.get("posts", 0),
        "bots_active": results.get("bots", 0),
        "interactions": results.get("interactions", 0)
    }

@router.patch("/{bot_id}/activate", response_model=BotResponse)
def activate_bot(bot_id: int, db: Session = Depends(get_db)):
    """Activate a specific bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    bot.is_active = True
    db.commit()
    db.refresh(bot)
    return bot

@router.patch("/{bot_id}/deactivate", response_model=BotResponse)
def deactivate_bot(bot_id: int, db: Session = Depends(get_db)):
    """Deactivate a specific bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    bot.is_active = False
    db.commit()
    db.refresh(bot)
    return bot

@router.post("/activate-all", status_code=status.HTTP_200_OK)
def activate_all_bots(db: Session = Depends(get_db)):
    """Activate all bots"""
    db.query(Bot).update({Bot.is_active: True})
    db.commit()
    count = db.query(Bot).count()
    return {"message": f"Activated {count} bots"}

@router.post("/deactivate-all", status_code=status.HTTP_200_OK)
def deactivate_all_bots(db: Session = Depends(get_db)):
    """Deactivate all bots"""
    db.query(Bot).update({Bot.is_active: False})
    db.commit()
    count = db.query(Bot).count()
    return {"message": f"Deactivated {count} bots"}
