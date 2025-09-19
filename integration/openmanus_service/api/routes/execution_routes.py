from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

# Import your enhanced controller
from integration.riona_controller.riona_controller import EnhancedRionaController

logger = logging.getLogger(__name__)

# Initialize enhanced controller
enhanced_riona = EnhancedRionaController(strict_mode=True)

router = APIRouter(prefix="/luna/execution", tags=["Task Execution"])

class TaskExecutionRequest(BaseModel):
    user_id: str
    task_type: str  # "engagement_like", "engagement_comment", "engagement_follow", "audience_research"
    task_data: Dict[str, Any]
    user_credentials: Optional[Dict[str, str]] = None

class ExecutorInitRequest(BaseModel):
    user_id: str
    credentials: Dict[str, str]

@router.post("/initialize-executor")
async def initialize_user_executor(request: ExecutorInitRequest):
    """
    Initialize task executor for a user with their Instagram credentials
    """
    try:
        success = await enhanced_riona.initialize_user_executor(
            request.user_id, 
            request.credentials
        )
        
        if success:
            return {
                "success": True,
                "message": f"Task executor initialized for user {request.user_id}",
                "user_id": request.user_id
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Failed to initialize task executor"
            )
            
    except Exception as e:
        logger.error(f"❌ Error initializing executor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-task")
async def execute_single_task(request: TaskExecutionRequest):
    """
    Execute a single Instagram engagement task
    """
    try:
        # Initialize executor if credentials provided
        if request.user_credentials:
            await enhanced_riona.initialize_user_executor(
                request.user_id, 
                request.user_credentials
            )
        
        # Prepare task data
        task = {
            "type": request.task_type,
            "details": request.task_data
        }
        
        # Execute task
        result = await enhanced_riona.execute_task_with_executor(
            task, 
            request.user_id
        )
        
        return {
            "success": result.get("success", True),
            "user_id": request.user_id,
            "task_type": request.task_type,
            "execution_result": result,
            "timestamp": result.get("completed_at")
        }
        
    except Exception as e:
        logger.error(f"❌ Task execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executor-stats/{user_id}")
async def get_executor_statistics(user_id: str):
    """
    Get execution statistics for a user's task executor
    """
    try:
        stats = await enhanced_riona.get_user_executor_stats(user_id)
        
        if stats:
            return {
                "user_id": user_id,
                "statistics": stats
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No executor found for user {user_id}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting executor stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-engagement")
async def test_engagement_system():
    """
    Test the engagement system with sample data
    """
    try:
        test_user_id = "test_engagement_user"
        test_credentials = {
            "username": "test_account",
            "password": "test_password"
        }
        
        # Initialize test executor
        await enhanced_riona.initialize_user_executor(test_user_id, test_credentials)
        
        # Test smart engagement
        engagement_task = {
            "type": "engagement_like",
            "details": {
                "post_urls": [
                    "https://instagram.com/p/sample1",
                    "https://instagram.com/p/sample2"
                ],
                "target_count": 2
            }
        }
        
        result = await enhanced_riona.execute_task_with_executor(
            engagement_task, 
            test_user_id
        )
        
        # Get stats
        stats = await enhanced_riona.get_user_executor_stats(test_user_id)
        
        return {
            "test_status": "completed",
            "engagement_result": result,
            "executor_stats": stats,
            "message": "Engagement system test successful"
        }
        
    except Exception as e:
        logger.error(f"❌ Engagement test failed: {e}")
        return {
            "test_status": "failed",
            "error": str(e),
            "message": "Engagement system test failed"
        }

@router.delete("/executor/{user_id}")
async def shutdown_user_executor(user_id: str):
    """
    Shutdown and cleanup task executor for a user
    """
    try:
        await enhanced_riona.shutdown_user_executor(user_id)
        
        return {
            "success": True,
            "message": f"Task executor shutdown for user {user_id}",
            "user_id": user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Error shutting down executor: {e}")
        raise HTTPException(status_code=500, detail=str(e))
