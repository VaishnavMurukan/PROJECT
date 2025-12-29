from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class DataSourceRequest(BaseModel):
    source_api: HttpUrl
    data_type: str = Field(default="comments", description="Type of data: posts, comments, reviews")
    language: Optional[str] = Field(default="en", description="Language code")
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    filters: Optional[Dict] = None

class TextData(BaseModel):
    id: int
    text: str
    created_at: Optional[datetime] = None
    metadata: Optional[Dict] = None

class SentimentPrediction(BaseModel):
    text: str
    sentiment: SentimentLabel
    confidence: float
    probabilities: Dict[str, float]

class SentimentAnalysisResult(BaseModel):
    status: str
    total_samples: int
    analyzed_samples: int
    sentiment_distribution: Dict[str, int]
    sentiment_percentages: Dict[str, float]
    average_confidence: float
    predictions: List[SentimentPrediction]
    data_quality: Dict[str, Any]
    message: Optional[str] = None

class TrainingData(BaseModel):
    texts: List[str]
    labels: List[SentimentLabel]

class TrainingResult(BaseModel):
    status: str
    accuracy: float
    samples_trained: int
    message: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    vectorizer_loaded: bool
