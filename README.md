# Social Media Platform with Sentiment Analysis Engine

## Final Year Project - Complete Implementation

This project demonstrates a modular, service-oriented system consisting of two independent yet compatible subsystems:

1. **Social Media Platform** - A functional social media environment with autonomous bot interaction
2. **Universal Sentiment Analysis Engine** - Platform-independent sentiment analysis via APIs

## 🎯 Project Objectives

- Create a controlled social media environment for data generation
- Implement emotion-driven bot interaction engine
- Build a universal, platform-independent sentiment analysis system
- Demonstrate complete decoupling between data generation and analysis
- Ensure ethical data handling and system scalability

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     SOCIAL MEDIA PLATFORM                      │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │  Frontend  │  │   Backend    │  │  Bot Engine         │   │
│  │  (React)   │◄─┤   (FastAPI)  │◄─┤  (Rule-based)       │   │
│  └────────────┘  └──────┬───────┘  └─────────────────────┘   │
│                         │                                      │
│                  ┌──────▼────────┐                            │
│                  │   PostgreSQL  │                            │
│                  └───────────────┘                            │
└─────────────────────────┬────────────────────────────────────┘
                          │ REST API
                          │ (Public Endpoints)
┌─────────────────────────▼────────────────────────────────────┐
│              SENTIMENT ANALYSIS ENGINE                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ Data         │  │ NLP Pipeline │  │ ML Classifier   │    │
│  │ Ingestion    │─►│ Preprocessing│─►│ (TF-IDF + LR)   │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
└────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 1. Setup Social Media Backend

```bash
cd social-media-platform/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create database
# In PostgreSQL:
# CREATE DATABASE social_media_db;

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run the server
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000

### 2. Setup Frontend

```bash
cd social-media-platform/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 3. Setup Sentiment Analysis Engine

```bash
cd sentiment-analysis-engine

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Train initial model
python train_model.py

# Run the service
uvicorn app.main:app --reload --port 8001
```

Sentiment API will be available at: http://localhost:8001

## 📖 Usage Guide

### Step 1: Create User Account

1. Open http://localhost:3000
2. Click "Register"
3. Create your account
4. Login with credentials

### Step 2: Create Sample Bots

Use the API documentation (http://localhost:8000/docs) or create via Python:

```python
import requests

# Create a positive bot
requests.post("http://localhost:8000/bots/", json={
    "name": "HappyBot",
    "profile": {
        "age_group": "18-25",
        "profession": "student",
        "region": "Global",
        "interests": "technology,music,art",
        "emotional_bias": "positive",
        "like_probability": 0.8,
        "dislike_probability": 0.05,
        "comment_probability": 0.6
    }
})

# Create a negative bot
requests.post("http://localhost:8000/bots/", json={
    "name": "CriticalBot",
    "profile": {
        "age_group": "35-50",
        "profession": "critic",
        "region": "Global",
        "interests": "technology,business",
        "emotional_bias": "negative",
        "like_probability": 0.2,
        "dislike_probability": 0.6,
        "comment_probability": 0.7
    }
})
```

### Step 3: Create Posts

1. Use the frontend to create posts with topics and keywords
2. Bots will automatically interact with posts based on their profiles
3. View likes, dislikes, and comments (including bot-generated ones)

### Step 4: Analyze Sentiment

```python
import requests

# Analyze sentiment from social media platform
response = requests.post("http://localhost:8001/analyze", json={
    "source_api": "http://localhost:8000/public/posts",
    "data_type": "posts",
    "language": "en"
})

result = response.json()
print(f"Status: {result['status']}")
print(f"Total Samples: {result['total_samples']}")
print(f"Sentiment Distribution: {result['sentiment_distribution']}")
print(f"Positive: {result['sentiment_percentages']['positive']}%")
print(f"Negative: {result['sentiment_percentages']['negative']}%")
print(f"Neutral: {result['sentiment_percentages']['neutral']}%")
print(f"Confidence: {result['average_confidence']:.2%}")
```

## 🎨 Key Features

### Social Media Platform

✅ User registration and authentication  
✅ Create text posts with topics and keywords  
✅ Like/Dislike functionality  
✅ Comment system  
✅ Real-time feed updates  
✅ Profile management  
✅ Public API for data access  

### Bot Interaction Engine

✅ Configurable bot personalities  
✅ Demographic parameters (age, profession, region)  
✅ Interest-based content matching  
✅ Emotional bias (positive/neutral/negative)  
✅ Probabilistic behavior  
✅ Realistic time delays  
✅ Interaction logging  

### Sentiment Analysis Engine

✅ Platform-independent API integration  
✅ Data quality validation  
✅ NLP preprocessing pipeline  
✅ TF-IDF feature extraction  
✅ Logistic Regression classification  
✅ Confidence scoring  
✅ Feature importance analysis  
✅ Explainable AI  

## 📊 Bot Behavior System

Bots make decisions using a multi-factor algorithm:

1. **Interest Matching**: Compare post topic/keywords with bot interests
2. **Relevance Scoring**: Calculate how relevant the post is (0.0 - 1.0)
3. **Emotional Bias**: Adjust probabilities based on emotional state
4. **Probabilistic Decision**: Use weighted random selection
5. **Response Generation**: Select appropriate comment from templates
6. **Time Delay**: Simulate realistic human response time

Example Bot Configuration:
```json
{
  "name": "TechEnthusiast",
  "profile": {
    "age_group": "25-35",
    "profession": "engineer",
    "interests": "technology,AI,programming,science",
    "emotional_bias": "positive",
    "like_probability": 0.7,
    "comment_probability": 0.5
  }
}
```

## 🧪 Testing the System

### Test 1: Create Posts with Different Topics

```python
topics = ["technology", "sports", "music", "politics"]
for topic in topics:
    requests.post("http://localhost:8000/posts/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": f"This is a post about {topic}",
            "topic": topic,
            "keywords": topic
        }
    )
```

### Test 2: Trigger Bot Processing

```python
requests.post("http://localhost:8000/bots/process-posts?hours=24")
```

### Test 3: Analyze Sentiment

```python
response = requests.post("http://localhost:8001/analyze", json={
    "source_api": "http://localhost:8000/public/comments"
})
```

## 📁 Project Structure

```
day2/
├── social-media-platform/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── models/          # Database models
│   │   │   ├── routers/         # API endpoints
│   │   │   ├── services/        # Business logic
│   │   │   ├── main.py
│   │   │   └── database.py
│   │   ├── requirements.txt
│   │   └── README.md
│   └── frontend/
│       ├── src/
│       │   ├── components/      # React components
│       │   ├── pages/           # Page components
│       │   ├── services/        # API services
│       │   └── App.jsx
│       ├── package.json
│       └── README.md
│
├── sentiment-analysis-engine/
│   ├── app/
│   │   ├── models/              # Pydantic schemas
│   │   ├── services/            # Core services
│   │   ├── main.py
│   │   └── config.py
│   ├── models/                  # Saved ML models
│   ├── train_model.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md (this file)
```

## 🔬 Technical Implementation Details

### Database Schema

**Users**: id, username, email, hashed_password, bio, created_at  
**Posts**: id, user_id, content, topic, keywords, created_at  
**Comments**: id, post_id, user_id, bot_id, content, created_at  
**Reactions**: id, post_id, user_id, bot_id, is_like, created_at  
**Bots**: id, name, is_active, created_at  
**BotProfiles**: bot_id, interests, emotional_bias, probabilities  
**BotInteractionLogs**: bot_id, post_id, action_type, relevance_score  

### NLP Pipeline

1. Text Cleaning (URLs, mentions, special chars)
2. Tokenization (NLTK word_tokenize)
3. Stopword Removal (preserving negations)
4. Lemmatization (WordNet)
5. TF-IDF Vectorization (5000 features, unigrams+bigrams)

### ML Model

- **Algorithm**: Logistic Regression
- **Features**: TF-IDF vectors
- **Classes**: 3 (positive, negative, neutral)
- **Training**: Balanced class weights
- **Validation**: 80/20 split

## 🎓 Academic Significance

This project demonstrates:

1. **Service-Oriented Architecture (SOA)**
2. **Microservices design principles**
3. **RESTful API design**
4. **Machine Learning integration**
5. **Natural Language Processing**
6. **Autonomous agent systems**
7. **Ethical AI data generation**
8. **Platform-independent design**

## 📈 Applications

- Product sentiment analysis
- Marketing campaign evaluation
- Public opinion research
- Bot behavior simulation
- Sentiment trend analysis
- Customer feedback analysis

## 🔒 Ethical Considerations

- ✅ Controlled data generation environment
- ✅ No real user data collection
- ✅ Transparent bot identification
- ✅ Clear separation of human and bot content
- ✅ Privacy-preserving design
- ✅ Explainable AI methods

## 🚀 Future Enhancements

1. **Deep Learning Models**: BERT, RoBERTa for sentiment
2. **Real-time Analysis**: WebSocket streaming
3. **Multi-language Support**: Support for multiple languages
4. **Advanced Bot AI**: Machine learning-based bots
5. **Recommendation System**: Content recommendation engine
6. **Analytics Dashboard**: Visual analytics interface
7. **API Rate Limiting**: Production-ready API management
8. **Deployment**: Docker containers, Kubernetes orchestration

## 📝 API Documentation

### Social Media Platform APIs

- Full documentation: http://localhost:8000/docs
- Public API: http://localhost:8000/public/posts

### Sentiment Analysis APIs

- Full documentation: http://localhost:8001/docs
- Analyze endpoint: POST http://localhost:8001/analyze

## 🤝 Contributing

This is an academic project. For improvements or suggestions, please document your changes clearly.

## 📄 License

MIT License - Free for academic and commercial use.

## 👨‍💻 Author

Created as a final year project demonstrating modern software architecture, NLP, and machine learning integration.

## 📧 Support

For issues or questions:
1. Check the README files in each subsystem
2. Review API documentation at /docs endpoints
3. Check logs for error messages

---

## 🎯 Quick Command Reference

```bash
# Start Social Media Backend
cd social-media-platform/backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Start Frontend
cd social-media-platform/frontend
npm run dev

# Start Sentiment Engine
cd sentiment-analysis-engine
venv\Scripts\activate
python train_model.py  # First time only
uvicorn app.main:app --reload --port 8001
```

**All systems should be running simultaneously for full functionality!**

---

**Project Status**: ✅ Complete and Functional

**Last Updated**: December 2024
