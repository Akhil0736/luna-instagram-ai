"""
Advanced Analytics Module for Luna AI
Comprehensive performance tracking and insights
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics
import uuid

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    metric_id: str
    user_id: str
    timestamp: datetime
    metric_type: str
    value: float
    metadata: Dict[str, Any] = None

class MetricsCollector:
    """Advanced metrics collection system"""
    
    def __init__(self):
        self.metrics_storage: List[PerformanceMetric] = []
        self.collection_history: List[Dict[str, Any]] = []
    
    async def collect_execution_metrics(self, execution_data: Dict[str, Any]) -> List[PerformanceMetric]:
        """Collect comprehensive metrics from execution"""
        try:
            user_id = execution_data.get("user_id", "unknown")
            timestamp = datetime.now()
            collected_metrics = []
            
            # Core metrics
            metrics_to_collect = [
                ("success_rate", self._calculate_success_rate(execution_data)),
                ("engagement_rate", execution_data.get("engagement_rate", 0.0)),
                ("follower_growth", execution_data.get("follower_growth", 0)),
                ("performance_score", execution_data.get("performance_score", 50.0))
            ]
            
            for metric_type, value in metrics_to_collect:
                metric = PerformanceMetric(
                    metric_id=str(uuid.uuid4()),
                    user_id=user_id,
                    timestamp=timestamp,
                    metric_type=metric_type,
                    value=float(value) if value is not None else 0.0,
                    metadata={"execution_id": execution_data.get("execution_id")}
                )
                collected_metrics.append(metric)
                self.metrics_storage.append(metric)
            
            logger.info(f"Collected {len(collected_metrics)} metrics for user {user_id}")
            return collected_metrics
            
        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")
            return []
    
    def _calculate_success_rate(self, execution_data: Dict[str, Any]) -> float:
        """Calculate success rate from execution data"""
        successful = execution_data.get("successful_actions", 0)
        failed = execution_data.get("failed_actions", 0)
        total = successful + failed
        return (successful / total * 100) if total > 0 else 0.0
    
    async def aggregate_metrics(self, user_id: str, time_period: str = "7d") -> Dict[str, Any]:
        """Aggregate metrics for time period"""
        try:
            if time_period == "24h":
                since = datetime.now() - timedelta(hours=24)
            elif time_period == "7d":
                since = datetime.now() - timedelta(days=7)
            else:
                since = datetime.now() - timedelta(days=7)
            
            relevant_metrics = [
                m for m in self.metrics_storage
                if m.user_id == user_id and m.timestamp >= since
            ]
            
            if not relevant_metrics:
                return {"message": "No metrics available"}
            
            # Group and aggregate
            aggregated = {}
            for metric in relevant_metrics:
                if metric.metric_type not in aggregated:
                    aggregated[metric.metric_type] = []
                aggregated[metric.metric_type].append(metric.value)
            
            # Calculate statistics
            result = {}
            for metric_type, values in aggregated.items():
                result[metric_type] = {
                    "average": statistics.mean(values),
                    "count": len(values),
                    "latest": values[-1] if values else 0.0
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Metrics aggregation failed: {e}")
            return {"error": str(e)}

class PerformanceTracker:
    """Performance tracking with trend analysis"""
    
    def __init__(self):
        self.performance_history: List[Dict[str, Any]] = []
    
    async def track_performance_change(self, user_id: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Track performance changes"""
        try:
            tracking_record = {
                "tracking_id": str(uuid.uuid4()),
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": current_metrics,
                "status": "tracked"
            }
            
            self.performance_history.append(tracking_record)
            logger.info(f"Performance tracking completed for user {user_id}")
            return tracking_record
            
        except Exception as e:
            logger.error(f"Performance tracking failed: {e}")
            return {"error": str(e)}

class ReportingEngine:
    """Advanced reporting engine"""
    
    def __init__(self, metrics_collector, performance_tracker):
        self.metrics_collector = metrics_collector
        self.performance_tracker = performance_tracker
        self.generated_reports: List[Dict[str, Any]] = []
    
    async def generate_comprehensive_report(self, user_id: str, report_type: str = "performance", time_period: str = "7d") -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        try:
            aggregated_metrics = await self.metrics_collector.aggregate_metrics(user_id, time_period)
            
            report = {
                "report_id": str(uuid.uuid4()),
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "time_period": time_period,
                "metrics": aggregated_metrics,
                "insights": [
                    "📈 Performance tracking active",
                    "📊 Analytics system operational", 
                    "🎯 Comprehensive reporting available"
                ],
                "recommendations": [
                    "🔄 Continue monitoring performance trends",
                    "📈 Optimize based on collected metrics",
                    "🎯 Focus on high-performing strategies"
                ]
            }
            
            self.generated_reports.append(report)
            logger.info(f"Report generated for user {user_id}")
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"error": str(e)}

class DashboardDataProvider:
    """Dashboard data provider"""
    
    def __init__(self, metrics_collector, reporting_engine):
        self.metrics_collector = metrics_collector
        self.reporting_engine = reporting_engine
    
    async def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """Get dashboard data"""
        try:
            recent_metrics = await self.metrics_collector.aggregate_metrics(user_id, "24h")
            
            dashboard_data = {
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
                "metrics": recent_metrics,
                "status": "operational"
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Dashboard data generation failed: {e}")
            return {"error": str(e)}

# Export main classes
__all__ = [
    "MetricsCollector",
    "PerformanceTracker", 
    "ReportingEngine",
    "DashboardDataProvider",
    "PerformanceMetric"
]
