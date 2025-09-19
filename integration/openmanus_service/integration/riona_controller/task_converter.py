from typing import Dict, List, Any
import uuid
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StrategyExecutionPlanner:
    """
    Converts Luna AI strategies into Riona-executable tasks
    
    This is the bridge between Luna's intelligence and Riona's automation.
    Takes strategic recommendations and breaks them into specific actions.
    """
    
    def __init__(self):
        self.task_id_counter = 0
    
    def convert_strategy_to_tasks(self, luna_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Convert Luna's strategic output into Riona execution tasks
        
        Args:
            luna_strategy: Dictionary containing Luna's strategic recommendations
            Example:
            {
                "user_id": "breathwork_coach_123",
                "niche": "breathwork for entrepreneurs", 
                "strategy": {
                    "target_audience": ["stressed_entrepreneurs", "productivity_coaches"],
                    "engagement_tactics": ["like_competitor_followers", "comment_on_wellness_posts"],
                    "hashtag_strategy": ["#entrepreneurstress", "#breathworkbusiness"],
                    "content_themes": ["morning_routines", "stress_relief"]
                },
                "execution_plan": {
                    "daily_likes": 50,
                    "daily_follows": 20,
                    "daily_comments": 10
                }
            }
            
        Returns:
            List of executable tasks for Riona
        """
        tasks = []
        
        try:
            # Extract key information
            user_id = luna_strategy.get("user_id", "unknown")
            niche = luna_strategy.get("niche", "general")
            strategy = luna_strategy.get("strategy", {})
            execution_plan = luna_strategy.get("execution_plan", {})
            
            logger.info(f"Converting strategy for user {user_id} in niche: {niche}")
            
            # 1. Convert engagement tactics to tasks
            tasks.extend(self._create_engagement_tasks(strategy, execution_plan, user_id))
            
            # 2. Convert hashtag strategy to research tasks  
            tasks.extend(self._create_hashtag_tasks(strategy, user_id))
            
            # 3. Convert audience targeting to research tasks
            tasks.extend(self._create_audience_research_tasks(strategy, user_id))
            
            # 4. Create analytics tracking tasks
            tasks.extend(self._create_analytics_tasks(user_id))
            
            logger.info(f"Generated {len(tasks)} tasks for execution")
            return tasks
            
        except Exception as e:
            logger.error(f"Error converting strategy to tasks: {e}")
            return []
    
    def _create_engagement_tasks(self, strategy: Dict, execution_plan: Dict, user_id: str) -> List[Dict]:
        """Create engagement automation tasks"""
        tasks = []
        
        # Daily likes task
        daily_likes = execution_plan.get("daily_likes", 30)
        target_audience = strategy.get("target_audience", [])
        
        tasks.append({
            "task_id": self._generate_task_id(),
            "type": "engagement_like",
            "user_id": user_id,
            "details": {
                "action": "auto_like_posts",
                "target_count": daily_likes,
                "target_audience": target_audience,
                "filters": {
                    "min_followers": 100,
                    "max_followers": 100000,
                    "recent_posts_only": True
                }
            },
            "priority": "high",
            "estimated_duration": "2-4 hours"
        })
        
        # Daily follows task
        daily_follows = execution_plan.get("daily_follows", 15)
        tasks.append({
            "task_id": self._generate_task_id(),
            "type": "engagement_follow", 
            "user_id": user_id,
            "details": {
                "action": "strategic_follow",
                "target_count": daily_follows,
                "target_audience": target_audience,
                "follow_criteria": {
                    "active_in_niche": True,
                    "engagement_rate": ">2%"
                }
            },
            "priority": "medium",
            "estimated_duration": "1-2 hours"
        })
        
        # Daily comments task
        daily_comments = execution_plan.get("daily_comments", 5)
        content_themes = strategy.get("content_themes", ["motivation", "wellness"])
        
        tasks.append({
            "task_id": self._generate_task_id(),
            "type": "engagement_comment",
            "user_id": user_id,
            "details": {
                "action": "intelligent_comment",
                "target_count": daily_comments,
                "content_themes": content_themes,
                "comment_style": "helpful_and_genuine"
            },
            "priority": "medium", 
            "estimated_duration": "30-60 minutes"
        })
        
        return tasks
    
    def _create_hashtag_tasks(self, strategy: Dict, user_id: str) -> List[Dict]:
        """Create hashtag research and optimization tasks"""
        tasks = []
        
        hashtag_strategy = strategy.get("hashtag_strategy", [])
        if hashtag_strategy:
            tasks.append({
                "task_id": self._generate_task_id(),
                "type": "hashtag_research",
                "user_id": user_id,
                "details": {
                    "action": "research_trending_hashtags",
                    "base_hashtags": hashtag_strategy,
                    "research_depth": "comprehensive",
                    "find_related": True,
                    "analyze_competition": True
                },
                "priority": "low",
                "estimated_duration": "15-30 minutes"
            })
        
        return tasks
    
    def _create_audience_research_tasks(self, strategy: Dict, user_id: str) -> List[Dict]:
        """Create audience research and targeting tasks"""
        tasks = []
        
        target_audience = strategy.get("target_audience", [])
        if target_audience:
            tasks.append({
                "task_id": self._generate_task_id(),
                "type": "audience_research",
                "user_id": user_id,
                "details": {
                    "action": "analyze_competitor_followers",
                    "target_audience": target_audience,
                    "research_competitors": True,
                    "identify_active_users": True,
                    "build_prospect_list": True
                },
                "priority": "medium",
                "estimated_duration": "45-90 minutes"
            })
        
        return tasks
    
    def _create_analytics_tasks(self, user_id: str) -> List[Dict]:
        """Create analytics and tracking tasks"""
        return [{
            "task_id": self._generate_task_id(),
            "type": "analytics_tracking",
            "user_id": user_id,
            "details": {
                "action": "track_growth_metrics",
                "metrics": ["followers_count", "engagement_rate", "daily_reach"],
                "frequency": "daily",
                "report_back": True
            },
            "priority": "low",
            "estimated_duration": "5-10 minutes"
        }]
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        self.task_id_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"luna_task_{timestamp}_{self.task_id_counter}"

# Example usage and testing
if __name__ == "__main__":
    # Test the converter
    planner = StrategyExecutionPlanner()
    
    # Sample Luna strategy (what Luna AI would generate)
    sample_strategy = {
        "user_id": "breathwork_coach_123",
        "niche": "breathwork for entrepreneurs",
        "strategy": {
            "target_audience": ["stressed_entrepreneurs", "productivity_coaches", "wellness_seekers"],
            "engagement_tactics": ["like_competitor_followers", "comment_on_wellness_posts"],
            "hashtag_strategy": ["#entrepreneurstress", "#breathworkbusiness", "#wellnesscoach"],
            "content_themes": ["morning_routines", "stress_relief", "breathing_techniques"]
        },
        "execution_plan": {
            "daily_likes": 50,
            "daily_follows": 20, 
            "daily_comments": 8
        }
    }
    
    # Convert to Riona tasks
    tasks = planner.convert_strategy_to_tasks(sample_strategy)
    
    print(f"Generated {len(tasks)} tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['type']}: {task['details']['action']}")
