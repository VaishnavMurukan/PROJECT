"""
Script to create sample bots with various personalities.
Run this after the backend is started to populate the system with bots.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

SAMPLE_BOTS = [
    {
        "name": "TechEnthusiast",
        "profile": {
            "age_group": "25-35",
            "profession": "software engineer",
            "region": "Global",
            "interests": "technology,AI,programming,innovation,software,coding",
            "emotional_bias": "positive",
            "like_probability": 0.85,
            "dislike_probability": 0.03,
            "comment_probability": 0.65,
            "min_response_delay": 3,
            "max_response_delay": 30
        }
    },
    {
        "name": "CriticalAnalyst",
        "profile": {
            "age_group": "35-50",
            "profession": "business analyst",
            "region": "North America",
            "interests": "business,technology,finance,strategy",
            "emotional_bias": "negative",
            "like_probability": 0.15,
            "dislike_probability": 0.65,
            "comment_probability": 0.75,
            "min_response_delay": 10,
            "max_response_delay": 120
        }
    },
    {
        "name": "CasualBrowser",
        "profile": {
            "age_group": "18-25",
            "profession": "student",
            "region": "Global",
            "interests": "music,movies,entertainment,sports,games",
            "emotional_bias": "neutral",
            "like_probability": 0.45,
            "dislike_probability": 0.15,
            "comment_probability": 0.35,
            "min_response_delay": 5,
            "max_response_delay": 60
        }
    },
    {
        "name": "PositivePaul",
        "profile": {
            "age_group": "30-40",
            "profession": "marketing manager",
            "region": "Europe",
            "interests": "marketing,business,innovation,creativity",
            "emotional_bias": "positive",
            "like_probability": 0.90,
            "dislike_probability": 0.01,
            "comment_probability": 0.70,
            "min_response_delay": 2,
            "max_response_delay": 20
        }
    },
    {
        "name": "SkepticalSam",
        "profile": {
            "age_group": "40-55",
            "profession": "journalist",
            "region": "Global",
            "interests": "news,politics,current events,investigation",
            "emotional_bias": "negative",
            "like_probability": 0.20,
            "dislike_probability": 0.55,
            "comment_probability": 0.80,
            "min_response_delay": 15,
            "max_response_delay": 180
        }
    },
    {
        "name": "ArtLover",
        "profile": {
            "age_group": "22-32",
            "profession": "graphic designer",
            "region": "Global",
            "interests": "art,design,creativity,music,culture",
            "emotional_bias": "positive",
            "like_probability": 0.75,
            "dislike_probability": 0.10,
            "comment_probability": 0.60,
            "min_response_delay": 5,
            "max_response_delay": 45
        }
    },
    {
        "name": "SportssFanatic",
        "profile": {
            "age_group": "20-30",
            "profession": "fitness trainer",
            "region": "North America",
            "interests": "sports,fitness,health,competition,teams",
            "emotional_bias": "positive",
            "like_probability": 0.80,
            "dislike_probability": 0.15,
            "comment_probability": 0.55,
            "min_response_delay": 3,
            "max_response_delay": 40
        }
    },
    {
        "name": "NeutralNancy",
        "profile": {
            "age_group": "28-38",
            "profession": "researcher",
            "region": "Asia",
            "interests": "science,research,technology,education",
            "emotional_bias": "neutral",
            "like_probability": 0.50,
            "dislike_probability": 0.20,
            "comment_probability": 0.45,
            "min_response_delay": 8,
            "max_response_delay": 90
        }
    },
    {
        "name": "GamerGeek",
        "profile": {
            "age_group": "18-28",
            "profession": "game developer",
            "region": "Global",
            "interests": "gaming,technology,esports,streaming,programming",
            "emotional_bias": "positive",
            "like_probability": 0.70,
            "dislike_probability": 0.08,
            "comment_probability": 0.60,
            "min_response_delay": 2,
            "max_response_delay": 25
        }
    },
    {
        "name": "PoliticalDebater",
        "profile": {
            "age_group": "35-50",
            "profession": "political scientist",
            "region": "Europe",
            "interests": "politics,government,policy,debate,law",
            "emotional_bias": "negative",
            "like_probability": 0.25,
            "dislike_probability": 0.60,
            "comment_probability": 0.85,
            "min_response_delay": 20,
            "max_response_delay": 200
        }
    }
]

def create_bots():
    """Create all sample bots"""
    print("="*60)
    print("CREATING SAMPLE BOTS")
    print("="*60)
    
    created = 0
    exists = 0
    failed = 0
    
    for bot in SAMPLE_BOTS:
        try:
            response = requests.post(f"{BASE_URL}/bots/", json=bot, timeout=10)
            
            if response.status_code == 201:
                print(f"✅ Created: {bot['name']}")
                print(f"   Interests: {bot['profile']['interests'][:50]}...")
                print(f"   Bias: {bot['profile']['emotional_bias']}")
                created += 1
            elif response.status_code == 400 and "already exists" in response.text.lower():
                print(f"⚠️  Exists: {bot['name']}")
                exists += 1
            else:
                print(f"❌ Failed: {bot['name']} - {response.text}")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {BASE_URL}")
            print("   Make sure the backend is running!")
            return
        except Exception as e:
            print(f"❌ Error creating {bot['name']}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Created: {created}")
    print(f"⚠️  Already Existed: {exists}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total Bots: {created + exists}")
    print("="*60)
    
    if created + exists > 0:
        print("\n✨ Bots are ready to interact with posts!")
        print("\nNext steps:")
        print("1. Create some posts in the frontend (http://localhost:3000)")
        print("2. Or use the API to create posts")
        print("3. Trigger bot processing: POST http://localhost:8000/bots/process-posts")
        print("4. Watch bots interact with your content!")

def list_bots():
    """List all existing bots"""
    try:
        response = requests.get(f"{BASE_URL}/bots/", timeout=10)
        if response.status_code == 200:
            bots = response.json()
            print(f"\n📋 Existing Bots ({len(bots)}):")
            for bot in bots:
                status = "🟢 Active" if bot.get('is_active') else "🔴 Inactive"
                print(f"  {status} {bot['name']}")
        else:
            print("Could not fetch bots list")
    except Exception as e:
        print(f"Error listing bots: {e}")

def main():
    print("\n🤖 Bot Creator Script")
    print("This will create 10 diverse bots with different personalities\n")
    
    # First, list existing bots
    list_bots()
    
    # Ask for confirmation
    choice = input("\nCreate sample bots? (y/n): ").lower()
    
    if choice == 'y':
        create_bots()
    else:
        print("Cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
