from .advanced_analytics import MetricsCollector, PerformanceMetric
import logging

logger = logging.getLogger(__name__)

class InstagramMetricsCollector(MetricsCollector):
    """Instagram-specific metrics collection with enhanced tracking"""
    
    def __init__(self):
        super().__init__()
        self.instagram_specific_metrics = [
            "story_views", "profile_visits", "website_clicks",
            "discovery_reach", "hashtag_reach", "location_reach"
        ]
    
    async def collect_instagram_insights(self, user_id: str, instagram_data: dict) -> dict:
        """Collect Instagram Insights API data"""
        try:
            insights = {
                "impressions": instagram_data.get("impressions", 0),
                "reach": instagram_data.get("reach", 0), 
                "profile_views": instagram_data.get("profile_views", 0),
                "website_clicks": instagram_data.get("website_clicks", 0),
                "story_impressions": instagram_data.get("story_impressions", 0),
                "story_reach": instagram_data.get("story_reach", 0)
            }
            
            # Store as performance metrics
            for metric_name, value in insights.items():
                metric = PerformanceMetric(
                    metric_id=f"ig_{metric_name}_{user_id}_{int(datetime.now().timestamp())}",
                    user_id=user_id,
                    timestamp=datetime.now(),
                    metric_type=f"instagram_{metric_name}",
                    value=float(value),
                    metadata={"source": "instagram_insights_api"}
                )
                self.metrics_storage.append(metric)
            
            logger.info(f"Instagram insights collected for user {user_id}")
            return insights
            
        except Exception as e:
            logger.error(f"Instagram insights collection failed: {e}")
            return {}

