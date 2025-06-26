# dev/test_vertex_ai.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

def test_vertex_ai():
    """Test Vertex AI connection"""
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION", "us-central1")
    
    print("TESTING VERTEX AI")
    print(f"Project: {project_id}")
    print(f"Location: {location}")
    print(f"Credentials: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    
    if not project_id:
        print("PROJECT_ID not found in .env")
        return False
    
    try:
        print("\n🔄 Initializing Vertex AI...")
        vertexai.init(project=project_id, location=location)
        
        print("Loading model...")
        model = GenerativeModel("gemini-2.5-flash")
        
        print("Testing summarization...")
        test_text = "This is a test to verify Vertex AI is working. We are testing the connection and basic functionality."
        
        response = model.generate_content(f"Summarize this: {test_text}")
        
        print("SUCCESS!")
        print(f"Summary: {response.text}")
        return True
        
    except Exception as e:
        print(f" FAILED: {e}")
        return False

if __name__ == "__main__":
    test_vertex_ai()