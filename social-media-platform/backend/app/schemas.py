from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

# Enums
class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class EmotionalBias(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Post Schemas
class MediaCreate(BaseModel):
    media_type: MediaType
    url: str

class MediaResponse(MediaCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    content: str
    topic: Optional[str] = None
    keywords: Optional[str] = None
    media: Optional[List[MediaCreate]] = []

class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    topic: Optional[str]
    keywords: Optional[str]
    created_at: datetime
    user: User
    media: List[MediaResponse]
    like_count: int = 0
    dislike_count: int = 0
    comment_count: int = 0
    
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        # Ensure timezone-aware datetime for proper client-side handling
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    
    class Config:
        from_attributes = True

# Comment Schemas
class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: Optional[int]
    bot_id: Optional[int]
    content: str
    created_at: datetime
    author_name: str  # Username or bot name
    is_bot: bool
    
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        # Ensure timezone-aware datetime for proper client-side handling
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    
    class Config:
        from_attributes = True

# Reaction Schemas
class ReactionCreate(BaseModel):
    is_like: bool

class ReactionResponse(BaseModel):
    id: int
    post_id: int
    is_like: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bot Schemas
class BotProfileCreate(BaseModel):
    age_group: Optional[str] = "18-35"
    profession: Optional[str] = "general"
    region: Optional[str] = "Global"
    interests: str  # Comma-separated
    emotional_bias: EmotionalBias = EmotionalBias.NEUTRAL
    like_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    dislike_probability: float = Field(default=0.1, ge=0.0, le=1.0)
    comment_probability: float = Field(default=0.3, ge=0.0, le=1.0)
    min_response_delay: int = Field(default=5, ge=1)
    max_response_delay: int = Field(default=300, ge=1)

class BotCreate(BaseModel):
    name: str
    profile: BotProfileCreate

class BotProfileResponse(BotProfileCreate):
    id: int
    bot_id: int
    
    class Config:
        from_attributes = True

class BotResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    profile: Optional[BotProfileResponse]
    
    class Config:
        from_attributes = True

# Public API Schemas (for Sentiment Analysis)
class PublicComment(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_bot: bool

class PublicPost(BaseModel):
    id: int
    content: str
    topic: Optional[str]
    created_at: datetime
    likes: int
    dislikes: int
    comments: List[PublicComment]
