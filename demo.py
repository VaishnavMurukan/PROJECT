"""
Sample script to demonstrate the complete workflow:
1. Create users
2. Create bots
3. Create posts
4. Let bots interact
5. Analyze sentiment
"""

import requests
import time
import json

# API Endpoints
SOCIAL_MEDIA_API = "http://localhost:8000"
SENTIMENT_API = "http://localhost:8001"

def create_user():
    """Create a test user"""
    print("\n1. Creating test user...")
    response = requests.post(f"{SOCIAL_MEDIA_API}/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    
    if response.status_code == 201:
        print("✓ User created successfully")
        
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        login_response = requests.post(f"{SOCIAL_MEDIA_API}/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        print("✓ Logged in successfully")
        return token
    else:
        print(f"Note: User might already exist. Trying to login...")
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        login_response = requests.post(f"{SOCIAL_MEDIA_API}/auth/login", data=login_data)
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✓ Logged in with existing user")
            return token
        return None

def create_sample_bots():
    """Create sample bots with different personalities"""
    print("\n2. Creating sample bots...")
    
    bots = [
        {
            "name": "TechEnthusiast",
            "profile": {
                "age_group": "25-35",
                "profession": "engineer",
                "region": "Global",
                "interests": "technology,AI,programming,innovation",
                "emotional_bias": "positive",
                "like_probability": 0.8,
                "dislike_probability": 0.05,
                "comment_probability": 0.6
            }
        },
        {
            "name": "CriticalThinker",
            "profile": {
                "age_group": "35-50",
                "profession": "analyst",
                "region": "Global",
                "interests": "technology,business,politics",
                "emotional_bias": "negative",
                "like_probability": 0.2,
                "dislike_probability": 0.6,
                "comment_probability": 0.7
            }
        },
        {
            "name": "CasualUser",
            "profile": {
                "age_group": "18-25",
                "profession": "student",
                "region": "Global",
                "interests": "music,sports,entertainment",
                "emotional_bias": "neutral",
                "like_probability": 0.5,
                "dislike_probability": 0.2,
                "comment_probability": 0.4
            }
        }
    ]
    
    for bot in bots:
        response = requests.post(f"{SOCIAL_MEDIA_API}/bots/", json=bot)
        if response.status_code == 201:
            print(f"✓ Created bot: {bot['name']}")
        else:
            print(f"Note: Bot {bot['name']} might already exist")

def create_sample_posts(token):
    """Create sample posts"""
    print("\n3. Creating sample posts...")
    
    posts = [
        {
            "content": "Just launched our new AI-powered feature! The technology behind it is absolutely revolutionary. Can't wait to see how users respond to this innovation!",
            "topic": "technology",
            "keywords": "AI,innovation,technology"
        },
        {
            "content": "The new software update has some serious bugs. Very disappointed with the quality control. This is not acceptable for a professional product.",
            "topic": "technology",
            "keywords": "software,bugs,quality"
        },
        {
            "content": "Attended an interesting tech conference today. Learned about some new developments in machine learning. Overall a decent experience.",
            "topic": "technology",
            "keywords": "conference,machine learning,technology"
        },
        {
            "content": "Music streaming services have completely changed how we consume content. The convenience is amazing and the sound quality keeps improving!",
            "topic": "music",
            "keywords": "music,streaming,entertainment"
        },
        {
            "content": "Latest political debate was absolutely frustrating. No real solutions were discussed, just more empty promises as usual.",
            "topic": "politics",
            "keywords": "politics,debate"
        }
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for post in posts:
        response = requests.post(f"{SOCIAL_MEDIA_API}/posts/", json=post, headers=headers)
        if response.status_code == 201:
            print(f"✓ Created post about: {post['topic']}")
        else:
            print(f"✗ Failed to create post: {response.text}")
    
    print("✓ All posts created")

def trigger_bot_processing():
    """Trigger bot processing for posts"""
    print("\n4. Triggering bot processing...")
    print("Bots are analyzing and interacting with posts...")
    
    response = requests.post(f"{SOCIAL_MEDIA_API}/bots/process-posts?hours=24")
    if response.status_code == 200:
        print("✓ Bot processing completed")
    else:
        print(f"✗ Bot processing failed: {response.text}")

def get_platform_stats():
    """Get platform statistics"""
    print("\n5. Fetching platform statistics...")
    
    response = requests.get(f"{SOCIAL_MEDIA_API}/public/stats")
    if response.status_code == 200:
        stats = response.json()
        print("\nPlatform Statistics:")
        print(f"  Total Posts: {stats['total_posts']}")
        print(f"  Total Comments: {stats['total_comments']}")
        print(f"  Total Reactions: {stats['total_reactions']}")
        print(f"  Total Users: {stats['total_users']}")
        print(f"  Total Bots: {stats['total_bots']}")
        print(f"  Active Bots: {stats['active_bots']}")

def analyze_sentiment():
    """Analyze sentiment using the sentiment engine"""
    print("\n6. Analyzing sentiment...")
    
    # First, check if sentiment model is loaded
    health_response = requests.get(f"{SENTIMENT_API}/health")
    if health_response.status_code == 200:
        health = health_response.json()
        if not health["model_loaded"]:
            print("⚠ Sentiment model not loaded. Please run: python train_model.py")
            return
    
    # Analyze posts and comments
    response = requests.post(f"{SENTIMENT_API}/analyze", json={
        "source_api": f"{SOCIAL_MEDIA_API}/public/posts",
        "data_type": "posts",
        "language": "en"
    })
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "="*60)
        print("SENTIMENT ANALYSIS RESULTS")
        print("="*60)
        print(f"Status: {result['status']}")
        print(f"Total Samples: {result['total_samples']}")
        print(f"Analyzed Samples: {result['analyzed_samples']}")
        print(f"\nSentiment Distribution:")
        for sentiment, count in result['sentiment_distribution'].items():
            percentage = result['sentiment_percentages'][sentiment]
            print(f"  {sentiment.capitalize()}: {count} ({percentage}%)")
        
        print(f"\nAverage Confidence: {result['average_confidence']:.2%}")
        print(f"Data Quality: {result['data_quality']['recommendation']}")
        
        print("\nSample Predictions:")
        for i, pred in enumerate(result['predictions'][:3]):
            print(f"\n  Text: {pred['text'][:80]}...")
            print(f"  Sentiment: {pred['sentiment']}")
            print(f"  Confidence: {pred['confidence']:.2%}")
        
        print("="*60)
    else:
        print(f"✗ Sentiment analysis failed: {response.text}")

def main():
    print("="*60)
    print("SOCIAL MEDIA PLATFORM WITH SENTIMENT ANALYSIS")
    print("Complete Workflow Demonstration")
    print("="*60)
    
    # Step 1: Create user and get token
    token = create_user()
    if not token:
        print("✗ Failed to create/login user. Exiting.")
        return
    
    # Step 2: Create bots
    create_sample_bots()
    
    # Wait a moment
    time.sleep(1)
    
    # Step 3: Create posts
    create_sample_posts(token)
    
    # Step 4: Trigger bot processing
    time.sleep(2)  # Give database time to commit
    trigger_bot_processing()
    
    # Step 5: Get platform stats
    time.sleep(1)
    get_platform_stats()
    
    # Step 6: Analyze sentiment
    time.sleep(1)
    analyze_sentiment()
    
    print("\n" + "="*60)
    print("DEMO COMPLETED!")
    print("="*60)
    print("\nYou can now:")
    print("1. Open http://localhost:3000 to see the frontend")
    print("2. View API docs at http://localhost:8000/docs")
    print("3. View Sentiment API at http://localhost:8001/docs")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to services.")
        print("Please make sure both services are running:")
        print("  - Social Media API: http://localhost:8000")
        print("  - Sentiment API: http://localhost:8001")
    except Exception as e:
        print(f"\n✗ Error: {e}")
