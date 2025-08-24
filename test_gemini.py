import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test the Gemini API connection"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with: GEMINI_API_KEY=your_actual_api_key")
        return False
    
    try:
        print(f"🔑 API Key found: {api_key[:10]}...{api_key[-4:]}")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple message
        response = model.generate_content("Hello, this is a test message")
        
        print("✅ SUCCESS: Gemini API connection working!")
        print(f"Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Gemini API connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_connection()
