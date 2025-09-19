"""
Revolutionary Feedback Loop & Optimization System
Integrated version for Luna AI v3.0.0
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

@dataclass
class ExecutionFeedback:
    """Comprehensive execution feedback data"""
    feedback_id: str
    user_id: str
    execution_id: str
    timestamp: datetime
    performance_score: float
    success_rate: float
    engagement_metrics: Dict[str, float]
    optimization_suggestions: List[str]
    strategy_adjustments: Dict[str, Any]

class LunaFeedbackProcessor:
    """Advanced feedback processing system"""
    
    def __init__(self, luna_orchestrator=None):
        self.luna_orchestrator = luna_orchestrator
        self.feedback_history: List[ExecutionFeedback] = []
        self.optimization_models = {}
        
    async def process_execution_feedback(self, execution_data: Dict[str, Any]) -> ExecutionFeedback:
        """Process comprehensive execution feedback"""
        try:
            user_id = execution_data.get("user_id")
            execution_id = execution_data.get("execution_id")
            
            # Calculate performance metrics
            performance_score = self._calculate_performance_score(execution_data)
            success_rate = self._calculate_success_rate(execution_data)
            engagement_metrics = self._extract_engagement_metrics(execution_data)
            
            # Generate optimization suggestions
            optimization_suggestions = await self._generate_optimization_suggestions(
                user_id, performance_score, engagement_metrics
            )
            
            # Generate strategy adjustments
            strategy_adjustments = await self._generate_strategy_adjustments(
                user_id, execution_data, optimization_suggestions
            )
            
            # Create feedback object
            feedback = ExecutionFeedback(
                feedback_id=str(uuid.uuid4()),
                user_id=user_id,
                execution_id=execution_id,
                timestamp=datetime.now(),
                performance_score=performance_score,
                success_rate=success_rate,
                engagement_metrics=engagement_metrics,
                optimization_suggestions=optimization_suggestions,
                strategy_adjustments=strategy_adjustments
            )
            
            # Store feedback
            self.feedback_history.append(feedback)
            
            # Send refined strategy back to Luna if significant improvements identified
            if performance_score < 70 and len(optimization_suggestions) > 2:
                await self._update_luna_strategy(user_id, strategy_adjustments)
            
            logger.info(f"Processed feedback for execution {execution_id}")
            return feedback
            
        except Exception as e:
            logger.error(f"Feedback processing failed: {e}")
            raise
    
    def _calculate_performance_score(self, execution_data: Dict[str, Any]) -> float:
        """Calculate overall performance score (0-100)"""
        successful_actions = execution_data.get("successful_actions", 0)
        total_actions = execution_data.get("total_actions", 1)
        engagement_rate = execution_data.get("engagement_rate", 0.0)
        follower_growth = execution_data.get("follower_growth", 0)
        
        # Weighted performance calculation
        success_component = (successful_actions / total_actions) * 40
        engagement_component = min(engagement_rate * 1000, 30)  # Cap at 30 points
        growth_component = min(follower_growth * 2, 30)  # Cap at 30 points
        
        return success_component + engagement_component + growth_component
    
    def _calculate_success_rate(self, execution_data: Dict[str, Any]) -> float:
        """Calculate task success rate"""
        successful = execution_data.get("successful_actions", 0)
        total = execution_data.get("total_actions", 1)
        return (successful / total) * 100
    
    def _extract_engagement_metrics(self, execution_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract engagement-related metrics"""
        return {
            "engagement_rate": execution_data.get("engagement_rate", 0.0),
            "likes_per_action": execution_data.get("likes_received", 0) / max(1, execution_data.get("successful_actions", 1)),
            "comments_per_action": execution_data.get("comments_received", 0) / max(1, execution_data.get("successful_actions", 1)),
            "follower_conversion": execution_data.get("follower_growth", 0) / max(1, execution_data.get("successful_actions", 1))
        }
    
    async def _generate_optimization_suggestions(self, user_id: str, performance_score: float, 
                                               engagement_metrics: Dict[str, float]) -> List[str]:
        """Generate AI-powered optimization suggestions"""
        suggestions = []
        
        # Performance-based suggestions
        if performance_score < 50:
            suggestions.extend([
                "Reduce automation frequency by 40% to focus on quality over quantity",
                "Implement stricter target audience filtering criteria",
                "Add longer delays between actions to appear more natural"
            ])
        elif performance_score < 70:
            suggestions.extend([
                "Optimize posting times based on audience activity patterns",
                "Refine hashtag strategy for better targeting",
                "A/B test different engagement approaches"
            ])
        
        # Engagement-based suggestions  
        if engagement_metrics["engagement_rate"] < 0.03:
            suggestions.extend([
                "Switch to higher-quality target audience segments",
                "Improve content relevance for better engagement",
                "Focus on accounts with 2-8% engagement rates"
            ])
        
        if engagement_metrics["follower_conversion"] < 0.1:
            suggestions.append("Optimize follow timing - engage first, then follow")
        
        return suggestions
    
    async def _generate_strategy_adjustments(self, user_id: str, execution_data: Dict[str, Any], 
                                           suggestions: List[str]) -> Dict[str, Any]:
        """Generate specific strategy adjustments"""
        adjustments = {}
        
        # Frequency adjustments
        if any("reduce" in s for s in suggestions):
            current_limits = execution_data.get("daily_limits", {})
            adjustments["daily_limits"] = {
                "likes": int(current_limits.get("likes", 50) * 0.6),
                "follows": int(current_limits.get("follows", 20) * 0.6),
                "comments": int(current_limits.get("comments", 10) * 0.6)
            }
        
        # Timing adjustments
        if any("timing" in s or "delay" in s for s in suggestions):
            adjustments["timing_strategy"] = {
                "min_interval_minutes": 5,
                "max_actions_per_hour": 15,
                "peak_hours": ["18:00", "19:00", "20:00"]
            }
        
        # Audience adjustments
        if any("audience" in s or "targeting" in s for s in suggestions):
            adjustments["audience_filters"] = {
                "min_followers": 500,
                "max_followers": 50000,
                "engagement_rate_min": 0.02,
                "account_age_min": 30
            }
        
        return adjustments
    
    async def _update_luna_strategy(self, user_id: str, adjustments: Dict[str, Any]):
        """Update Luna AI strategy with optimized parameters"""
        try:
            if self.luna_orchestrator:
                await self.luna_orchestrator.update_user_strategy(user_id, adjustments)
                logger.info(f"Updated Luna strategy for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to update Luna strategy: {e}")

