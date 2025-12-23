import os
import joblib
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from ..config import settings
from ..models.schemas import SentimentLabel

class SentimentModel:
    """
    Machine Learning model for sentiment analysis.
    Uses TF-IDF vectorization and Logistic Regression for classification.
    """
    
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.label_mapping = {
            'positive': SentimentLabel.POSITIVE,
            'negative': SentimentLabel.NEGATIVE,
            'neutral': SentimentLabel.NEUTRAL
        }
        self.load_model()
    
    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """
        Train the sentiment model with provided data.
        
        Args:
            texts: List of preprocessed text samples
            labels: List of sentiment labels (positive, negative, neutral)
        
        Returns:
            Dictionary with training results
        """
        if len(texts) != len(labels):
            raise ValueError("Number of texts and labels must match")
        
        if len(texts) < 10:
            raise ValueError("Need at least 10 samples for training")
        
        # Split data for training and validation
        X_train, X_val, y_train, y_val = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Create and train TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.8  # Ignore terms that appear in more than 80% of documents
        )
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_val_vec = self.vectorizer.transform(X_val)
        
        # Train Logistic Regression model
        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced classes
        )
        
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate on validation set
        y_pred = self.model.predict(X_val_vec)
        accuracy = accuracy_score(y_val, y_pred)
        
        # Save the model
        self.save_model()
        
        return {
            "status": "success",
            "accuracy": round(accuracy, 4),
            "samples_trained": len(texts),
            "train_samples": len(X_train),
            "validation_samples": len(X_val),
            "message": f"Model trained successfully with {accuracy:.2%} accuracy"
        }
    
    def predict(self, texts: List[str]) -> List[Dict]:
        """
        Predict sentiment for a list of texts.
        
        Returns:
            List of predictions with sentiment label, confidence, and probabilities
        """
        if self.model is None or self.vectorizer is None:
            raise Exception("Model not loaded. Please train or load a model first.")
        
        if not texts:
            return []
        
        # Vectorize texts
        X = self.vectorizer.transform(texts)
        
        # Get predictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        results = []
        for i, text in enumerate(texts):
            pred_label = predictions[i]
            probs = probabilities[i]
            
            # Get confidence (max probability)
            confidence = float(np.max(probs))
            
            # Create probability dictionary
            prob_dict = {}
            for label, prob in zip(self.model.classes_, probs):
                prob_dict[label] = round(float(prob), 4)
            
            results.append({
                "text": text,
                "sentiment": self.label_mapping.get(pred_label, SentimentLabel.NEUTRAL),
                "confidence": round(confidence, 4),
                "probabilities": prob_dict
            })
        
        return results
    
    def predict_single(self, text: str) -> Dict:
        """Predict sentiment for a single text"""
        results = self.predict([text])
        return results[0] if results else None
    
    def save_model(self):
        """Save model and vectorizer to disk"""
        os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
        
        if self.model:
            joblib.dump(self.model, settings.MODEL_PATH)
        
        if self.vectorizer:
            joblib.dump(self.vectorizer, settings.VECTORIZER_PATH)
    
    def load_model(self):
        """Load model and vectorizer from disk"""
        try:
            if os.path.exists(settings.MODEL_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
            
            if os.path.exists(settings.VECTORIZER_PATH):
                self.vectorizer = joblib.load(settings.VECTORIZER_PATH)
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None and self.vectorizer is not None
    
    def get_feature_importance(self, top_n: int = 20) -> Dict[str, List[Tuple[str, float]]]:
        """
        Get most important features (words) for each sentiment class.
        Useful for model interpretability.
        """
        if not self.is_loaded():
            return {}
        
        feature_names = self.vectorizer.get_feature_names_out()
        importance = {}
        
        for idx, class_name in enumerate(self.model.classes_):
            # Get coefficients for this class
            coef = self.model.coef_[idx]
            
            # Get top positive and negative features
            top_positive_idx = np.argsort(coef)[-top_n:][::-1]
            top_negative_idx = np.argsort(coef)[:top_n]
            
            importance[class_name] = {
                "positive_features": [
                    (feature_names[i], float(coef[i])) 
                    for i in top_positive_idx
                ],
                "negative_features": [
                    (feature_names[i], float(coef[i])) 
                    for i in top_negative_idx
                ]
            }
        
        return importance
