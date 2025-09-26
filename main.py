import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

import logging
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client.core import CollectorRegistry
import time
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from prompts.prompt_manager import LunaPromptManager
from cache_manager_working import WorkingLunaCacheManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Luna Instagram AI", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


luna_prompt_manager = LunaPromptManager()
cache_manager = WorkingLunaCacheManager()


class InstagramQuery(BaseModel):
    query: str
    user_id: Optional[str] = None
    account_context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class LunaResponse(BaseModel):
    response: str
    query_type: str
    confidence: int
    modules_used: List[str]
    citations: List[str]
    session_id: str


@app.on_event("startup")
async def on_startup() -> None:
    await cache_manager.init_redis()
    logger.info("🌙 Luna Prompt Manager ready")


@app.post("/luna/query", response_model=LunaResponse)
async def process_instagram_query(request: InstagramQuery) -> LunaResponse:
    """Main Luna AI endpoint - processes Instagram coaching queries using prompt modules."""

    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        query_analysis = luna_prompt_manager.detect_query_type(request.query)

        user_context = {}
        if request.user_id:
            user_context = luna_prompt_manager.load_user_memory(request.user_id)

        response_data = luna_prompt_manager.orchestrate_response(
            query=request.query,
            context=request.account_context or {},
            user_memory=user_context,
            session_id=request.session_id,
        )

        if request.user_id:
            cache_manager.store_query_response(
                user_id=request.user_id,
                query=request.query,
                response=response_data["response"],
            )

        return LunaResponse(
            response=response_data["response"],
            query_type=query_analysis["type"],
            confidence=query_analysis["confidence"],
            modules_used=response_data.get("modules_used", []),
            citations=response_data.get("citations", []),
            session_id=response_data.get("session_id", ""),
        )

    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - safety net
        logger.exception("Luna query processing error: %s", exc)
        raise HTTPException(status_code=500, detail=f"Processing error: {exc}")


@app.get("/luna/health")
async def luna_health_check() -> Dict[str, Any]:
    """Health check for Luna AI system."""
    return {
        "status": "healthy",
        "prompt_modules": len(luna_prompt_manager.module_catalog),
        "systems": ["prompt_manager", "cache"],
        "version": "2.0.0",
    }


@app.get("/luna/prompt-modules")
async def get_prompt_modules() -> Dict[str, Any]:
    """List all available prompt modules and their capabilities."""
    return luna_prompt_manager.get_module_info()


@app.post("/chat")
async def chat_endpoint(request: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced chat endpoint using Luna AI."""
    query = str(request.get("message", "")).strip()
    if not query:
        raise HTTPException(status_code=400, detail="Chat message cannot be empty")

    luna_request = InstagramQuery(
        query=query,
        user_id=request.get("user_id"),
        account_context=request.get("context", {}),
    )

    luna_response = await process_instagram_query(luna_request)

    return {
        "response": luna_response.response,
        "query_type": luna_response.query_type,
        "confidence": luna_response.confidence,
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "🌙 Luna AI - Prompt-Orchestrated Instagram Coach",
        "version": "2.0.0",
        "endpoints": {
            "luna_query": "/luna/query",
            "luna_health": "/luna/health",
            "prompt_modules": "/luna/prompt-modules",
            "chat": "/chat",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Authentication Endpoints
@app.post("/auth/register")
async def register_user(email: str, password: str, profile_data: Optional[Dict[str, Any]] = None):
    """Register new user"""
    validated_email = input_validator.validate_email(email)
    
    # Basic password validation
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    user_data = auth_manager.register_user(validated_email, password, profile_data)
    return {"message": "User registered successfully", "user_id": user_data["id"]}

@app.post("/auth/login")
async def login_user(email: str, password: str):
    """Authenticate user and return JWT token"""
    validated_email = input_validator.validate_email(email)
    
    user_data = auth_manager.authenticate_user(validated_email, password)
    token_data = auth_manager.create_access_token(user_data)
    
    return {
        "message": "Login successful",
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "business_type": user_data.get("business_type"),
            "niche": user_data.get("niche")
        },
        "access_token": token_data
    }

@app.post("/auth/logout")
async def logout_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user by invalidating tokens"""
    success = auth_manager.logout_user(current_user["user_id"])
    if success:
        return {"message": "Logged out successfully"}
    else:
        raise HTTPException(status_code=500, detail="Logout failed")

@app.get("/auth/me")
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "auth_method": current_user["auth_method"],
        "profile": current_user["user_data"]
    }

@app.post("/auth/api-key")
async def generate_api_key(name: str = "Default API Key", current_user: Dict[str, Any] = Depends(get_current_user)):
    """Generate API key for authenticated user"""
    api_key_data = auth_manager.generate_api_key(current_user["user_id"], name)
    return api_key_data

@app.get("/auth/rate-limits")
async def get_rate_limit_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current rate limit status"""
    user_type = "authenticated_user" if current_user["auth_method"] == "jwt" else "api_key_user"
    status = rate_limiter.get_rate_limit_status(current_user["user_id"], user_type)
    return status

@app.get("/user/analytics")
async def get_user_analytics(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user analytics and insights"""
    analytics = luna_prompt_manager.get_user_analytics(current_user["user_id"])
    return analytics
