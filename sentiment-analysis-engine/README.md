# Universal Sentiment Analysis Engine

## Overview

This is a platform-independent sentiment analysis service that can analyze data from **any social media platform or data source** through standardized REST APIs. The system is completely decoupled from data sources and operates as an independent microservice.

## Key Features

- ✅ **Platform-Independent**: Works with any API that provides text data
- ✅ **API-Driven Architecture**: Fetches data via REST APIs
- ✅ **NLP Processing Pipeline**: Text cleaning, tokenization, lemmatization
- ✅ **Machine Learning**: TF-IDF + Logistic Regression
- ✅ **Data Quality Validation**: Ensures sufficient and quality data
- ✅ **Confidence Scoring**: Provides reliability metrics
- ✅ **Explainable AI**: Feature importance analysis

## Technology Stack

- **Framework**: FastAPI
- **NLP**: NLTK, scikit-learn
- **ML Model**: Logistic Regression with TF-IDF vectorization
- **Data Processing**: Pandas, NumPy

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Download NLTK Data

The preprocessing module will automatically download required NLTK data on first run, or you can manually download:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 3. Train the Model

Before using the sentiment analysis service, you need to train the model:

```bash
python train_model.py
```

This will create a basic sentiment model using sample data. The model files will be saved in the `models/` directory.

For production use, train with your own labeled dataset using the `/train` API endpoint.

### 4. Run the Service

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at: http://localhost:8001

API Documentation: http://localhost:8001/docs

## API Endpoints

### 1. Analyze Sentiment from External API

**POST** `/analyze`

Fetch data from any external API and perform sentiment analysis.

```json
{
  "source_api": "http://localhost:8000/public/posts",
  "data_type": "comments",
  "language": "en",
  "date_from": "2024-01-01T00:00:00",
  "date_to": "2024-12-31T23:59:59"
}
```

**Response:**
```json
{
  "status": "success",
  "total_samples": 150,
  "analyzed_samples": 150,
  "sentiment_distribution": {
    "positive": 80,
    "negative": 30,
    "neutral": 40
  },
  "sentiment_percentages": {
    "positive": 53.33,
    "negative": 20.0,
    "neutral": 26.67
  },
  "average_confidence": 0.8542,
  "predictions": [...],
  "data_quality": {...}
}
```

### 2. Analyze Text List

**POST** `/analyze-texts`

Analyze a list of texts directly.

```json
[
  "This is amazing!",
  "I don't like this",
  "It's okay"
]
```

### 3. Train Model

**POST** `/train`

Train the model with your own labeled data.

```json
{
  "texts": ["Great product!", "Terrible experience", "It's alright"],
  "labels": ["positive", "negative", "neutral"]
}
```

### 4. Health Check

**GET** `/health`

Check if the service and model are ready.

### 5. Model Information

**GET** `/model/info`

Get information about the loaded model.

**GET** `/model/features?top_n=20`

Get most important features (words) for each sentiment class.

### 6. Preprocess Text

**POST** `/preprocess`

Test the NLP preprocessing pipeline.

## Using with Social Media Platform

To analyze data from the social media platform in this project:

```bash
# Example using curl
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "source_api": "http://localhost:8000/public/posts",
    "data_type": "posts",
    "language": "en"
  }'
```

Or using Python:

```python
import requests

response = requests.post(
    "http://localhost:8001/analyze",
    json={
        "source_api": "http://localhost:8000/public/posts",
        "data_type": "posts",
        "language": "en"
    }
)

result = response.json()
print(f"Sentiment Distribution: {result['sentiment_distribution']}")
print(f"Average Confidence: {result['average_confidence']}")
```

## Architecture

### Service-Oriented Design

```
┌─────────────────────────────────────┐
│   Any Social Media Platform / API   │
└────────────────┬────────────────────┘
                 │ HTTP/REST
                 │
┌────────────────▼────────────────────┐
│   Sentiment Analysis Engine         │
│   ┌─────────────────────────────┐   │
│   │  1. Data Ingestion          │   │
│   │  2. Validation              │   │
│   │  3. NLP Preprocessing       │   │
│   │  4. ML Prediction           │   │
│   │  5. Result Aggregation      │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### NLP Pipeline

1. **Text Cleaning**: Remove URLs, mentions, special characters
2. **Tokenization**: Split text into words
3. **Stopword Removal**: Remove common words (keeping negations)
4. **Lemmatization**: Reduce words to base form
5. **TF-IDF Vectorization**: Convert text to numerical features
6. **Classification**: Logistic Regression prediction

### Data Quality Checks

- Minimum sample size validation
- Empty text detection
- Vocabulary diversity analysis
- Confidence thresholding

## Model Details

**Algorithm**: Logistic Regression with balanced class weights

**Features**: TF-IDF vectors (max 5000 features, unigrams + bigrams)

**Classes**: Positive, Negative, Neutral

**Interpretability**: Feature importance available via `/model/features`

## Advantages

1. **Platform Independence**: Works with any API
2. **No Data Storage**: Doesn't store user data
3. **Real-time Analysis**: On-demand processing
4. **Explainable**: Feature importance insights
5. **Scalable**: Stateless microservice design
6. **Flexible**: Easy to retrain with new data

## Project Structure

```
sentiment-analysis-engine/
├── app/
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── data_ingestion.py    # API data fetching
│   │   ├── preprocessing.py     # NLP pipeline
│   │   ├── sentiment_model.py   # ML model
│   │   └── sentiment_service.py # Main orchestrator
│   ├── config.py
│   └── main.py
├── models/                  # Saved ML models
├── train_model.py          # Training script
├── requirements.txt
└── README.md
```

## Future Enhancements

- Deep learning models (BERT, RoBERTa)
- Multi-language support
- Aspect-based sentiment analysis
- Real-time streaming analysis
- Model versioning and A/B testing

## License

MIT License - Feel free to use for academic and commercial purposes.
