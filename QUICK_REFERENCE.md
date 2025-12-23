# ⚡ QUICK REFERENCE CARD

## 🚀 Starting the System

### Prerequisites Check
```bash
python --version    # Should be 3.8+
node --version      # Should be 16+
psql --version      # Should be 12+
```

### Database Setup (One Time)
```sql
-- In PostgreSQL:
CREATE DATABASE social_media_db;
```

### Start Services (Every Time)

**Terminal 1 - Backend (Port 8000)**
```bash
cd social-media-platform\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend (Port 3000)**
```bash
cd social-media-platform\frontend
npm run dev
```

**Terminal 3 - Sentiment (Port 8001)**
```bash
cd sentiment-analysis-engine
venv\Scripts\activate
uvicorn app.main:app --reload --port 8001
```

---

## 🔗 Important URLs

| Service | URL | Documentation |
|---------|-----|---------------|
| Frontend | http://localhost:3000 | User Interface |
| Backend API | http://localhost:8000 | http://localhost:8000/docs |
| Sentiment API | http://localhost:8001 | http://localhost:8001/docs |

---

## 🤖 Quick Bot Creation

```python
import requests

requests.post("http://localhost:8000/bots/", json={
    "name": "BotName",
    "profile": {
        "interests": "technology,AI",
        "emotional_bias": "positive",  # positive/negative/neutral
        "like_probability": 0.8,        # 0.0 - 1.0
        "comment_probability": 0.6      # 0.0 - 1.0
    }
})
```

Or use the script:
```bash
python create_bots.py
```

---

## 📊 Quick Sentiment Analysis

```python
import requests

response = requests.post("http://localhost:8001/analyze", json={
    "source_api": "http://localhost:8000/public/posts",
    "data_type": "posts",
    "language": "en"
})

print(response.json())
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | Change port: `--port 8002` |
| Module not found | `pip install -r requirements.txt` |
| Cannot connect to DB | Check PostgreSQL is running |
| NLTK error | `python -c "import nltk; nltk.download('all')"` |
| Frontend blank | Check backend is running |

---

## 📝 API Quick Reference

### Authentication
```bash
# Register
POST /auth/register
{
  "username": "user",
  "email": "user@example.com",
  "password": "pass123"
}

# Login
POST /auth/login
Form: username=user&password=pass123

# Get token, then use in headers:
Authorization: Bearer <token>
```

### Posts
```bash
# Create post
POST /posts/
{
  "content": "Post text",
  "topic": "technology",
  "keywords": "AI,ML"
}

# Get feed
GET /posts/

# React to post
POST /posts/{id}/reactions
{"is_like": true}

# Comment on post
POST /posts/{id}/comments
{"content": "Comment text"}
```

### Bots
```bash
# Create bot
POST /bots/
{...}

# List bots
GET /bots/

# Toggle bot active/inactive
PATCH /bots/{id}/toggle

# Trigger processing
POST /bots/process-posts?hours=24
```

### Public API
```bash
# Get posts with comments
GET /public/posts

# Get statistics
GET /public/stats
```

### Sentiment Analysis
```bash
# Analyze from API
POST /analyze
{
  "source_api": "http://localhost:8000/public/posts",
  "data_type": "posts"
}

# Analyze texts
POST /analyze-texts
["text1", "text2", "text3"]

# Train model
POST /train
{
  "texts": ["Great!", "Terrible"],
  "labels": ["positive", "negative"]
}
```

---

## 🎯 Common Tasks

### Create Test Data
```bash
python demo.py
```

### Create Bots
```bash
python create_bots.py
```

### Train Sentiment Model
```bash
cd sentiment-analysis-engine
python train_model.py
```

### Check Service Health
```bash
# Backend
curl http://localhost:8000/health

# Sentiment
curl http://localhost:8001/health
```

---

## 📦 Project Structure

```
day2/
├── social-media-platform/
│   ├── backend/          # FastAPI + PostgreSQL
│   └── frontend/         # React.js
├── sentiment-analysis-engine/  # ML + NLP
├── demo.py              # Full demo
├── create_bots.py       # Bot creator
└── *.md                 # Documentation
```

---

## 🔑 Key Concepts

### Bot Decision Making
1. Calculate relevance (post interests ↔ bot interests)
2. Apply emotional bias modifier
3. Use probability + random selection
4. Generate appropriate response
5. Log interaction

### Sentiment Pipeline
1. Fetch data from API
2. Validate quality
3. Preprocess (clean, tokenize, lemmatize)
4. Vectorize (TF-IDF)
5. Classify (Logistic Regression)
6. Aggregate results

---

## 📚 File Locations

| File | Path | Purpose |
|------|------|---------|
| Backend Main | `backend/app/main.py` | FastAPI app |
| Bot Engine | `backend/app/services/bot_service.py` | Bot logic |
| React App | `frontend/src/App.jsx` | Main UI |
| Sentiment Main | `sentiment-analysis-engine/app/main.py` | Sentiment API |
| ML Model | `sentiment-analysis-engine/app/services/sentiment_model.py` | ML logic |
| NLP Pipeline | `sentiment-analysis-engine/app/services/preprocessing.py` | Text processing |

---

## 🎓 For Presentation

**Demo Order:**
1. Show frontend (login, post, interact)
2. Create bot via API docs
3. Trigger bot processing
4. Show bot interactions
5. Run sentiment analysis
6. Show results and insights

**Key Points:**
- Complete independence (microservices)
- Smart bot system (rule-based)
- Platform-agnostic sentiment analysis
- Production-ready code quality

---

## ⚡ One-Command Setup (After Installation)

Create a `start.bat` file:
```batch
@echo off
start cmd /k "cd social-media-platform\backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"
start cmd /k "cd social-media-platform\frontend && npm run dev"
start cmd /k "cd sentiment-analysis-engine && venv\Scripts\activate && uvicorn app.main:app --reload --port 8001"
```

Then just double-click `start.bat`!

---

## 💡 Quick Tips

- Keep all 3 terminals open
- Check terminal outputs for errors
- Use /docs endpoints for API testing
- Use demo.py for quick testing
- Bots need time to process (5-300 seconds)
- Need 10+ samples for sentiment analysis
- Train model before using sentiment API

---

## 🆘 Emergency Commands

```bash
# Kill process on port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Reinstall everything
pip install -r requirements.txt --force-reinstall
npm install --force

# Reset database
# In PostgreSQL:
DROP DATABASE social_media_db;
CREATE DATABASE social_media_db;
```

---

## ✅ Pre-Presentation Checklist

- [ ] All services start without errors
- [ ] Can create and login user
- [ ] Can create posts
- [ ] Bots are created
- [ ] Bots interact with posts
- [ ] Sentiment analysis returns results
- [ ] Screenshots prepared
- [ ] Understand architecture
- [ ] Can explain bot algorithm
- [ ] Can explain sentiment pipeline

---

**Keep this card handy during development and presentation!** 📌
