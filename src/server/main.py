# src/server/main.py - Minimal working version
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Vertex AI Summarizer", version="1.0.0")

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150

class SummarizeResponse(BaseModel):
    original_text: str
    summary: str
    summary_source: str = "mock"

@app.get("/")
async def health_check():
    return {
        "message": "Hello, this API is to showcase Vertex AI based summarization!",
        "project_id": os.getenv("PROJECT_ID", "not set"),
        "location": os.getenv("LOCATION", "not set"),
        "port": os.getenv("PORT", "not set")
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(request: SummarizeRequest):
    """Mock summarize endpoint for testing deployment"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize")
    
    # Mock summary for testing
    mock_summary = f"Mock summary: {request.text[:50]}... (Original length: {len(request.text)} chars)"
    
    return SummarizeResponse(
        original_text=request.text,
        summary=mock_summary,
        summary_source="mock"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)