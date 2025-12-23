from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .config import settings
from .models.schemas import (
    DataSourceRequest,
    SentimentAnalysisResult,
    TrainingData,
    TrainingResult,
    HealthResponse
)
from .services.sentiment_service import SentimentAnalysisService
from .services.sentiment_model import SentimentModel
from .services.preprocessing import TextPreprocessor

app = FastAPI(
    title="Universal Sentiment Analysis Engine",
    description="Platform-independent sentiment analysis service via API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sentiment_service = SentimentAnalysisService()
model = SentimentModel()
preprocessor = TextPreprocessor()

@app.get("/")
def read_root():
    return {
        "message": "Universal Sentiment Analysis Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "Platform-independent sentiment analysis via API"
    }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check service health and model status"""
    return HealthResponse(
        status="healthy",
        model_loaded=model.is_loaded(),
        vectorizer_loaded=model.vectorizer is not None
    )

@app.post("/analyze", response_model=SentimentAnalysisResult)
async def analyze_sentiment(request: DataSourceRequest):
    """
    Analyze sentiment from any external API.
    
    This endpoint fetches data from the provided API URL and performs
    complete sentiment analysis.
    
    Example request:
    ```json
    {
        "source_api": "http://localhost:8000/public/posts",
        "data_type": "comments",
        "language": "en",
        "date_from": "2024-01-01T00:00:00",
        "date_to": "2024-12-31T23:59:59"
    }
    ```
    """
    try:
        result = sentiment_service.analyze_from_api(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-texts", response_model=SentimentAnalysisResult)
async def analyze_text_list(texts: List[str]):
    """
    Analyze sentiment for a list of texts directly.
    
    Useful for testing or when you already have the text data.
    """
    try:
        result = sentiment_service.analyze_texts(texts)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train", response_model=TrainingResult)
async def train_model(training_data: TrainingData):
    """
    Train the sentiment model with labeled data.
    
    Example request:
    ```json
    {
        "texts": ["This is great!", "I hate this", "It's okay"],
        "labels": ["positive", "negative", "neutral"]
    }
    ```
    """
    try:
        # Preprocess texts
        preprocessed_texts = preprocessor.preprocess_batch(training_data.texts)
        
        # Convert labels to strings
        labels = [label.value for label in training_data.labels]
        
        # Train model
        result = model.train(preprocessed_texts, labels)
        
        return TrainingResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
def get_model_info():
    """Get information about the current model"""
    if not model.is_loaded():
        return {
            "status": "not_loaded",
            "message": "Model not trained yet"
        }
    
    return {
        "status": "loaded",
        "model_type": "Logistic Regression",
        "vectorizer": "TF-IDF",
        "classes": list(model.model.classes_) if model.model else [],
        "message": "Model is ready for predictions"
    }

@app.get("/model/features")
def get_feature_importance(top_n: int = 20):
    """
    Get most important features (words) for each sentiment class.
    Useful for understanding model behavior.
    """
    if not model.is_loaded():
        raise HTTPException(
            status_code=400, 
            detail="Model not loaded. Train the model first."
        )
    
    try:
        features = model.get_feature_importance(top_n=top_n)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/preprocess")
def preprocess_text(texts: List[str]):
    """
    Preprocess texts using the NLP pipeline.
    Useful for debugging and understanding preprocessing steps.
    """
    try:
        preprocessed = preprocessor.preprocess_batch(texts)
        return {
            "original": texts,
            "preprocessed": preprocessed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
