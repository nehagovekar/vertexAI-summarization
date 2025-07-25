# src/server/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Try to load environment variables safely
try:
    from dotenv import load_dotenv
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    print("Warning: dotenv not available, using environment variables directly")


try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    print(" OpenAI library imported successfully")
except ImportError as e:
    print(f" OpenAI library import failed: {e}")
    OPENAI_AVAILABLE = False
    OpenAI = None

# Initialize OpenAI client with detailed debugging
openai_api_key = os.getenv("OPENAI_API_KEY")
initialization_error = None

if OPENAI_AVAILABLE and openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
        print(f" OpenAI client created with key: {openai_api_key[:15]}...")
        
        # Don't test the client during initialization - just create it
        print(" OpenAI client initialization complete")
        
    except Exception as e:
        print(f" OpenAI client initialization failed: {type(e).__name__}: {e}")
        initialization_error = str(e)
        client = None

app = FastAPI(title="AI Summarizer", version="1.0.0")

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150

class SummarizeResponse(BaseModel):
    original_text: str
    summary: str
    summary_source: str = "generated"

def summarize_text(text: str, max_length: int = 150) -> str:
    """Use OpenAI to summarize text with fallback to mock"""
    
    # Use mock if OpenAI not available
    if not client or not OPENAI_AVAILABLE:
        print(f"Using mock response. Client: {bool(client)}, Available: {OPENAI_AVAILABLE}")
        return f"Mock summary: This text contains {len(text)} characters and discusses various topics. In a real implementation, AI would analyze the content and extract key points to create a meaningful summary of approximately {max_length} words."
    
    try:
        print(f"Attempting OpenAI request for {len(text)} characters...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a helpful assistant that creates concise summaries. Summarize the following text in {max_length} words or less."
                },
                {
                    "role": "user", 
                    "content": text
                }
            ],
            max_tokens=max_length * 2,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        print(f"OpenAI request successful, got {len(result)} characters")
        return result
        
    except Exception as e:
        print(f" OpenAI API error: {type(e).__name__}: {e}")
        # Fallback to mock on any error
        return f"Fallback summary (OpenAI error: {type(e).__name__}): This text contains {len(text)} characters and would normally be summarized to highlight the main points and key information."

@app.get("/")
async def health_check():
    """API health check"""
    ai_status = "openai" if (client and OPENAI_AVAILABLE) else "mock"
    return {
        "message": "Hello, this API is to showcase AI-powered summarization!",
        "ai_status": ai_status,
        "openai_available": OPENAI_AVAILABLE,
        "api_key_configured": bool(openai_api_key),
        "initialization_error": initialization_error,
        "status": "Ready"
    }

@app.get("/health")
async def health():
    ai_mode = "openai" if (client and OPENAI_AVAILABLE) else "mock"
    return {
        "status": "healthy", 
        "ai": ai_mode,
        "openai_library": OPENAI_AVAILABLE,
        "api_key": bool(openai_api_key),
        "client_ready": bool(client),
        "init_error": initialization_error
    }

@app.get("/debug")
async def debug_env():
    return {
        "env_vars": {
            "OPENAI_API_KEY_present": bool(openai_api_key),
            "OPENAI_API_KEY_length": len(openai_api_key) if openai_api_key else 0,
            "OPENAI_API_KEY_prefix": openai_api_key[:15] if openai_api_key else None,
            "PROJECT_ID": os.getenv("PROJECT_ID"),
            "LOCATION": os.getenv("LOCATION")
        },
        "openai_status": {
            "library_available": OPENAI_AVAILABLE,
            "client_initialized": bool(client),
            "initialization_error": initialization_error
        }
    }

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(request: SummarizeRequest):
    """Summarize text using OpenAI or mock"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize")
    
    try:
        summary = summarize_text(request.text, request.max_length)
        source = "openai" if (client and OPENAI_AVAILABLE) else "mock"
        
        return SummarizeResponse(
            original_text=request.text,
            summary=summary,
            summary_source=source
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Sample document for testing
SAMPLE_DOC = """Media playback is not supported on this device
The QPR striker scored on his home debut to boost his hopes of making the squad for the Euro 2016 finals.
"Conor has strength, power and composure - he looks like he is going to be an asset for us," said O'Neill.
"It's a great achievement to go unbeaten in 10 games and now we just want to build on it."
Washington struck his first goal for Northern Ireland before the break, while Roy Carroll kept out Milivoje Novakovic's penalty in the second half."""

@app.get("/summarize/{index}")
async def summarize_by_index(index: int):
    """Get summary of sample document by index"""
    if index != 1:
        raise HTTPException(status_code=404, detail="Document not found")
    
    summary = summarize_text(SAMPLE_DOC)
    source = "openai" if (client and OPENAI_AVAILABLE) else "mock"
    
    return {
        "document": SAMPLE_DOC,
        "generated_summary": summary,
        "ground_truth_summary": "Northern Ireland boss Michael O'Neill praised scorer Conor Washington as a 1-0 win over Slovenia set a new record of 10 games unbeaten.",
        "summary_source": source
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  
     