from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

# Import your feedback system
from feedback_optimization.feedback_controller import LunaFeedbackProcessor
from analytics.advanced_analytics import MetricsCollector, ReportingEngine, DashboardDataProvider

logger = logging.getLogger(__name__)

# Initialize systems
feedback_processor = LunaFeedbackProcessor()
metrics_collector = MetricsCollector()
reporting_engine = ReportingEngine(metrics_collector, None)
dashboard_provider = DashboardDataProvider(metrics_collector, reporting_engine)

router = APIRouter(prefix="/luna/feedback", tags=["Feedback & Optimization"])

class ExecutionFeedbackRequest(BaseModel):
    execution_id: str
    user_id: str
    performance_data: Dict[str, Any]
    instagram_metrics: Optional[Dict[str, Any]] = None

@router.post("/process-execution")
async def process_execution_feedback(request: ExecutionFeedbackRequest):
    """Process execution feedback and generate optimization insights"""
    try:
        # Collect metrics
        execution_data = {
            "execution_id": request.execution_id,
            "user_id": request.user_id,
            **request.performance_data
        }
        
        if request.instagram_metrics:
            execution_data["instagram_metrics"] = request.instagram_metrics
        
        # Collect performance metrics
        metrics = await metrics_collector.collect_execution_metrics(execution_data)
        
        # Process feedback
        feedback = await feedback_processor.process_execution_feedback(execution_data)
        
        return {
            "success": True,
            "feedback_id": feedback.feedback_id,
            "performance_score": feedback.performance_score,
            "success_rate": feedback.success_rate,
            "optimization_suggestions": feedback.optimization_suggestions,
            "strategy_adjustments": feedback.strategy_adjustments,
            "metrics_collected": len(metrics)
        }
        
    except Exception as e:
        logger.error(f"Feedback processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/{user_id}")
async def get_user_analytics(user_id: str, period: str = "7d"):
    """Get comprehensive user analytics"""
    try:
        # Get aggregated metrics
        metrics = await metrics_collector.aggregate_metrics(user_id, period)
        
        # Generate report
        report = await reporting_engine.generate_comprehensive_report(user_id, "analytics", period)
        
        return {
            "user_id": user_id,
            "period": period,
            "metrics": metrics,
            "insights": report.insights,
            "recommendations": report.recommendations,
            "performance_grade": report.metrics_summary.get("performance_grade", "N/A")
        }
        
    except Exception as e:
        logger.error(f"Analytics generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/{user_id}")
async def get_dashboard_data(user_id: str):
    """Get real-time dashboard data"""
    try:
        dashboard_data = await dashboard_provider.get_dashboard_data(user_id)
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Dashboard data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimization-report/{user_id}")
async def get_optimization_report(user_id: str):
    """Get optimization report with actionable insights"""
    try:
        # Get user feedback history
        user_feedback = [
            fb for fb in feedback_processor.feedback_history 
            if fb.user_id == user_id
        ]
        
        if not user_feedback:
            return {"message": "No feedback data available for optimization report"}
        
        # Get latest feedback
        latest_feedback = user_feedback[-1]
        
        # Calculate trend
        if len(user_feedback) >= 2:
            prev_score = user_feedback[-2].performance_score
            current_score = latest_feedback.performance_score
            trend = "improving" if current_score > prev_score else "declining" if current_score < prev_score else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "user_id": user_id,
            "current_performance_score": latest_feedback.performance_score,
            "performance_trend": trend,
            "latest_suggestions": latest_feedback.optimization_suggestions,
            "strategy_adjustments": latest_feedback.strategy_adjustments,
            "total_feedback_sessions": len(user_feedback),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Optimization report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

