from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

from integration.riona_controller import RionaController

logger = logging.getLogger(__name__)

# Initialize Riona controller (will be shared across requests)
riona_controller = RionaController(strict_mode=True)

# Create API router
router = APIRouter(prefix="/luna/riona", tags=["Riona Integration"])

# Pydantic models for request/response validation
class StrategyExecutionRequest(BaseModel):
    """Request model for strategy execution"""
    user_id: str
    niche: str
    consultation_context: Optional[str] = None
    strategy: Dict[str, Any]
    execution_plan: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "breathwork_coach_sarah",
                "niche": "breathwork for entrepreneurs",
                "consultation_context": "Wants to grow from 500 to 5,000 followers in 90 days",
                "strategy": {
                    "target_audience": ["stressed_entrepreneurs", "wellness_seekers"],
                    "hashtag_strategy": ["#entrepreneurstress", "#breathworkbusiness"],
                    "engagement_tactics": ["like_competitor_followers", "comment_on_wellness_posts"]
                },
                "execution_plan": {
                    "daily_likes": 50,
                    "daily_follows": 20,
                    "daily_comments": 8
                }
            }
        }

class ExecutionResponse(BaseModel):
    """Response model for strategy execution"""
    success: bool
    execution_id: Optional[str] = None
    tasks_queued: Optional[int] = None
    tasks_filtered: Optional[int] = None
    safety_report: Optional[Dict[str, Any]] = None
    estimated_completion: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None

class ExecutionStatusResponse(BaseModel):
    """Response model for execution status"""
    execution_id: str
    user_id: Optional[str] = None
    status: str
    progress_percentage: float
    completed_tasks: int
    total_tasks: int
    current_task: Optional[str] = None
    errors: List[str]
    created_at: Optional[str] = None
    estimated_completion: Optional[str] = None

@router.post("/execute-strategy", response_model=ExecutionResponse)
async def execute_strategy_via_riona(
    request: StrategyExecutionRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute Luna AI strategy through Riona automation
    
    This endpoint receives a Luna AI strategy and converts it into 
    executable tasks for Riona, applying safety filters and queueing
    for humanized execution.
    """
    try:
        logger.info(f"🌙 Received strategy execution request for user: {request.user_id}")
        
        # Convert request to strategy dict
        luna_strategy = {
            "user_id": request.user_id,
            "niche": request.niche,
            "consultation_context": request.consultation_context,
            "strategy": request.strategy,
            "execution_plan": request.execution_plan
        }
        
        # Execute strategy through Riona controller
        result = await riona_controller.execute_strategy(luna_strategy)
        
        if result["success"]:
            logger.info(f"✅ Strategy queued successfully: {result['execution_id']}")
            return ExecutionResponse(
                success=True,
                execution_id=result["execution_id"],
                tasks_queued=result["tasks_queued"],
                tasks_filtered=result["tasks_filtered"],
                safety_report=result["safety_report"],
                estimated_completion=result["estimated_completion"],
                status=result["status"]
            )
        else:
            logger.error(f"❌ Strategy execution failed: {result['error']}")
            raise HTTPException(
                status_code=400,
                detail=f"Strategy execution failed: {result['error']}"
            )
            
    except Exception as e:
        logger.error(f"❌ API error executing strategy: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/execution-status/{execution_id}", response_model=ExecutionStatusResponse)
async def get_execution_status(execution_id: str):
    """
    Get current status of strategy execution
    
    Returns detailed information about execution progress,
    completed tasks, current task, and any errors.
    """
    try:
        logger.info(f"📊 Status check for execution: {execution_id}")
        
        status = await riona_controller.get_execution_status(execution_id)
        
        if status is None:
            raise HTTPException(
                status_code=404,
                detail=f"Execution {execution_id} not found"
            )
        
        return ExecutionStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting execution status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/executions/user/{user_id}")
async def get_user_executions(user_id: str):
    """
    Get all executions for a specific user
    
    Returns list of all strategy executions for the user,
    useful for tracking their automation history.
    """
    try:
        # Get all executions for user from controller
        user_executions = []
        
        for exec_id, exec_info in riona_controller.execution_queue.items():
            if exec_info.get("user_id") == user_id:
                status = await riona_controller.get_execution_status(exec_id)
                if status:
                    user_executions.append(status)
        
        return {
            "user_id": user_id,
            "total_executions": len(user_executions),
            "executions": user_executions
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting user executions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health")
async def riona_health_check():
    """
    Health check for Riona integration
    
    Verifies that the Riona controller is operational
    and ready to receive strategy executions.
    """
    try:
        return {
            "status": "healthy",
            "riona_controller": "operational",
            "strict_mode": riona_controller.task_filter.strict_mode,
            "active_executions": len(riona_controller.execution_queue),
            "message": "Luna → Riona integration ready"
        }
    except Exception as e:
        logger.error(f"❌ Riona health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Riona integration unhealthy: {str(e)}"
        )

@router.post("/test-integration")
async def test_luna_riona_integration():
    """
    Test endpoint for Luna → Riona integration
    
    Executes a sample strategy to verify the complete flow
    from Luna consultation to Riona task execution.
    """
    try:
        # Sample test strategy
        test_strategy = StrategyExecutionRequest(
            user_id="test_integration_user",
            niche="wellness coaching",
            consultation_context="Testing Luna → Riona integration",
            strategy={
                "target_audience": ["wellness_seekers", "entrepreneurs"],
                "hashtag_strategy": ["#wellness", "#coaching"],
                "engagement_tactics": ["like_posts", "strategic_follow"]
            },
            execution_plan={
                "daily_likes": 20,
                "daily_follows": 10,
                "daily_comments": 3
            }
        )
        
        # Execute test strategy
        result = await execute_strategy_via_riona(test_strategy, BackgroundTasks())
        
        return {
            "test_status": "passed",
            "integration_working": True,
            "execution_result": result,
            "message": "Luna → Riona integration test successful"
        }
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return {
            "test_status": "failed", 
            "integration_working": False,
            "error": str(e),
            "message": "Luna → Riona integration test failed"
        }
