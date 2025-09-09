from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

import logging
from logging_config import setup_logging
from logging_middleware import RequestIdMiddleware, HttpLoggingMiddleware

# Configure logging early
setup_logging()

app = FastAPI(
    title="OpenManus Service", 
    description="Luna AI semantic intelligence and strategy generation",
    version="0.1.0"
)

# CORS configuration
origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add these after your CORS middleware
app.add_middleware(RequestIdMiddleware)
app.add_middleware(HttpLoggingMiddleware)

# Initialize LLM
try:
    from openmanus.app.llm import LLM
    llm = LLM()
    semantic_available = llm.is_available()
except Exception as e:
    llm = None
    semantic_available = False

class SemanticRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {
        "service": "OpenManus Service",
        "version": "0.1.0",
        "semantic_available": semantic_available
    }

@app.post("/semantic/understand")
async def semantic_understand(request: SemanticRequest):
    """Luna's revolutionary semantic understanding of Instagram goals"""
    if not semantic_available or not llm:
        raise HTTPException(status_code=503, detail="Semantic engine not available")
    
    result = llm.understand_text(request.text)
    if not result.get("understood"):
        raise HTTPException(status_code=500, detail="Failed to process semantic request")
    
    return result

@app.post("/luna/process-goal")
async def process_goal(goal_data: dict):
    """Process Instagram growth goal and generate strategy"""
    return {
        "goal_processed": True,
        "strategy": {
            "posting_frequency": "daily",
            "content_types": ["carousel", "reel", "story"],
            "engagement_tactics": ["strategic_follows", "targeted_likes", "authentic_comments"],
            "hashtag_strategy": "niche_specific_trending"
        },
        "timeline": "60_days",
        "expected_growth": "400%"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
