from typing import List, Dict
from ..models.schemas import (
    DataSourceRequest, 
    SentimentAnalysisResult, 
    SentimentPrediction,
    TextData
)
from ..config import settings
from .data_ingestion import DataIngestionService
from .preprocessing import TextPreprocessor
from .sentiment_model import SentimentModel

class SentimentAnalysisService:
    """
    Main service orchestrating the sentiment analysis pipeline.
    This service is completely independent and platform-agnostic.
    """
    
    def __init__(self):
        self.ingestion_service = DataIngestionService()
        self.preprocessor = TextPreprocessor()
        self.model = SentimentModel()
    
    def analyze_from_api(self, request: DataSourceRequest) -> SentimentAnalysisResult:
        """
        Complete sentiment analysis pipeline from external API.
        
        Steps:
        1. Fetch data from API
        2. Validate data sufficiency
        3. Preprocess texts
        4. Predict sentiments
        5. Aggregate results
        6. Evaluate confidence
        """
        
        # Step 1: Fetch data
        try:
            raw_data = self.ingestion_service.fetch_from_api(request)
        except Exception as e:
            return SentimentAnalysisResult(
                status="error",
                total_samples=0,
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality={},
                message=f"Failed to fetch data: {str(e)}"
            )
        
        # Step 2: Validate data sufficiency
        quality_check = self.ingestion_service.validate_data_sufficiency(
            raw_data, 
            min_samples=settings.MIN_SAMPLES_FOR_ANALYSIS
        )
        
        if not quality_check["sufficient"]:
            return SentimentAnalysisResult(
                status="insufficient_data",
                total_samples=quality_check.get("total_samples", 0),
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality=quality_check,
                message=quality_check["reason"] + ". " + quality_check["recommendation"]
            )
        
        # Step 3: Preprocess texts
        texts = [item.text for item in raw_data if item.text.strip()]
        preprocessed_texts = self.preprocessor.preprocess_batch(texts)
        
        # Step 4: Check if model is loaded
        if not self.model.is_loaded():
            return SentimentAnalysisResult(
                status="error",
                total_samples=len(texts),
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality=quality_check,
                message="Sentiment model not loaded. Please train the model first."
            )
        
        # Step 5: Predict sentiments
        predictions = self.model.predict(preprocessed_texts)
        
        # Step 6: Aggregate results
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        total_confidence = 0.0
        
        for pred in predictions:
            sentiment_counts[pred["sentiment"]] += 1
            total_confidence += pred["confidence"]
        
        total_analyzed = len(predictions)
        avg_confidence = total_confidence / total_analyzed if total_analyzed > 0 else 0.0
        
        # Calculate percentages
        sentiment_percentages = {
            sentiment: round((count / total_analyzed) * 100, 2)
            for sentiment, count in sentiment_counts.items()
        }
        
        # Create prediction objects
        prediction_objects = [
            SentimentPrediction(**pred) for pred in predictions
        ]
        
        return SentimentAnalysisResult(
            status="success",
            total_samples=len(raw_data),
            analyzed_samples=total_analyzed,
            sentiment_distribution=sentiment_counts,
            sentiment_percentages=sentiment_percentages,
            average_confidence=round(avg_confidence, 4),
            predictions=prediction_objects[:50],  # Limit to first 50 for response size
            data_quality=quality_check,
            message=f"Successfully analyzed {total_analyzed} samples"
        )
    
    def analyze_texts(self, texts: List[str]) -> SentimentAnalysisResult:
        """
        Analyze a list of texts directly (without API fetch).
        Useful for testing or when data is already available.
        """
        if not texts:
            return SentimentAnalysisResult(
                status="error",
                total_samples=0,
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality={},
                message="No texts provided"
            )
        
        # Validate sufficiency
        if len(texts) < settings.MIN_SAMPLES_FOR_ANALYSIS:
            return SentimentAnalysisResult(
                status="insufficient_data",
                total_samples=len(texts),
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality={"sufficient": False},
                message=f"Need at least {settings.MIN_SAMPLES_FOR_ANALYSIS} samples"
            )
        
        # Preprocess
        preprocessed_texts = self.preprocessor.preprocess_batch(texts)
        
        # Check model
        if not self.model.is_loaded():
            return SentimentAnalysisResult(
                status="error",
                total_samples=len(texts),
                analyzed_samples=0,
                sentiment_distribution={},
                sentiment_percentages={},
                average_confidence=0.0,
                predictions=[],
                data_quality={},
                message="Model not loaded"
            )
        
        # Predict
        predictions = self.model.predict(preprocessed_texts)
        
        # Aggregate
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        total_confidence = 0.0
        
        for pred in predictions:
            sentiment_counts[pred["sentiment"]] += 1
            total_confidence += pred["confidence"]
        
        total_analyzed = len(predictions)
        avg_confidence = total_confidence / total_analyzed if total_analyzed > 0 else 0.0
        
        sentiment_percentages = {
            sentiment: round((count / total_analyzed) * 100, 2)
            for sentiment, count in sentiment_counts.items()
        }
        
        prediction_objects = [SentimentPrediction(**pred) for pred in predictions]
        
        return SentimentAnalysisResult(
            status="success",
            total_samples=len(texts),
            analyzed_samples=total_analyzed,
            sentiment_distribution=sentiment_counts,
            sentiment_percentages=sentiment_percentages,
            average_confidence=round(avg_confidence, 4),
            predictions=prediction_objects[:50],
            data_quality={"sufficient": True},
            message=f"Successfully analyzed {total_analyzed} samples"
        )
