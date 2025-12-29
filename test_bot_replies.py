"""
Test script to create a post and verify bot replies.
"""

import requests
import time

BASE_URL = 'http://localhost:8000'

# Login (user should already exist)
login_data = {'username': 'testuser', 'password': 'test123'}
resp = requests.post(f'{BASE_URL}/auth/login', data=login_data)
if resp.status_code == 200:
    token = resp.json()['access_token']
    print('Login successful!')
    
    # Test different types of posts
    test_posts = [
        {
            'content': 'This app makes my life so much easier. Clean UI and super fast performance 🔥',
            'topic': 'review',
            'keywords': 'app,ui,performance'
        }
    ]
    
    headers = {'Authorization': f'Bearer {token}'}
    
    for i, post_data in enumerate(test_posts):
        print(f'\n--- Test Post {i+1} ---')
        print(f'Content: {post_data["content"]}')
        
        resp = requests.post(f'{BASE_URL}/posts/', json=post_data, headers=headers)
        if resp.status_code == 201:
            post = resp.json()
            post_id = post['id']
            
            # Wait a moment for bots to process
            time.sleep(1)
            
            # Get comments for this post
            resp = requests.get(f'{BASE_URL}/posts/{post_id}/comments')
            if resp.status_code == 200:
                comments = resp.json()
                print(f'\n=== Bot Comments ({len(comments)}) ===')
                for c in comments:
                    author = c["author_name"]
                    content = c["content"]
                    print(f'[{author}]: {content}')
        else:
            print(f'Failed to create post: {resp.text}')
else:
    print(f'Login failed: {resp.text}')
