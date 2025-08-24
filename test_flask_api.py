import requests
import json

def test_chat_api():
    """Test the Flask chat API endpoint"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"message": "test message"})
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('status')}")
            print(f"AI Response: {data.get('response', 'No response')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to Flask server. Make sure the app is running.")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_chat_api()
