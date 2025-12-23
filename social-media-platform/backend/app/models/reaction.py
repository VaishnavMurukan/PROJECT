from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Reaction(Base):
    __tablename__ = "reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for bot reactions
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=True)  # For bot-generated reactions
    is_like = Column(Boolean, nullable=False)  # True for like, False for dislike
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="reactions")
    user = relationship("User", back_populates="reactions")
    bot = relationship("Bot", back_populates="reactions")
    
    # Ensure a user or bot can only react once per post
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_user_reaction'),
        UniqueConstraint('post_id', 'bot_id', name='unique_bot_reaction'),
    )
