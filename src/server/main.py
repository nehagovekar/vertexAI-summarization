# src/server/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Load environment variables (only if .env exists)
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY not found, using mock responses")
    client = None
else:
    client = OpenAI(api_key=openai_api_key)

app = FastAPI(title="AI Summarizer", version="1.0.0")

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150

class SummarizeResponse(BaseModel):
    original_text: str
    summary: str
    summary_source: str = "generated"

def summarize_text(text: str, max_length: int = 150) -> str:
    """Use OpenAI to summarize text"""
    
    # Fallback to mock if no API key
    if not client:
        return f"Mock summary: This text discusses various topics and contains {len(text)} characters. Key points would be extracted here in a real implementation."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheap and fast
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
            max_tokens=max_length * 2,  # Rough estimate
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.get("/")
async def health_check():
    """API health check"""
    return {
        "message": "Hello, this API is to showcase AI-powered summarization!",
        "ai_status": "OpenAI" if client else "Mock Mode",
        "status": "Ready"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "ai": "openai" if client else "mock"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(request: SummarizeRequest):
    """Summarize text using OpenAI"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize")
    
    try:
        summary = summarize_text(request.text, request.max_length)
        
        return SummarizeResponse(
            original_text=request.text,
            summary=summary,
            summary_source="openai" if client else "mock"
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
    
    return {
        "document": SAMPLE_DOC,
        "generated_summary": summary,
        "ground_truth_summary": "Northern Ireland boss Michael O'Neill praised scorer Conor Washington as a 1-0 win over Slovenia set a new record of 10 games unbeaten.",
        "summary_source": "openai" if client else "mock"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)