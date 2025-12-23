"""
Script to train the sentiment model with sample data.
This creates a basic model that can be improved with real data.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sentiment_model import SentimentModel
from app.services.preprocessing import TextPreprocessor

# Sample training data
TRAINING_DATA = {
    "positive": [
        "This is amazing! I love it!",
        "Fantastic work, keep it up!",
        "Absolutely wonderful experience!",
        "Great content, very helpful!",
        "Best thing I've seen today!",
        "Love this so much!",
        "Incredible, thank you!",
        "Perfect, exactly what I needed!",
        "Awesome job!",
        "Brilliant idea!",
        "Excellent quality!",
        "So happy with this!",
        "This is exactly what I wanted!",
        "Outstanding performance!",
        "Really impressed!",
        "This made my day!",
        "Wonderful experience!",
        "Top notch quality!",
        "Highly recommended!",
        "Exceeded my expectations!",
    ],
    "negative": [
        "This is terrible, I hate it.",
        "Very disappointing, not good at all.",
        "Waste of time and money.",
        "Awful experience, would not recommend.",
        "This is the worst thing ever.",
        "Completely useless.",
        "I'm very unhappy with this.",
        "Poor quality, not worth it.",
        "Terrible service.",
        "I regret this decision.",
        "Not what I expected at all.",
        "Very frustrating experience.",
        "This is horrible.",
        "Extremely disappointed.",
        "Absolutely terrible quality.",
        "Would not recommend to anyone.",
        "This ruined my day.",
        "Very poor performance.",
        "Total disaster.",
        "Completely unacceptable.",
    ],
    "neutral": [
        "This is okay, nothing special.",
        "It's alright, I guess.",
        "Fair enough, could be better.",
        "It's just okay.",
        "Neither good nor bad.",
        "Average quality.",
        "It works as expected.",
        "Nothing to complain about.",
        "It's fine.",
        "Normal experience.",
        "Standard quality.",
        "As described.",
        "It's acceptable.",
        "Could be better, could be worse.",
        "It does the job.",
        "Pretty standard.",
        "What you'd expect.",
        "Nothing remarkable.",
        "It's there.",
        "Mediocre at best.",
    ]
}

def train_model():
    """Train the sentiment model with sample data"""
    print("Initializing model and preprocessor...")
    model = SentimentModel()
    preprocessor = TextPreprocessor()
    
    # Prepare training data
    texts = []
    labels = []
    
    for sentiment, samples in TRAINING_DATA.items():
        texts.extend(samples)
        labels.extend([sentiment] * len(samples))
    
    print(f"\nTraining with {len(texts)} samples...")
    print(f"  - Positive: {len(TRAINING_DATA['positive'])}")
    print(f"  - Negative: {len(TRAINING_DATA['negative'])}")
    print(f"  - Neutral: {len(TRAINING_DATA['neutral'])}")
    
    # Preprocess texts
    print("\nPreprocessing texts...")
    preprocessed_texts = preprocessor.preprocess_batch(texts)
    
    # Train model
    print("\nTraining model...")
    result = model.train(preprocessed_texts, labels)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print(f"Status: {result['status']}")
    print(f"Accuracy: {result['accuracy']:.2%}")
    print(f"Samples Trained: {result['samples_trained']}")
    print(f"Message: {result['message']}")
    print("="*50)
    
    # Test the model
    print("\nTesting model with sample predictions...")
    test_texts = [
        "I absolutely love this!",
        "This is terrible.",
        "It's okay, I guess."
    ]
    
    preprocessed_test = preprocessor.preprocess_batch(test_texts)
    predictions = model.predict(preprocessed_test)
    
    for i, pred in enumerate(predictions):
        print(f"\nText: {test_texts[i]}")
        print(f"Sentiment: {pred['sentiment']}")
        print(f"Confidence: {pred['confidence']:.2%}")
    
    print("\n✓ Model trained and saved successfully!")
    print("✓ You can now use the sentiment analysis API")

if __name__ == "__main__":
    train_model()
