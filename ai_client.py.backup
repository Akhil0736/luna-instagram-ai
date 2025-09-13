import httpx
import asyncio
import os
import logging
from sml_classifier import luna_classifier

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_api_key_here")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def call_openrouter_model(model: str, messages: list, 
                               max_tokens: int = 1024, 
                               temperature: float = 0.7) -> dict:
    """
    Enhanced OpenRouter API call with better error handling
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://luna-ai.com",
        "X-Title": "Luna Instagram AI"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            
            if response.status_code == 401:
                raise Exception("🚫 Unauthorized: Invalid or missing OpenRouter API key. Please check your environment variable.")
            elif response.status_code == 402:
                raise Exception("💳 Payment Required: OpenRouter credits exhausted. Please add credits to your account.")
            
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenRouter API HTTP error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"OpenRouter API failed with status {e.response.status_code}")
    except Exception as e:
        logger.error(f"OpenRouter request failed: {e}")
        raise

def detect_query_type(query: str) -> str:
    """
    SML-powered query classification
    Ultra-fast classification with intelligent caching
    """
    try:
        return luna_classifier.classify_query_intent(query)
    except Exception as e:
        logger.warning(f"SML classification failed, using fallback: {e}")
        # Fallback to simple rule-based classification
        query_lower = query.lower()
        if any(word in query_lower for word in ["hi", "hello", "thanks", "thank you"]):
            return "simple_chat"
        elif any(word in query_lower for word in ["algorithm", "trend", "latest", "research"]):
            return "instagram_research"
        elif any(word in query_lower for word in ["competitor", "analyze", "compare"]):
            return "competitor_analysis"
        elif any(word in query_lower for word in ["code", "script", "automation", "bot"]):
            return "coding"
        else:
            return "general"

def select_luna_model(query: str, query_type: str) -> str:
    """
    Enhanced model selection using SML recommendations
    """
    try:
        # Use SML recommendations if available
        model_name, _ = luna_classifier.get_model_recommendation(query_type)
        return model_name
    except Exception as e:
        logger.warning(f"SML model selection failed, using fallback: {e}")
        # Fallback model mapping
        model_map = {
            "simple_chat": "microsoft/phi-3-mini-4k-instruct",
            "instagram_research": "moonshot/kimi-k2",
            "competitor_analysis": "moonshot/kimi-k2",
            "coding": "deepseek/deepseek-r1",
            "general": "moonshot/kimi"
        }
        return model_map.get(query_type, "moonshot/kimi")

def get_smart_ttl(query_type: str) -> int:
    """
    Get smart TTL based on SML classification
    """
    try:
        _, ttl = luna_classifier.get_model_recommendation(query_type)
        return ttl
    except Exception as e:
        logger.warning(f"SML TTL calculation failed, using fallback: {e}")
        # Fallback TTL mapping
        ttl_map = {
            "simple_chat": 86400,        # 24 hours
            "instagram_research": 600,   # 10 minutes
            "competitor_analysis": 1800, # 30 minutes
            "coding": 43200,             # 12 hours
            "general": 3600              # 1 hour
        }
        return ttl_map.get(query_type, 3600)

async def call_parallel_ai(query: str) -> str:
    """Call Parallel.ai for research (placeholder implementation)"""
    await asyncio.sleep(0.1)  # Simulate API call
    return f"Research context for: {query}"

# Backward compatibility
def detect_query_type_sml(query: str) -> str:
    return detect_query_type(query)

def select_luna_model_sml(query: str, query_type: str) -> str:
    return select_luna_model(query, query_type)
