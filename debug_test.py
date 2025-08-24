import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_directly():
    """Test Gemini API directly with the same setup as Flask"""
    print("=== Testing Gemini API Directly ===")
    
    # Get the API key you stored in the .env file
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"DEBUG: API Key from env: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
    
    if not api_key:
        print("Error: Gemini API key is not configured in .env file.")
        return False
    
    try:
        # Configure the Gemini library with your key
        genai.configure(api_key=api_key)
        print("DEBUG: Gemini configured successfully")
        
        # Define the AI's persona and instructions (same as in Flask)
        system_prompt = (
            "You are FitAI, a professional, friendly, and encouraging AI fitness coach. "
            "Your expertise includes workout routines, nutrition, injury prevention, and motivation. "
            "Provide safe, clear, and actionable advice. If a question is outside the scope of "
            "fitness, health, or nutrition, you must politely state that you can only answer fitness-related questions. "
            "Keep your responses focused and easy to understand."
        )
        
        # Combine your instructions with the user's actual question
        test_message = "test message"
        full_prompt = f"{system_prompt}\n\nUser's question: {test_message}"
        print(f"DEBUG: Sending prompt: {full_prompt[:100]}...")

        # Call the Gemini model to get a response
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        
        print("DEBUG: Response received successfully")
        print(f"Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Gemini API connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gemini_directly()
