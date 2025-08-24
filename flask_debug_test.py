from app import app, chat_with_fitness_ai
import os

def test_flask_environment():
    """Test the Flask app environment specifically"""
    print("=== Testing Flask Environment ===")
    
    # Test environment variables
    with app.app_context():
        api_key = os.getenv("GEMINI_API_KEY")
        print(f"Flask API Key: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
        
        # Test the function directly
        print("Testing chat_with_fitness_ai function...")
        result = chat_with_fitness_ai("test message")
        print(f"Function result: {result}")
        
        return result

if __name__ == "__main__":
    test_flask_environment()
