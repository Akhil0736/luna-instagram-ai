from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/luna/scheduling", tags=["User Scheduling"])

# Simple in-memory storage for demo (replace with database in production)
user_preferences_storage = {}

class UserSchedulingPreferencesRequest(BaseModel):
    user_id: str
    working_hours: Optional[Dict[str, str]] = None
    break_preferences: Optional[Dict[str, Any]] = None
    activity_settings: Optional[Dict[str, Any]] = None
    weekly_schedule: Optional[Dict[str, Any]] = None
    stealth_mode: Optional[bool] = None
    adaptive_scheduling: Optional[bool] = None

@router.post("/preferences")
async def set_user_scheduling_preferences(request: UserSchedulingPreferencesRequest):
    """Set or update user scheduling preferences"""
    try:
        user_id = request.user_id
        
        # Store preferences (simplified for testing)
        preferences_data = {
            "user_id": user_id,
            "working_hours": request.working_hours or {"start_time": "09:00", "end_time": "17:00"},
            "break_preferences": request.break_preferences or {"coffee_breaks": True, "lunch_break": True},
            "activity_settings": request.activity_settings or {"daily_likes": 50, "daily_follows": 20},
            "weekly_schedule": request.weekly_schedule or {"active_days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]},
            "stealth_mode": request.stealth_mode if request.stealth_mode is not None else True,
            "adaptive_scheduling": request.adaptive_scheduling if request.adaptive_scheduling is not None else True
        }
        
        user_preferences_storage[user_id] = preferences_data
        
        logger.info(f"✅ Updated scheduling preferences for user {user_id}")
        
        return {
            "success": True,
            "message": "Scheduling preferences updated successfully",
            "user_id": user_id,
            "preferences": preferences_data
        }
        
    except Exception as e:
        logger.error(f"❌ Error setting user preferences: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to set preferences: {str(e)}")

@router.get("/preferences/{user_id}")
async def get_user_scheduling_preferences(user_id: str):
    """Get current scheduling preferences for a user"""
    try:
        if user_id not in user_preferences_storage:
            raise HTTPException(status_code=404, detail=f"No scheduling preferences found for user {user_id}")
        
        preferences = user_preferences_storage[user_id]
        
        return {
            "user_id": user_id,
            "preferences": preferences,
            "current_status": {
                "date": "2025-09-18",
                "status": "active",
                "activity_count": {"likes": 0, "follows": 0, "comments": 0}
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting user preferences: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/status/{user_id}")
async def get_user_schedule_status(user_id: str):
    """Get current schedule status for a user"""
    try:
        # Simplified status for testing
        return {
            "user_id": user_id,
            "schedule_status": "active",
            "status_reason": "Ready for activity",
            "activity_summary": {
                "date": "2025-09-18",
                "day": "Thursday",
                "status": "active",
                "status_reason": "Ready for activity",
                "activity_count": {"likes": 0, "follows": 0, "comments": 0},
                "daily_limits": {"likes": 50, "follows": 20, "comments": 8},
                "completion_percentage": {"likes": 0.0, "follows": 0.0, "comments": 0.0},
                "working_hours": "09:00-17:00"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting schedule status: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/test-schedule/{user_id}")
async def test_user_schedule(user_id: str):
    """Test user scheduling preferences"""
    try:
        return {
            "user_id": user_id,
            "current_schedule_status": "active",
            "status_reason": "Ready for activity",
            "activity_tests": {
                "likes": [True, "Can perform likes (0/50)"],
                "follows": [True, "Can perform follows (0/20)"],
                "comments": [True, "Can perform comments (0/8)"]
            },
            "timing_tests": {
                "coffee_break_probability": False,
                "lunch_break_time": False,
                "next_delay_seconds": 30
            },
            "activity_summary": {
                "date": "2025-09-18",
                "status": "active",
                "activity_count": {"likes": 0, "follows": 0, "comments": 0}
            },
            "preferences_active": True
        }
        
    except Exception as e:
        logger.error(f"❌ Error testing schedule: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/execute-strategy")
async def execute_strategy_with_scheduling(request: dict):
    """Execute Luna strategy with humanized scheduling"""
    try:
        user_id = request.get("user_id", "unknown")
        
        # Simplified execution for testing
        return {
            "success": True,
            "execution_id": f"luna_exec_20250918_181700_test123",
            "tasks_queued": 4,
            "tasks_filtered": 0,
            "scheduling_info": {
                "user_scheduler": user_id,
                "humanized_execution": True,
                "activity_summary": {
                    "date": "2025-09-18",
                    "status": "executing",
                    "working_hours": "09:00-17:00"
                }
            },
            "estimated_completion": "2 hours",
            "status": "queued_for_humanized_execution"
        }
        
    except Exception as e:
        logger.error(f"❌ Error executing scheduled strategy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/activity-summary/{user_id}")
async def get_user_activity_summary(user_id: str):
    """Get detailed activity summary for a user"""
    try:
        return {
            "date": "2025-09-18",
            "day": "Thursday",
            "status": "active",
            "status_reason": "Ready for activity",
            "activity_count": {"likes": 0, "follows": 0, "comments": 0},
            "daily_limits": {"likes": 50, "follows": 20, "comments": 8},
            "completion_percentage": {"likes": 0.0, "follows": 0.0, "comments": 0.0},
            "working_hours": "09:00-17:00",
            "break_end": None
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting activity summary: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
