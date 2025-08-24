import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_routes():
    with app.test_client() as client:
        # Test the new AI query route
        response = client.get('/ai_query')
        print(f"AI Query Route Status: {response.status_code}")
        
        # Test the existing AI coach route
        response = client.get('/ai-coach')
        print(f"AI Coach Route Status: {response.status_code}")
        
        # Test the API endpoint
        response = client.post('/api/ai_query', json={'user_prompt': 'test'})
        print(f"API AI Query Status: {response.status_code}")
        print(f"API Response: {response.get_json()}")

if __name__ == '__main__':
    test_routes()
