from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class RionaTaskFilter:
    """
    Filters tasks to exclude dangerous or unwanted automation
    
    This is your safety system - ensures Riona only executes 
    engagement tasks, never posting or content creation.
    """
    
    # Tasks we NEVER want Riona to execute automatically
    EXCLUDED_TASK_TYPES = [
        'create_post',
        'post_content', 
        'schedule_post',
        'upload_media',
        'create_story',
        'post_reel',
        'auto_dm'  # Direct messaging can be risky
    ]
    
    # Tasks that are safe for automation
    ALLOWED_TASK_TYPES = [
        'engagement_like',
        'engagement_follow',
        'engagement_comment', 
        'hashtag_research',
        'audience_research',
        'analytics_tracking',
        'competitor_analysis'
    ]
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize filter
        
        Args:
            strict_mode: If True, only allows explicitly approved tasks
        """
        self.strict_mode = strict_mode
        
    def filter_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter task list to remove unsafe tasks
        
        Args:
            tasks: List of Riona tasks
            
        Returns:
            Filtered list of safe tasks
        """
        filtered_tasks = []
        excluded_count = 0
        
        for task in tasks:
            task_type = task.get('type', 'unknown')
            
            if self._is_task_allowed(task_type):
                filtered_tasks.append(task)
                logger.debug(f"✅ Allowed task: {task_type}")
            else:
                excluded_count += 1
                logger.warning(f"❌ Excluded task: {task_type} (safety filter)")
        
        logger.info(f"Filtered {len(tasks)} tasks → {len(filtered_tasks)} allowed, {excluded_count} excluded")
        return filtered_tasks
    
    def _is_task_allowed(self, task_type: str) -> bool:
        """Check if task type is allowed for execution"""
        
        # Never allow explicitly banned tasks
        if task_type in self.EXCLUDED_TASK_TYPES:
            return False
            
        # In strict mode, only allow explicitly approved tasks
        if self.strict_mode:
            return task_type in self.ALLOWED_TASK_TYPES
        
        # In non-strict mode, allow anything not explicitly banned
        return True
    
    def get_safety_report(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate safety report for task list
        
        Returns:
            Dict with safety analysis
        """
        total_tasks = len(tasks)
        safe_tasks = len(self.filter_tasks(tasks))
        excluded_tasks = total_tasks - safe_tasks
        
        excluded_types = []
        for task in tasks:
            task_type = task.get('type', 'unknown')
            if not self._is_task_allowed(task_type):
                excluded_types.append(task_type)
        
        return {
            "total_tasks": total_tasks,
            "safe_tasks": safe_tasks,
            "excluded_tasks": excluded_tasks,
            "safety_percentage": (safe_tasks / total_tasks * 100) if total_tasks > 0 else 100,
            "excluded_types": list(set(excluded_types)),
            "strict_mode": self.strict_mode
        }

# Example usage
if __name__ == "__main__":
    # Test the filter
    filter_system = RionaTaskFilter(strict_mode=True)
    
    # Sample tasks including some that should be filtered
    sample_tasks = [
        {"type": "engagement_like", "details": {"action": "like_posts"}},
        {"type": "create_post", "details": {"action": "auto_post"}},  # Should be filtered
        {"type": "hashtag_research", "details": {"action": "research"}},
        {"type": "post_content", "details": {"action": "schedule"}},  # Should be filtered
        {"type": "engagement_follow", "details": {"action": "follow_users"}}
    ]
    
    # Filter tasks
    safe_tasks = filter_system.filter_tasks(sample_tasks)
    safety_report = filter_system.get_safety_report(sample_tasks)
    
    print(f"Safety Report: {safety_report}")
    print(f"Safe tasks: {len(safe_tasks)}")
