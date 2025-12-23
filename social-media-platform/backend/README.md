# Social Media Platform Backend

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create PostgreSQL database:
```sql
CREATE DATABASE social_media_db;
```

5. Copy `.env.example` to `.env` and update database credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/social_media_db
SECRET_KEY=your-secret-key-here
```

6. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `GET /auth/me` - Get current user info

### Posts
- `POST /posts/` - Create post
- `GET /posts/` - Get all posts (feed)
- `GET /posts/{post_id}` - Get specific post
- `DELETE /posts/{post_id}` - Delete post

### Comments
- `POST /posts/{post_id}/comments` - Add comment
- `GET /posts/{post_id}/comments` - Get comments
- `DELETE /posts/comments/{comment_id}` - Delete comment

### Reactions
- `POST /posts/{post_id}/reactions` - Add/update reaction
- `DELETE /posts/{post_id}/reactions` - Remove reaction

### Bots
- `POST /bots/` - Create bot
- `GET /bots/` - Get all bots
- `GET /bots/{bot_id}` - Get specific bot
- `PATCH /bots/{bot_id}/toggle` - Toggle bot active/inactive
- `DELETE /bots/{bot_id}` - Delete bot
- `POST /bots/process-posts` - Trigger bot processing

### Public API (for Sentiment Analysis)
- `GET /public/posts` - Get posts with comments
- `GET /public/comments` - Get all comments
- `GET /public/stats` - Get platform statistics

## Project Structure
```
backend/
├── app/
│   ├── models/          # Database models
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── schemas.py       # Pydantic schemas
│   └── main.py          # FastAPI app
├── requirements.txt
└── .env
```
