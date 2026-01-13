from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base

class EmotionalBias(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class Bot(Base):
    __tablename__ = "bots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    profile = relationship("BotProfile", back_populates="bot", uselist=False, cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="bot", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="bot", cascade="all, delete-orphan")
    interaction_logs = relationship("BotInteractionLog", back_populates="bot", cascade="all, delete-orphan")

class BotProfile(Base):
    __tablename__ = "bot_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), unique=True, nullable=False)
    
    # Demographics
    age_group = Column(String)  # e.g., "18-25", "26-35"
    profession = Column(String)  # e.g., "student", "engineer"
    region = Column(String)  # e.g., "North America", "Asia"
    
    # Interests (comma-separated)
    interests = Column(String)  # e.g., "technology,sports,music"
    
    # Emotional characteristics
    emotional_bias = Column(Enum(EmotionalBias), default=EmotionalBias.NEUTRAL)
    
    # Behavior probabilities (0.0 to 1.0)
    like_probability = Column(Float, default=0.5)
    dislike_probability = Column(Float, default=0.1)
    comment_probability = Column(Float, default=0.3)
    
    # Time behavior (seconds)
    min_response_delay = Column(Integer, default=5)
    max_response_delay = Column(Integer, default=300)
    
    # Relationships
    bot = relationship("Bot", back_populates="profile")

class BotInteractionLog(Base):
    __tablename__ = "bot_interaction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    action_type = Column(String, nullable=False)  # "like", "dislike", "comment"
    relevance_score = Column(Float)  # How relevant was the post to bot's interests
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    bot = relationship("Bot", back_populates="interaction_logs")
