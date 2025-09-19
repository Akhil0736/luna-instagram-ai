from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
import uuid

from .task_converter import StrategyExecutionPlanner
from .task_filter import RionaTaskFilter

logger = logging.getLogger(__name__)

class RionaController:
    """
    Main controller for Luna → Riona integration
    
    Orchestrates the flow from Luna's strategies to Riona's execution:
    1. Receives Luna strategies
    2. Converts to executable tasks  
    3. Filters for safety
    4. Queues for Riona execution
    5. Tracks execution status
    """
    
    def __init__(self, strict_mode: bool = True):
        self.planner = StrategyExecutionPlanner()
        self.task_filter = RionaTaskFilter(strict_mode=strict_mode)
        self.execution_queue = {}  # Will store queued executions
        self.execution_status = {}  # Will track execution progress
        
    async def execute_strategy(self, luna_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method: Execute Luna strategy via Riona
        
        Args:
            luna_strategy: Strategy dict from Luna AI
            
        Returns:
            Execution tracking information
        """
        try:
            # Generate unique execution ID
            execution_id = self._generate_execution_id()
            user_id = luna_strategy.get("user_id", "unknown")
            
            logger.info(f"🌙 Starting strategy execution {execution_id} for user {user_id}")
            
            # Step 1: Convert strategy to tasks
            raw_tasks = self.planner.convert_strategy_to_tasks(luna_strategy)
            logger.info(f"📋 Converted strategy to {len(raw_tasks)} tasks")
            
            # Step 2: Apply safety filter
            safe_tasks = self.task_filter.filter_tasks(raw_tasks)
            safety_report = self.task_filter.get_safety_report(raw_tasks)
            logger.info(f"🛡️ Safety filter: {len(safe_tasks)}/{len(raw_tasks)} tasks approved")
            
            # Step 3: Queue for execution
            execution_info = {
                "execution_id": execution_id,
                "user_id": user_id,
                "strategy": luna_strategy,
                "tasks": safe_tasks,
                "safety_report": safety_report,
                "status": "queued",
                "created_at": datetime.now().isoformat(),
                "estimated_completion": self._calculate_completion_time(safe_tasks)
            }
            
            # Store in execution queue
            self.execution_queue[execution_id] = execution_info
            self.execution_status[execution_id] = {
                "status": "queued",
                "progress": 0,
                "completed_tasks": 0,
                "total_tasks": len(safe_tasks),
                "current_task": None,
                "errors": []
            }
            
            # Step 4: Start async execution (in background)
            asyncio.create_task(self._execute_tasks_async(execution_id))
            
            return {
                "success": True,
                "execution_id": execution_id,
                "tasks_queued": len(safe_tasks),
                "tasks_filtered": len(raw_tasks) - len(safe_tasks),
                "safety_report": safety_report,
                "estimated_completion": execution_info["estimated_completion"],
                "status": "queued_for_execution"
            }
            
        except Exception as e:
            logger.error(f"❌ Error executing strategy: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_id": None
            }
    
    async def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of strategy execution"""
        if execution_id not in self.execution_status:
            return None
            
        status = self.execution_status[execution_id].copy()
        execution_info = self.execution_queue.get(execution_id, {})
        
        return {
            "execution_id": execution_id,
            "user_id": execution_info.get("user_id"),
            "status": status["status"],
            "progress_percentage": (status["completed_tasks"] / status["total_tasks"] * 100) if status["total_tasks"] > 0 else 0,
            "completed_tasks": status["completed_tasks"],
            "total_tasks": status["total_tasks"],
            "current_task": status["current_task"],
            "errors": status["errors"],
            "created_at": execution_info.get("created_at"),
            "estimated_completion": execution_info.get("estimated_completion")
        }
    
    async def _execute_tasks_async(self, execution_id: str):
        """Execute tasks asynchronously (placeholder for Riona integration)"""
        try:
            execution_info = self.execution_queue[execution_id]
            status = self.execution_status[execution_id]
            tasks = execution_info["tasks"]
            
            status["status"] = "executing"
            logger.info(f"🤖 Starting execution of {len(tasks)} tasks for {execution_id}")
            
            for i, task in enumerate(tasks):
                # Update current task
                status["current_task"] = task["type"]
                status["progress"] = (i / len(tasks)) * 100
                
                # Simulate task execution (replace with actual Riona API calls)
                await self._execute_single_task(task)
                
                # Update completed count
                status["completed_tasks"] = i + 1
                
                # Add delay between tasks (humanized scheduling will control this)
                await asyncio.sleep(1)
            
            # Mark as completed
            status["status"] = "completed"
            status["progress"] = 100
            status["current_task"] = None
            
            logger.info(f"✅ Execution {execution_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Execution {execution_id} failed: {e}")
            self.execution_status[execution_id]["status"] = "failed"
            self.execution_status[execution_id]["errors"].append(str(e))
    
    async def _execute_single_task(self, task: Dict[str, Any]):
        """Execute a single task (placeholder - integrate with Riona here)"""
        # TODO: Integrate with actual Riona agent
        task_type = task["type"]
        task_details = task["details"]
        
        logger.info(f"🎯 Executing task: {task_type} - {task_details.get('action', 'unknown')}")
        
        # Placeholder: simulate task execution time
        await asyncio.sleep(2)
        
        # TODO: Replace with actual Riona API calls:
        # - Call Riona engagement functions
        # - Handle Riona responses
        # - Log execution results
        
        return {"success": True, "task_id": task["task_id"]}
    
    def _generate_execution_id(self) -> str:
        """Generate unique execution ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"luna_exec_{timestamp}_{unique_id}"
    
    def _calculate_completion_time(self, tasks: List[Dict]) -> str:
        """Calculate estimated completion time"""
        # Rough estimation based on task count
        hours = len(tasks) * 0.5  # 30 minutes per task average
        if hours < 1:
            return f"{int(hours * 60)} minutes"
        elif hours < 24:
            return f"{int(hours)} hours"
        else:
            return f"{int(hours / 24)} days"

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_controller():
        controller = RionaController(strict_mode=True)
        
        # Sample Luna strategy
        strategy = {
            "user_id": "test_breathwork_coach",
            "niche": "breathwork for entrepreneurs",
            "strategy": {
                "target_audience": ["stressed_entrepreneurs"],
                "hashtag_strategy": ["#entrepreneurstress"],
            },
            "execution_plan": {
                "daily_likes": 30,
                "daily_follows": 10
            }
        }
        
        # Execute strategy
        result = await controller.execute_strategy(strategy)
        print(f"Execution result: {result}")
        
        if result["success"]:
            execution_id = result["execution_id"]
            
            # Check status after a few seconds
            await asyncio.sleep(3)
            status = await controller.get_execution_status(execution_id)
            print(f"Execution status: {status}")
    
    asyncio.run(test_controller())

# Add import for the new task executor
from .riona_task_executor import RionaTaskExecutor

class EnhancedRionaController(RionaController):
    """
    Enhanced Riona Controller with actual task execution capabilities
    """
    
    def __init__(self, strict_mode: bool = True):
        super().__init__(strict_mode)
        self.task_executors = {}  # user_id -> RionaTaskExecutor
    
    async def initialize_user_executor(self, user_id: str, credentials: Dict[str, str]) -> bool:
        """Initialize task executor for a specific user"""
        try:
            executor = RionaTaskExecutor(credentials)
            if await executor.initialize():
                self.task_executors[user_id] = executor
                logger.info(f"✅ Initialized task executor for user {user_id}")
                return True
            else:
                logger.error(f"❌ Failed to initialize executor for user {user_id}")
                return False
        except Exception as e:
            logger.error(f"❌ Error initializing executor for user {user_id}: {e}")
            return False
    
    async def execute_task_with_executor(self, task: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Execute a specific task using the user's task executor"""
        try:
            executor = self.task_executors.get(user_id)
            if not executor:
                return {"success": False, "error": f"No executor found for user {user_id}"}
            
            task_type = task.get("type")
            task_details = task.get("details", {})
            
            if task_type == "engagement_like":
                return await executor.smart_engagement(task_details)
            elif task_type == "engagement_comment":
                return await executor.intelligent_commenting(task_details)
            elif task_type == "engagement_follow":
                return await executor.strategic_follow_unfollow(task_details)
            elif task_type == "audience_research":
                return await executor.audience_research(task_details)
            else:
                return {"success": False, "error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"❌ Task execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_executor_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get execution statistics for a user"""
        executor = self.task_executors.get(user_id)
        if executor:
            return await executor.get_execution_stats()
        return None
    
    async def shutdown_user_executor(self, user_id: str):
        """Shutdown task executor for a user"""
        executor = self.task_executors.get(user_id)
        if executor:
            await executor.shutdown()
            del self.task_executors[user_id]
            logger.info(f"🛑 Shutdown executor for user {user_id}")
