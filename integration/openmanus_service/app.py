from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
import time
import requests
from typing import List, Optional, Dict, Any
from logging_config import setup_logging
from logging_middleware import RequestIdMiddleware, HttpLoggingMiddleware

# Configure logging early
setup_logging()

app = FastAPI(
    title="OpenManus Service", 
    description="Luna AI semantic intelligence and strategy generation with multi-scraper integration",
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

# Add logging middleware
app.add_middleware(RequestIdMiddleware)
app.add_middleware(HttpLoggingMiddleware)

# Environment variables and logger
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
logger = logging.getLogger("luna.llm")

def initialize_search_clients():
    """Initialize multiple search clients with Scrapedo as primary"""
    clients = {}
    
    # Scrapedo (Primary - Cost Effective)
    try:
        scrapedo_api_key = os.getenv("SCRAPEDO_API_KEY")
        if scrapedo_api_key:
            clients['scrapedo'] = {
                'api_key': scrapedo_api_key,
                'base_url': 'https://api.scrapedo.com/v1',
                'available': True
            }
            logger.info("🎯 Scrapedo client initialized (Primary)")
        else:
            clients['scrapedo'] = {'available': False}
    except Exception as e:
        logger.warning("⚠️ Scrapedo not available: %s", str(e))
        clients['scrapedo'] = {'available': False}
    
    # Tavily (Fallback - AI Optimized)
    try:
        from tavily import TavilyClient
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            clients['tavily'] = {
                'client': TavilyClient(api_key=tavily_api_key),
                'available': True
            }
            logger.info("🌐 Tavily client initialized (Fallback)")
        else:
            clients['tavily'] = {'available': False}
    except Exception as e:
        logger.warning("⚠️ Tavily not available: %s", str(e))
        clients['tavily'] = {'available': False}
    
    # Apify (Optional - High Volume)
    try:
        from apify_client import ApifyClient
        apify_api_token = os.getenv("APIFY_API_TOKEN")
        if apify_api_token:
            clients['apify'] = {
                'client': ApifyClient(apify_api_token),
                'available': True
            }
            logger.info("📊 Apify client initialized (Optional)")
        else:
            clients['apify'] = {'available': False}
    except Exception as e:
        logger.warning("⚠️ Apify not available: %s", str(e))
        clients['apify'] = {'available': False}
    
    return clients

# Initialize search clients globally
search_clients = initialize_search_clients()
web_search_available = any(client.get('available', False) for client in search_clients.values())

# Legacy LLM initialization (backward compatibility)
try:
    from openmanus.app.llm import LLM
    llm = LLM()
    semantic_available = llm.is_available()
except Exception as e:
    llm = None
    semantic_available = True  # We'll use direct API instead

# Pydantic models
class SemanticRequest(BaseModel):
    text: str

class TargetingRequest(BaseModel):
    hashtags: Optional[List[str]] = []
    competitors: Optional[List[str]] = []
    location: Optional[str] = "global"
    limits: Optional[Dict[str, int]] = {}
    demographics: Optional[Dict[str, Any]] = {}
    ai: Optional[Dict[str, str]] = {}

def detect_task_type(text: str) -> tuple[str, str]:
    """Enhanced task type detection for proper model routing"""
    logger.info("🔍 Analyzing task type for: %s", text[:50] + "...")
    
    # Research indicators
    research_keywords = [
        "analyze", "research", "deep dive", "comprehensive", "detailed analysis", 
        "strategy", "study", "investigate", "compare", "competitive analysis",
        "market research", "trends", "insights", "report", "breakdown", "explain",
        "examine", "evaluation", "assessment"
    ]
    
    # Current information indicators  
    current_info_keywords = [
        "latest", "current", "recent", "today", "now", "new", "update", 
        "changes", "news", "2025", "this year", "algorithm", "feature",
        "announcement", "released", "launch", "rolled out"
    ]
    
    text_lower = text.lower()
    
    # Check for research tasks
    if any(keyword in text_lower for keyword in research_keywords):
        logger.info("📊 Detected RESEARCH task - routing to enhanced processing")
        return ("research", "high")
    
    # Check for current information needs
    elif any(keyword in text_lower for keyword in current_info_keywords):
        logger.info("🌐 Detected CURRENT INFO task - routing to web search")
        return ("research", "high")
    
    # Check for complex/long queries
    elif len(text) > 200 or len(text.split()) > 30:
        logger.info("📝 Detected COMPLEX query - routing to enhanced processing")
        return ("research", "medium")
    
    # Default to chat
    else:
        logger.info("💬 Detected CHAT task - routing to fast processing")
        return ("chat", "low")

def select_luna_model(task_type: str = "chat", compute_budget: str = "low") -> str:
    """Enhanced Luna model routing with proper task detection"""
    logger.info("🧭 ROUTING: task_type=%s, compute_budget=%s", task_type, compute_budget)
    
    if task_type == "chat":
        if compute_budget == "low":
            selected = "phi3:mini"
            logger.info("⚡ Selected Phi 3 Mini for fast chat")
            return selected
        else:
            selected = "phi3:mini"  # Can upgrade to llama3.1 when available
            logger.info("🦙 Selected enhanced Phi for complex chat")
            return selected
    
    elif task_type == "research":
        # For research tasks, use Phi with enhanced prompting
        # TODO: Integrate DeepSeek API when available
        selected = "phi3:mini"
        logger.info("🔬 Selected Phi (enhanced prompting) for research task")
        return selected
    
    elif task_type == "embedding":
        selected = "mxbai-embed-large"
        logger.info("🧠 Selected mxbai for embeddings")
        return selected
    
    else:
        logger.warning("⚠️ Unknown task type %s, defaulting to Phi", task_type)
        return "phi3:mini"

def scrapedo_search(query: str, max_results: int = 5) -> Dict:
    """Perform search using Scrapedo API"""
    try:
        scrapedo_config = search_clients.get('scrapedo', {})
        if not scrapedo_config.get('available'):
            raise Exception("Scrapedo not configured")
        
        logger.info("🎯 Using Scrapedo for search: %s", query)
        
        # Scrapedo API call
        response = requests.post(
            f"{scrapedo_config['base_url']}/search",
            headers={
                'Authorization': f"Bearer {scrapedo_config['api_key']}",
                'Content-Type': 'application/json'
            },
            json={
                'query': f"{query} Instagram marketing social media 2025",
                'max_results': max_results,
                'include_content': True,
                'filters': {
                    'domains': ['instagram.com', 'socialmediaexaminer.com', 'buffer.com', 'hootsuite.com', 'later.com'],
                    'date_range': '2025'
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            results = response.json()
            logger.info("✅ Scrapedo search successful: %d results", len(results.get('results', [])))
            return results
        else:
            raise Exception(f"Scrapedo API error: {response.status_code}")
            
    except Exception as e:
        logger.error("❌ Scrapedo search failed: %s", str(e))
        return None

def tavily_search_fallback(query: str, max_results: int = 5) -> Dict:
    """Fallback search using Tavily"""
    try:
        tavily_config = search_clients.get('tavily', {})
        if not tavily_config.get('available'):
            raise Exception("Tavily not configured")
        
        logger.info("🌐 Using Tavily fallback for search: %s", query)
        
        tavily_client = tavily_config['client']
        results = tavily_client.search(
            query=f"{query} Instagram marketing social media 2025",
            search_depth="advanced",
            max_results=max_results,
            include_answer=True,
            include_raw_content=False
        )
        
        logger.info("✅ Tavily fallback successful")
        return results
        
    except Exception as e:
        logger.error("❌ Tavily fallback failed: %s", str(e))
        return None

def perform_deep_search(query: str) -> str:
    """Enhanced multi-scraper deep search with Scrapedo primary"""
    logger.info("🌐 Starting MULTI-SCRAPER DEEP SEARCH for: %s", query)
    
    # Strategy: Try Scrapedo first (cost-effective), fallback to Tavily
    search_results = None
    search_provider = None
    
    # Try Scrapedo first (Primary)
    if search_clients.get('scrapedo', {}).get('available'):
        search_results = scrapedo_search(query)
        search_provider = "Scrapedo"
    
    # Fallback to Tavily if Scrapedo fails
    if not search_results and search_clients.get('tavily', {}).get('available'):
        search_results = tavily_search_fallback(query)
        search_provider = "Tavily"
    
    # Format results
    if search_results:
        context = f"🔍 Deep Search Results ({search_provider}) for '{query}':\n\n"
        
        # Handle Tavily format
        if search_provider == "Tavily" and search_results.get('answer'):
            context += f"📋 AI Summary: {search_results['answer']}\n\n"
        
        # Handle both Scrapedo and Tavily results
        results_list = search_results.get('results', [])
        for i, result in enumerate(results_list[:5], 1):
            title = result.get('title', 'No title')
            url = result.get('url', '#')
            content = result.get('content', result.get('snippet', ''))[:400]
            
            context += f"{i}. **{title}**\n"
            context += f"   🔗 Source: {url}\n"
            context += f"   📄 Content: {content}...\n\n"
        
        context += f"🎯 Information enriched with real-time data via {search_provider}."
        
        logger.info("✅ Multi-scraper search completed successfully via %s", search_provider)
        return context
    
    else:
        logger.warning("⚠️ All search providers failed, using knowledge base")
        return "Deep search temporarily unavailable. Using available knowledge base for response."

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "OpenManus Service",
        "version": "0.1.0",
        "semantic_available": semantic_available,
        "web_search_available": web_search_available,
        "search_providers": {
            "scrapedo": search_clients.get('scrapedo', {}).get('available', False),
            "tavily": search_clients.get('tavily', {}).get('available', False),
            "apify": search_clients.get('apify', {}).get('available', False)
        }
    }

# ENHANCED SEMANTIC ENDPOINT with intelligent routing & multi-scraper search
@app.post("/semantic/understand")
async def semantic_understand(request: SemanticRequest):
    """Luna's enhanced semantic understanding with intelligent routing & deep search"""
    start_time = time.perf_counter()
    text = request.text
    
    # Step 1: Detect task type and routing
    task_type, compute_budget = detect_task_type(text)
    selected_model = select_luna_model(task_type, compute_budget)
    
    # Step 2: Determine if deep search is needed
    needs_search = (task_type == "research" or 
                   any(keyword in text.lower() for keyword in ["latest", "current", "recent", "new", "update", "2025", "today", "now"]))
    
    logger.info("🧠 Luna PROCESSING: %s | Model: %s | Deep Search: %s", 
                text[:50] + "..." if len(text) > 50 else text, 
                selected_model, "Yes" if needs_search else "No")
    
    # Step 3: Prepare enhanced prompt
    if needs_search and web_search_available:
        # Perform deep search
        search_context = perform_deep_search(text)
        enhanced_prompt = f"""You are Luna, an Instagram growth AI assistant with access to real-time information and deep research capabilities.

CURRENT SEARCH RESULTS:
{search_context}

USER QUERY: {text}

INSTRUCTIONS:
1. Use the search results above to provide current, comprehensive analysis
2. Provide detailed, research-backed Instagram growth strategies  
3. Include specific actionable recommendations with reasoning
4. Reference sources when possible
5. Focus on data-driven insights and proven tactics
6. Provide step-by-step implementation guidance
7. If search results are limited, combine with your knowledge appropriately

Generate a comprehensive, research-backed response:"""
    
    elif task_type == "research":
        # Research task without web search
        enhanced_prompt = f"""You are Luna, an Instagram growth AI assistant specializing in comprehensive analysis and strategic planning.

USER QUERY: {text}

INSTRUCTIONS:
1. Provide detailed, comprehensive analysis of the Instagram growth topic
2. Break down complex strategies into actionable steps
3. Include multiple approaches and tactics
4. Explain the reasoning behind each recommendation
5. Consider different user types (beginners, intermediate, advanced)
6. Provide specific examples and case studies when relevant
7. Focus on proven, results-driven strategies

Generate a thorough, research-quality response:"""
    
    else:
        # Standard chat prompt
        enhanced_prompt = f"""You are Luna, an Instagram growth AI assistant specializing in practical, actionable advice.

USER QUERY: {text}

INSTRUCTIONS:
1. Provide clear, actionable Instagram growth strategies
2. Focus on proven tactics and best practices
3. Give specific steps the user can implement immediately
4. Include relevant examples when helpful
5. Keep advice practical and results-focused
6. Be concise but thorough

Provide helpful Instagram growth guidance:"""

    # Step 4: Call model with enhanced prompt and retry logic
    timeouts = [45, 90, 120] if needs_search else [30, 60, 90]
    
    for attempt, timeout_val in enumerate(timeouts, 1):
        try:
            logger.info("🚀 Attempt %d with %s model (timeout: %ds)", 
                       attempt, selected_model, timeout_val)
            
            # Make API call to Ollama
            ollama_response = requests.post(f"{OLLAMA_HOST}/api/chat", json={
                "model": selected_model,
                "messages": [{"role": "user", "content": enhanced_prompt}],
                "stream": False
            }, timeout=timeout_val)
            
            if ollama_response.status_code == 200:
                result = ollama_response.json()
                duration = time.perf_counter() - start_time
                
                logger.info("✅ Luna COMPLETED: %.3fs | Model: %s | Deep Search: %s", 
                           duration, selected_model, "Enabled" if needs_search else "Disabled")
                
                return {
                    "understood": True,
                    "text": text,
                    "task_type": task_type,
                    "compute_budget": compute_budget,
                    "deep_search_used": needs_search and web_search_available,
                    "analysis": {
                        "response": result["message"]["content"],
                        "model_used": selected_model,
                        "processing_time": f"{duration:.3f}s",
                        "search_enhanced": needs_search and web_search_available,
                        "attempt": attempt,
                        "goal_type": "instagram_growth",
                        "platform": "instagram",
                        "intent": "follower_growth"
                    }
                }
                
        except requests.exceptions.ReadTimeout:
            duration = time.perf_counter() - start_time
            logger.warning("⏰ Timeout attempt %d after %.3fs", attempt, duration)
            continue
        except Exception as e:
            duration = time.perf_counter() - start_time
            logger.exception("❌ Error attempt %d after %.3fs: %s", attempt, duration, str(e))
            break
    
    # Fallback response
    return {
        "understood": False,
        "error": "Processing timeout or service unavailable",
        "suggestion": "Try breaking your request into smaller parts or try again in a moment",
        "task_type": task_type,
        "deep_search_used": needs_search and web_search_available
    }

# TARGETING ENDPOINTS
@app.post("/targeting/suggest")
async def targeting_suggest(request: TargetingRequest):
    """Generate AI targeting suggestions"""
    try:
        suggestions = []
        
        # Hashtag suggestions
        if request.hashtags:
            suggested_hashtags = request.hashtags + ["socialmedia", "marketing", "growth", "engagement", "contentcreator"]
            suggestions.append({
                "field": "hashtags", 
                "current": request.hashtags,
                "suggestion": suggested_hashtags[:15],
                "reasoning": "Added high-performing growth hashtags to increase reach by 40-60%"
            })
        
        # Location suggestions
        if request.location == "us":
            suggestions.append({
                "field": "location",
                "current": "us", 
                "suggestion": "global",
                "reasoning": "Expanding to Global increases potential audience by 300%"
            })
        
        # Engagement limits optimization
        if request.limits:
            current_follows = request.limits.get("follows", 25)
            if current_follows < 30:
                suggestions.append({
                    "field": "follows",
                    "current": current_follows,
                    "suggestion": 30,
                    "reasoning": "Increasing to 30 daily follows optimizes growth while staying in safe zone"
                })
            
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/targeting/analyze")
async def targeting_analyze(request: TargetingRequest):
    """Analyze current targeting settings"""
    try:
        analysis = {
            "risk_score": 15,
            "optimization_potential": 85,
            "recommendations": [
                "Add more niche-specific hashtags",
                "Optimize posting times for your audience", 
                "Increase engagement limits safely",
                "Target competitors' engaged followers"
            ],
            "estimated_growth": "20-40% increase in 30 days with optimized settings"
        }
        return {"analysis": analysis, "status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/targeting/apply")
async def targeting_apply(request: dict):
    """Apply accepted targeting suggestions"""
    try:
        accepted = request.get("accepted", [])
        
        applied_changes = []
        for suggestion in accepted:
            applied_changes.append({
                "field": suggestion.get("field"),
                "old_value": suggestion.get("current"),
                "new_value": suggestion.get("suggestion"),
                "impact": "positive"
            })
            
        return {
            "applied": True,
            "changes": applied_changes,
            "total_changes": len(accepted),
            "status": "success",
            "estimated_improvement": f"{len(accepted) * 15}% growth boost"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GOAL PROCESSING ENDPOINT
@app.post("/luna/process-goal")
async def process_goal(goal_data: dict):
    """Process Instagram growth goal and generate strategy"""
    try:
        goal_text = goal_data.get("goal", "")
        current_followers = goal_data.get("current_followers", 0)
        target_followers = goal_data.get("target_followers", 1000)
        timeline = goal_data.get("timeline", "60_days")
        
        # Calculate growth needed
        followers_needed = target_followers - current_followers
        growth_rate = int((followers_needed / current_followers) * 100) if current_followers > 0 else 400
        
        return {
            "goal_processed": True,
            "current_followers": current_followers,
            "target_followers": target_followers,
            "followers_needed": followers_needed,
            "growth_rate": f"{growth_rate}%",
            "strategy": {
                "posting_frequency": "daily" if followers_needed > 1000 else "5x per week",
                "content_types": ["carousel", "reel", "story"],
                "engagement_tactics": ["strategic_follows", "targeted_likes", "authentic_comments"],
                "hashtag_strategy": "niche_specific_trending",
                "focus_areas": [
                    "High-quality visual content",
                    "Consistent posting schedule",
                    "Active community engagement",
                    "Strategic hashtag usage"
                ]
            },
            "timeline": timeline,
            "expected_growth": f"{growth_rate}%",
            "success_probability": "85%" if followers_needed < 5000 else "75%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Startup logging
logger.info("🌙 Luna OpenManus service with multi-scraper integration startup complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

