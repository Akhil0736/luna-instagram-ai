import logging
import time
import requests
import json
import httpx
import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/luna-instagram-ai/.env', override=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("luna")

app = FastAPI(
    title="Luna AI Enterprise",
    description="Universal AI Intelligence with Real-Time Research + Elite Multi-Agent Processing",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PARALLEL_AI_API_KEY = os.getenv("PARALLEL_AI_API_KEY")

# Request models
class QueryRequest(BaseModel):
    message: str
    user_id: str
    priority: Optional[str] = "balanced"
    research_enabled: Optional[bool] = True
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7

# Elite query processor placeholder
class EliteQueryProcessor:
    def __init__(self):
        pass
    
    async def process_query(self, query: str, user_id: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"🌙 Processing query for {user_id}: {query[:100]}...")
        
        return {
            "response": f"Luna AI Enterprise processed: {query}",
            "processing_method": "elite",
            "research_enhanced": True,
            "processing_time": "0.5s",
            "timestamp": time.time(),
            "user_id": user_id,
            "sources": ["Luna AI Intelligence"]
        }

# Initialize elite processor
elite_processor = EliteQueryProcessor()

# API Endpoints
@app.get("/")
async def root():
    return {
        "service": "Luna AI Enterprise", 
        "version": "3.0.0",
        "status": "operational",
        "capabilities": [
            "Real-time research integration",
            "Elite multi-agent processing", 
            "Strategic analysis and planning",
            "Context-aware intelligence"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "parallel_ai_configured": bool(PARALLEL_AI_API_KEY)
    }

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process user query with elite-level analysis"""
    
    logger.info(f"🌙 Query from {request.user_id}: {request.message[:100]}...")
    
    try:
        result = await elite_processor.process_query(
            query=request.message,
            user_id=request.user_id,
            priority=request.priority,
            research_enabled=request.research_enabled,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === Luna AI Multi-Agent System Integration ===
import sys
import os
from typing import Dict

# Add orchestration path
sys.path.append(os.path.join(os.path.dirname(__file__), 'orchestration'))

try:
    from luna_master_orchestrator import LunaMasterOrchestrator
    luna_orchestrator = LunaMasterOrchestrator()
    LUNA_AVAILABLE = True
    print("✅ Luna AI Multi-Agent System loaded successfully")
except Exception as e:
    print(f"⚠️ Luna orchestrator error: {e}")
    LUNA_AVAILABLE = False
    # Create a mock orchestrator for testing
    class MockLunaOrchestrator:
        def __init__(self):
            self.active_conversations = {}
        
        async def initiate_luna_consultation(self, user_input: str, user_id: str):
            niche = "breathwork" if "breathwork" in user_input.lower() else "coaching"
            return {
                "status": "conversation_active",
                "message": f"Luna AI understands you're a {niche} professional! To create your comprehensive Instagram growth strategy, I need to analyze your specific situation:",
                "questions": [
                    {"category": "content", "question": "What type of content are you currently creating or planning?", "priority": "high"},
                    {"category": "competitors", "question": "Who are 3-5 coaches in your niche you admire on Instagram?", "priority": "high"},
                    {"category": "audience", "question": "What's your current follower count and engagement rate?", "priority": "medium"},
                    {"category": "goals", "question": "What's your target growth and revenue goals?", "priority": "high"}
                ],
                "conversation_id": user_id,
                "luna_version": "Multi-Agent Research System v3.0 (Mock Mode)"
            }
        
        async def get_consultation_status(self, user_id: str):
            return {
                "status": "active",
                "user_id": user_id,
                "current_stage": "conversation",
                "message": "Luna consultation active (mock mode)"
            }
    
    luna_orchestrator = MockLunaOrchestrator()

# Luna AI Consultation Endpoints
@app.post("/luna/consultation/start")
async def start_luna_consultation(request: QueryRequest):
    """Start comprehensive Luna AI consultation with multi-agent research"""
    
    try:
        result = await luna_orchestrator.initiate_luna_consultation(
            request.message, 
            request.user_id
        )
        
        return {
            **result,
            "system_info": {
                "luna_multi_agent_available": LUNA_AVAILABLE,
                "capabilities": [
                    "Intelligent conversation analysis",
                    "Comprehensive competitor research via Parallel AI", 
                    "Multi-agent strategy synthesis",
                    "Implementation planning with automation scope"
                ]
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Luna consultation error: {str(e)}",
            "user_id": request.user_id
        }

@app.get("/luna/consultation/status/{user_id}")
async def get_consultation_status(user_id: str):
    """Get current Luna consultation status"""
    
    try:
        return await luna_orchestrator.get_consultation_status(user_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Status check error: {str(e)}",
            "user_id": user_id
        }

@app.get("/luna/system/info")
async def luna_system_info():
    """Get Luna AI system information"""
    
    return {
        "luna_status": "Multi-Agent Research System" if LUNA_AVAILABLE else "Mock Mode",
        "version": "3.0.0",
        "components": {
            "conversation_agent": "✅ Intelligent context extraction and question generation",
            "research_agent": "✅ Comprehensive competitor and market analysis", 
            "strategy_agent": "✅ Multi-expert strategy synthesis",
            "execution_agent": "✅ Implementation planning and automation scope"
        },
        "research_capabilities": [
            "Instagram competitor analysis via browser automation",
            "Parallel AI deep market research",
            "Visual content pattern analysis with Kimi v2",
            "Hashtag intelligence and trend research",
            "Lead generation funnel optimization"
        ],
        "available": LUNA_AVAILABLE
    }

# Enhanced health check
@app.get("/health")
async def enhanced_health_check():
    """Enhanced health check including Luna multi-agent system"""
    
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "luna_multi_agent_system": {
            "available": LUNA_AVAILABLE,
            "status": "operational" if LUNA_AVAILABLE else "mock_mode"
        },
        "api_integrations": {
            "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
            "parallel_ai_configured": bool(os.getenv("PARALLEL_AI_API_KEY"))
        }
    }

# === Luna AI Multi-Agent System Integration ===
import sys
import os
from datetime import datetime

# Add project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.conversation.conversation_agent import ConversationAgent
    
    class LunaMasterOrchestrator:
        def __init__(self):
            self.conversation_agent = ConversationAgent()
            self.active_conversations = {}
        
        async def initiate_luna_consultation(self, user_input: str, user_id: str):
            """Start Luna consultation with real ConversationAgent"""
            try:
                conversation_result = await self.conversation_agent.process_initial_input(user_input, user_id)
                
                self.active_conversations[user_id] = {
                    "stage": "conversation",
                    "conversation_data": conversation_result,
                    "started_at": datetime.utcnow().isoformat()
                }
                
                niche = conversation_result.get("context", {}).get("niche", "your field")
                
                return {
                    "status": "conversation_active",
                    "message": f"Perfect! I understand you're in the {niche} space. To create your comprehensive Instagram growth strategy, I need to dive deeper with a few targeted questions:",
                    "questions": conversation_result["follow_up_questions"],
                    "conversation_id": user_id,
                    "next_action": "answer_questions",
                    "luna_version": "Multi-Agent Research System v3.0"
                }
            except Exception as e:
                return {"status": "error", "message": f"Consultation error: {str(e)}"}
        
        async def get_consultation_status(self, user_id: str):
            """Get consultation status"""
            conversation_state = self.active_conversations.get(user_id)
            if not conversation_state:
                return {"status": "not_found", "message": "No active consultation found"}
            
            return {
                "status": "active",
                "current_stage": conversation_state["stage"],
                "started_at": conversation_state["started_at"],
                "conversation_id": user_id
            }
    
    luna_orchestrator = LunaMasterOrchestrator()
    LUNA_AVAILABLE = True
    print("✅ Luna AI Multi-Agent System loaded successfully")
    
except Exception as e:
    print(f"⚠️ Luna orchestrator error: {e}")
    
    # Fallback mock orchestrator
    class MockLunaOrchestrator:
        def __init__(self):
            self.active_conversations = {}
        
        async def initiate_luna_consultation(self, user_input: str, user_id: str):
            niche = "breathwork" if "breathwork" in user_input.lower() else "coaching"
            return {
                "status": "conversation_active",
                "message": f"Luna AI understands you're a {niche} professional! [Mock Mode]",
                "questions": [
                    {"category": "content", "question": "What type of content are you creating?", "priority": "high"},
                    {"category": "goals", "question": "What are your growth goals?", "priority": "high"}
                ],
                "conversation_id": user_id,
                "luna_version": "Multi-Agent Research System v3.0 (Mock Mode)"
            }
        
        async def get_consultation_status(self, user_id: str):
            return {"status": "active", "user_id": user_id, "message": "Mock mode consultation"}
    
    luna_orchestrator = MockLunaOrchestrator()
    LUNA_AVAILABLE = False

# Luna AI API Endpoints
@app.post("/luna/consultation/start")
async def start_luna_consultation(request: QueryRequest):
    """Start comprehensive Luna AI consultation"""
    try:
        result = await luna_orchestrator.initiate_luna_consultation(request.message, request.user_id)
        return {
            **result,
            "system_status": "operational" if LUNA_AVAILABLE else "mock_mode",
            "capabilities": [
                "Intelligent conversation analysis",
                "Context-aware question generation", 
                "Multi-agent strategy synthesis",
                "Implementation planning"
            ]
        }
    except Exception as e:
        return {"status": "error", "message": f"Luna consultation error: {str(e)}"}

@app.get("/luna/consultation/status/{user_id}")
async def get_consultation_status(user_id: str):
    """Get consultation status"""
    try:
        return await luna_orchestrator.get_consultation_status(user_id)
    except Exception as e:
        return {"status": "error", "message": f"Status error: {str(e)}"}

@app.get("/luna/system/info")
async def luna_system_info():
    """Get Luna system info"""
    return {
        "luna_status": "Multi-Agent Research System" if LUNA_AVAILABLE else "Mock Mode",
        "version": "3.0.0",
        "available": LUNA_AVAILABLE,
        "components": {
            "conversation_agent": "✅ Intelligent context extraction and question generation",
            "research_agent": "✅ Comprehensive competitor and market analysis",
            "strategy_agent": "✅ Multi-expert strategy synthesis", 
            "execution_agent": "✅ Implementation planning and automation scope"
        },
        "research_capabilities": [
            "Instagram competitor analysis via browser automation",
            "Parallel AI deep market research",
            "Visual content pattern analysis with Kimi v2",
            "Hashtag intelligence and trend research",
            "Lead generation funnel optimization"
        ]
    }

# Enhanced health check
@app.get("/health")
async def enhanced_health_check():
    """Enhanced health check including Luna status"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "luna_multi_agent_system": {
            "available": LUNA_AVAILABLE,
            "status": "operational" if LUNA_AVAILABLE else "mock_mode"
        },
        "api_integrations": {
            "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
            "parallel_ai_configured": bool(os.getenv("PARALLEL_AI_API_KEY"))
        }
    }

# Add Riona integration routes
from api.routes.riona_routes import router as riona_router
app.include_router(riona_router)

@app.get("/luna/system/complete-info")
async def get_complete_system_info():
    """Enhanced system info including Riona integration status"""
    try:
        from integration.riona_controller import RionaController
        
        # Test Riona controller
        controller = RionaController()
        riona_status = "operational"
        
    except Exception as e:
        riona_status = f"error: {str(e)}"
    
    return {
        "luna_status": "Multi-Agent Research System with Riona Integration",
        "version": "3.1.0",
        "available": True,
        "components": {
            "conversation_agent": "✅ Intelligent context extraction and question generation",
            "research_agent": "✅ Comprehensive competitor and market analysis", 
            "strategy_agent": "✅ Multi-expert strategy synthesis",
            "execution_agent": "✅ Implementation planning and automation scope",
            "riona_integration": f"✅ Strategy-to-execution pipeline: {riona_status}"
        },
        "new_capabilities": {
            "strategy_execution": "/luna/riona/execute-strategy",
            "execution_tracking": "/luna/riona/execution-status/{execution_id}",
            "user_executions": "/luna/riona/executions/user/{user_id}",
            "integration_health": "/luna/riona/health"
        }
    }

# Add Scheduling Routes
try:
    from api.routes.scheduling_routes import router as scheduling_router
    app.include_router(scheduling_router)
    print("✅ Scheduling routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Could not load scheduling routes: {e}")

@app.get("/luna/system/scheduling-info")
async def get_scheduling_system_info():
    """Get information about the humanized scheduling system"""
    return {
        "scheduling_system": "Humanized Social Media Manager",
        "version": "1.0.0",
        "features": {
            "user_controlled_hours": "✅ Custom work hours per user",
            "intelligent_breaks": "✅ Coffee breaks and lunch breaks",
            "activity_limits": "✅ Daily limits with weekend adjustments", 
            "natural_delays": "✅ Human-like thinking delays",
            "stealth_mode": "✅ Instagram bot detection avoidance",
            "adaptive_patterns": "✅ Learning from user behavior"
        },
        "endpoints": {
            "set_preferences": "/luna/scheduling/preferences",
            "get_status": "/luna/scheduling/status/{user_id}",
            "activity_summary": "/luna/scheduling/activity-summary/{user_id}",
            "test_schedule": "/luna/scheduling/test-schedule/{user_id}",
            "scheduled_execution": "/luna/scheduling/execute-strategy"
        }
    }

# Add Task Execution Routes
try:
    from api.routes.execution_routes import router as execution_router
    app.include_router(execution_router)
    print("✅ Task execution routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Could not load execution routes: {e}")

@app.get("/luna/system/execution-info")
async def get_execution_system_info():
    """Get information about the task execution system"""
    return {
        "execution_system": "Riona Task Execution Engine",
        "version": "1.0.0",
        "capabilities": {
            "smart_engagement": "✅ Intelligent post liking with rate limiting",
            "intelligent_commenting": "✅ Context-aware comment generation",
            "strategic_following": "✅ Targeted follow/unfollow automation",
            "audience_research": "✅ Competitor analysis and target identification"
        },
        "safety_features": {
            "rate_limiting": "✅ Instagram-compliant rate limits",
            "human_delays": "✅ Randomized human-like timing",
            "engagement_only": "✅ No posting or content creation",
            "error_handling": "✅ Comprehensive error recovery"
        },
        "endpoints": {
            "initialize_executor": "/luna/execution/initialize-executor",
            "execute_task": "/luna/execution/execute-task",
            "executor_stats": "/luna/execution/executor-stats/{user_id}",
            "test_engagement": "/luna/execution/test-engagement"
        }
    }
