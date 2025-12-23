# SETUP INSTRUCTIONS

## Step-by-Step Guide to Run Your Project

### Prerequisites Installation

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - This includes npm

3. **PostgreSQL 12 or higher**
   - Download from: https://www.postgresql.org/download/
   - Remember your postgres password during installation

4. **Git** (optional, for version control)
   - Download from: https://git-scm.com/downloads

---

## Part 1: Database Setup

1. Open **pgAdmin** or **psql** terminal

2. Create the database:
```sql
CREATE DATABASE social_media_db;
```

3. Verify it was created:
```sql
\l  -- Lists all databases
```

---

## Part 2: Social Media Backend Setup

1. Open PowerShell/Terminal in the project directory

2. Navigate to backend:
```powershell
cd social-media-platform\backend
```

3. Create virtual environment:
```powershell
python -m venv venv
```

4. Activate virtual environment:
```powershell
venv\Scripts\activate
```
You should see `(venv)` in your terminal

5. Install dependencies:
```powershell
pip install -r requirements.txt
```

6. Create .env file:
```powershell
cp .env.example .env
```

7. Edit .env file with your details:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/social_media_db
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

8. Start the backend server:
```powershell
uvicorn app.main:app --reload --port 8000
```

✅ Backend should be running at: http://localhost:8000
✅ Check API docs at: http://localhost:8000/docs

**Keep this terminal open!**

---

## Part 3: Frontend Setup

1. Open a **NEW** PowerShell/Terminal window

2. Navigate to frontend:
```powershell
cd social-media-platform\frontend
```

3. Install dependencies:
```powershell
npm install
```
This might take a few minutes...

4. Start development server:
```powershell
npm run dev
```

✅ Frontend should be running at: http://localhost:3000

**Keep this terminal open!**

---

## Part 4: Sentiment Analysis Engine Setup

1. Open a **NEW** PowerShell/Terminal window (third one)

2. Navigate to sentiment engine:
```powershell
cd sentiment-analysis-engine
```

3. Create virtual environment:
```powershell
python -m venv venv
```

4. Activate virtual environment:
```powershell
venv\Scripts\activate
```

5. Install dependencies:
```powershell
pip install -r requirements.txt
```

6. Train the initial model:
```powershell
python train_model.py
```
This will take a minute and download NLTK data...

7. Start the sentiment API:
```powershell
uvicorn app.main:app --reload --port 8001
```

✅ Sentiment API should be running at: http://localhost:8001
✅ Check API docs at: http://localhost:8001/docs

**Keep this terminal open!**

---

## Part 5: Test the System

### Option 1: Use the Demo Script

1. Open a **NEW** PowerShell/Terminal window (fourth one)

2. Make sure you're in the main project directory:
```powershell
cd day2
```

3. Run the demo script:
```powershell
python demo.py
```

This will:
- Create a test user
- Create sample bots
- Create sample posts
- Let bots interact
- Analyze sentiment

### Option 2: Manual Testing

1. **Open browser**: http://localhost:3000

2. **Register a new account**:
   - Click "Register"
   - Enter username, email, password
   - Click Register

3. **Create a post**:
   - Enter text in "What's on your mind?"
   - Optionally add topic and keywords
   - Click "Post"

4. **Create bots** using API docs:
   - Go to: http://localhost:8000/docs
   - Find "POST /bots/"
   - Click "Try it out"
   - Use this example:
   ```json
   {
     "name": "HappyBot",
     "profile": {
       "interests": "technology,music",
       "emotional_bias": "positive",
       "like_probability": 0.8,
       "comment_probability": 0.6
     }
   }
   ```
   - Click "Execute"

5. **Trigger bot processing**:
   - In API docs: POST /bots/process-posts
   - Click "Try it out" and "Execute"

6. **Check sentiment analysis**:
   - Go to: http://localhost:8001/docs
   - Find "POST /analyze"
   - Click "Try it out"
   - Use:
   ```json
   {
     "source_api": "http://localhost:8000/public/posts",
     "data_type": "posts",
     "language": "en"
   }
   ```
   - Click "Execute"
   - See sentiment results!

---

## Summary: What Should Be Running

You should have **4 terminals open**:

1. ✅ **Backend API** - Port 8000
   ```
   social-media-platform\backend> uvicorn app.main:app --reload --port 8000
   ```

2. ✅ **Frontend** - Port 3000
   ```
   social-media-platform\frontend> npm run dev
   ```

3. ✅ **Sentiment API** - Port 8001
   ```
   sentiment-analysis-engine> uvicorn app.main:app --reload --port 8001
   ```

4. ✅ **Demo/Testing** (optional)
   ```
   day2> python demo.py
   ```

---

## Troubleshooting

### Error: "Module not found"
```powershell
# Make sure virtual environment is activated
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Port already in use"
```powershell
# Change the port number
uvicorn app.main:app --reload --port 8002
```

### Error: "Cannot connect to database"
- Check PostgreSQL is running
- Verify credentials in .env file
- Check database exists: `psql -U postgres -l`

### Error: "NLTK data not found"
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Frontend not loading
```powershell
# Clear node_modules and reinstall
rm -r node_modules
npm install
```

---

## Quick Start Commands (After Initial Setup)

When you want to run the project again:

**Terminal 1 - Backend:**
```powershell
cd social-media-platform\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd social-media-platform\frontend
npm run dev
```

**Terminal 3 - Sentiment:**
```powershell
cd sentiment-analysis-engine
venv\Scripts\activate
uvicorn app.main:app --reload --port 8001
```

---

## Important URLs

- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📊 Backend Docs: http://localhost:8000/docs
- 🧠 Sentiment API: http://localhost:8001
- 📖 Sentiment Docs: http://localhost:8001/docs

---

## Next Steps

1. ✅ Create user accounts
2. ✅ Create multiple bots with different personalities
3. ✅ Post content with various topics
4. ✅ Watch bots interact
5. ✅ Analyze sentiment
6. ✅ Experiment with different bot configurations
7. ✅ Test with different types of content

---

## Need Help?

- Check the main README.md for detailed documentation
- Review API documentation at /docs endpoints
- Check individual README files in each folder
- Review error messages in terminal windows

Good luck with your final year project! 🚀
