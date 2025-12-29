"""
Script to create the 6 personality bots.
"""

import requests

BASE_URL = 'http://localhost:8000'

bots = [
    {
        'name': 'Optimistic_Bot',
        'profile': {
            'age_group': '25-35',
            'profession': 'Life Coach',
            'region': 'Global',
            'interests': 'optimistic,encouraging,positive,motivation,happiness',
            'emotional_bias': 'positive',
            'like_probability': 0.95,
            'dislike_probability': 0.01,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    },
    {
        'name': 'Critical_Bot',
        'profile': {
            'age_group': '40-50',
            'profession': 'Analyst',
            'region': 'Global',
            'interests': 'critical,skeptic,questioning,analysis,doubt',
            'emotional_bias': 'negative',
            'like_probability': 0.15,
            'dislike_probability': 0.60,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    },
    {
        'name': 'Neutral_Bot',
        'profile': {
            'age_group': '30-40',
            'profession': 'Observer',
            'region': 'Global',
            'interests': 'neutral,balanced,objective,fair,impartial',
            'emotional_bias': 'neutral',
            'like_probability': 0.50,
            'dislike_probability': 0.20,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    },
    {
        'name': 'Sarcastic_Bot',
        'profile': {
            'age_group': '22-30',
            'profession': 'Comedian',
            'region': 'Global',
            'interests': 'sarcastic,irony,humor,wit,comedy',
            'emotional_bias': 'neutral',
            'like_probability': 0.40,
            'dislike_probability': 0.30,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    },
    {
        'name': 'Techie_Bot',
        'profile': {
            'age_group': '25-35',
            'profession': 'Software Developer',
            'region': 'Global',
            'interests': 'tech,programming,technology,coding,software',
            'emotional_bias': 'positive',
            'like_probability': 0.70,
            'dislike_probability': 0.10,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    },
    {
        'name': 'Minimal_Bot',
        'profile': {
            'age_group': '20-25',
            'profession': 'Student',
            'region': 'Global',
            'interests': 'minimal,brief,short,concise,simple',
            'emotional_bias': 'neutral',
            'like_probability': 0.60,
            'dislike_probability': 0.15,
            'comment_probability': 1.0,
            'min_response_delay': 1,
            'max_response_delay': 5
        }
    }
]

if __name__ == "__main__":
    print("Creating personality bots...")
    for bot in bots:
        response = requests.post(f'{BASE_URL}/bots/', json=bot)
        if response.status_code == 201:
            print(f"✓ Created bot: {bot['name']}")
        else:
            print(f"✗ Failed {bot['name']}: {response.status_code} - {response.text}")
    
    print("\nVerifying bots...")
    response = requests.get(f'{BASE_URL}/bots/')
    if response.status_code == 200:
        bots_list = response.json()
        print(f"Total bots: {len(bots_list)}")
        for b in bots_list:
            print(f"  - {b['name']} (active: {b['is_active']})")
