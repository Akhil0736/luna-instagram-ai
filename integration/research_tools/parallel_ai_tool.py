from __future__ import annotations
import os
import asyncio
import time
import json
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass
import aiohttp
import logging
from integration.models import ResearchInsight
from .base import ResearchTool

@dataclass
class ParallelAIConfig:
    """Production configuration for Parallel AI"""
    api_key: str
    base_url: str = "https://api.parallel.ai/v1"
    search_base_url: str = "https://api.parallel.ai/v1beta"
    default_processor: Literal["base", "core"] = "core"
    timeout_seconds: int = 120
    max_retries: int = 3
    enable_search_api: bool = True
    search_rate_limit: int = 600  # per minute

class ParallelAIResearchTool(ResearchTool):
    """
    Production Parallel AI research tool implementing both Task and Search APIs
    """
    name = "parallel_ai"
    
    def __init__(self, config: Optional[ParallelAIConfig] = None):
        self.config = config or ParallelAIConfig(
            api_key=os.getenv("PARALLEL_API_KEY", "")
        )
        self.logger = logging.getLogger(__name__)
        
        if not self.config.api_key:
            raise ValueError("PARALLEL_API_KEY environment variable is required")
        
        # Performance tracking
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "avg_response_time": 0.0,
            "error_rate": 0.0,
            "search_api_calls": 0,
            "task_api_calls": 0
        }
        
        # Rate limiting for Search API (600/min)
        self._search_api_calls = []
        self._search_rate_window = 60  # seconds
    
    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        """Standard research interface - uses Task API for comprehensive research"""
        if not queries:
            return []
        
        primary_query = queries[0]
        context_queries = queries[1:] if len(queries) > 1 else []
        
        return await self.task_api_research(primary_query, context_queries)
    
    async def task_api_research(
        self, 
        primary_query: str, 
        context_queries: List[str] = None,
        research_type: str = "instagram_growth"
    ) -> List[ResearchInsight]:
        """
        Use Parallel AI Task API for structured Instagram research
        """
        start_time = time.time()
        
        try:
            # Create Instagram-optimized task specification
            task_spec = self._create_instagram_task_spec(research_type)
            
            # Format input for Instagram research
            task_input = self._format_instagram_input(primary_query, context_queries)
            
            # Execute Task API request
            run_data = await self._create_task_run(task_input, task_spec)
            
            if not run_data or "run_id" not in run_data:
                raise Exception("Failed to create task run")
            
            # Poll for results
            result_data = await self._poll_task_result(run_data["run_id"])
            
            # Convert to ResearchInsight objects
            insights = self._process_task_result(result_data, primary_query)
            
            self._update_performance_metrics(start_time, success=True, api_type="task")
            return insights
            
        except Exception as e:
            self.logger.error(f"Task API research failed: {e}")
            self._update_performance_metrics(start_time, success=False, api_type="task")
            
            # Fallback to Search API if available
            if self.config.enable_search_api:
                return await self.search_api_research(primary_query, context_queries)
            
            raise
    
    async def search_api_research(
        self,
        primary_query: str,
        context_queries: List[str] = None
    ) -> List[ResearchInsight]:
        """
        Use Parallel AI Search API for quick Instagram trend research
        """
        start_time = time.time()
        
        try:
            # Check rate limits
            if not self._check_search_rate_limit():
                self.logger.warning("Search API rate limit exceeded, skipping")
                return []
            
            # Create search request
            search_payload = {
                "objective": f"Instagram growth research: {primary_query}",
                "search_queries": [primary_query] + (context_queries or []),
                "processor": "base",  # Use base for speed
                "max_results": 10,
                "max_chars_per_result": 4000
            }
            
            headers = {
                "x-api-key": self.config.api_key,
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.search_base_url}/search",
                    headers=headers,
                    json=search_payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status != 200:
                        raise Exception(f"Search API error: {response.status}")
                    
                    result = await response.json()
                    insights = self._process_search_result(result, primary_query)
                    
                    self._update_performance_metrics(start_time, success=True, api_type="search")
                    self._record_search_api_call()
                    
                    return insights
        
        except Exception as e:
            self.logger.error(f"Search API research failed: {e}")
            self._update_performance_metrics(start_time, success=False, api_type="search")
            return []
    
    def _create_instagram_task_spec(self, research_type: str) -> Dict[str, Any]:
        """Create task specification optimized for Instagram research"""
        
        base_schema = {
            "type": "json",
            "json_schema": {
                "type": "object",
                "properties": {
                    "growth_strategies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of proven Instagram growth strategies specific to the niche"
                    },
                    "content_recommendations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content_type": {"type": "string"},
                                "description": {"type": "string"},
                                "engagement_potential": {"type": "string", "enum": ["high", "medium", "low"]}
                            }
                        },
                        "description": "Specific content recommendations with engagement potential"
                    },
                    "hashtag_strategy": {
                        "type": "object",
                        "properties": {
                            "primary_hashtags": {"type": "array", "items": {"type": "string"}},
                            "niche_hashtags": {"type": "array", "items": {"type": "string"}},
                            "trending_hashtags": {"type": "array", "items": {"type": "string"}}
                        },
                        "description": "Comprehensive hashtag strategy"
                    },
                    "posting_schedule": {
                        "type": "object",
                        "properties": {
                            "optimal_times": {"type": "array", "items": {"type": "string"}},
                            "frequency": {"type": "string"},
                            "content_mix": {"type": "string"}
                        },
                        "description": "Optimal posting schedule and content mix"
                    },
                    "engagement_tactics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific tactics to increase engagement and followers"
                    },
                    "success_metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Key metrics to track for measuring success"
                    }
                },
                "required": ["growth_strategies", "content_recommendations", "hashtag_strategy", "posting_schedule", "engagement_tactics"],
                "additionalProperties": False
            }
        }
        
        return {"output_schema": base_schema}
    
    def _format_instagram_input(self, primary_query: str, context_queries: List[str]) -> Dict[str, Any]:
        """Format input for Instagram research task"""
        return {
            "niche_or_topic": primary_query,
            "additional_context": context_queries or [],
            "research_focus": "Instagram growth and engagement strategies",
            "target_metrics": ["followers", "engagement_rate", "reach", "conversions"]
        }
    
    async def _create_task_run(self, task_input: Dict[str, Any], task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task run"""
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": task_input,
            "processor": self.config.default_processor,
            "task_spec": task_spec
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.config.base_url}/tasks/runs",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Task creation failed: {response.status} - {error_text}")
                
                return await response.json()
    
    async def _poll_task_result(self, run_id: str) -> Dict[str, Any]:
        """Poll for task completion and retrieve results"""
        headers = {
            "x-api-key": self.config.api_key
        }
        
        max_polls = 60  # 60 polls * 2 seconds = 2 minutes max wait
        poll_interval = 2
        
        for attempt in range(max_polls):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.base_url}/tasks/runs/{run_id}/result",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        if result.get("run", {}).get("status") == "completed":
                            return result
                        elif result.get("run", {}).get("status") == "failed":
                            raise Exception(f"Task failed: {result}")
                    
                    elif response.status != 202:  # 202 is expected for pending
                        error_text = await response.text()
                        raise Exception(f"Polling failed: {response.status} - {error_text}")
            
            await asyncio.sleep(poll_interval)
        
        raise Exception(f"Task {run_id} timed out after {max_polls * poll_interval} seconds")
    
    def _process_task_result(self, result_data: Dict[str, Any], query: str) -> List[ResearchInsight]:
        """Convert Task API result to ResearchInsight objects"""
        insights = []
        
        try:
            output = result_data.get("output", {})
            content = output.get("content", {})
            basis = output.get("basis", [])
            
            # Create insights from structured content
            if "growth_strategies" in content:
                for strategy in content["growth_strategies"]:
                    insights.append(ResearchInsight(
                        source="parallel_ai_task",
                        insight=f"Growth strategy: {strategy}",
                        confidence=0.8,
                        metadata={
                            "type": "growth_strategy",
                            "query": query,
                            "processor": self.config.default_processor
                        }
                    ))
            
            if "content_recommendations" in content:
                for rec in content["content_recommendations"]:
                    confidence_map = {"high": 0.9, "medium": 0.7, "low": 0.5}
                    confidence = confidence_map.get(rec.get("engagement_potential", "medium"), 0.7)
                    
                    insights.append(ResearchInsight(
                        source="parallel_ai_task",
                        insight=f"Content recommendation ({rec.get('content_type', 'general')}): {rec.get('description', '')}",
                        confidence=confidence,
                        metadata={
                            "type": "content_recommendation",
                            "content_type": rec.get("content_type"),
                            "engagement_potential": rec.get("engagement_potential")
                        }
                    ))
            
            if "hashtag_strategy" in content:
                hashtag_data = content["hashtag_strategy"]
                hashtag_insight = f"Hashtag strategy - Primary: {', '.join(hashtag_data.get('primary_hashtags', [])[:5])}"
                if hashtag_data.get("trending_hashtags"):
                    hashtag_insight += f" | Trending: {', '.join(hashtag_data['trending_hashtags'][:3])}"
                
                insights.append(ResearchInsight(
                    source="parallel_ai_task",
                    insight=hashtag_insight,
                    confidence=0.85,
                    metadata={
                        "type": "hashtag_strategy",
                        "primary_count": len(hashtag_data.get('primary_hashtags', [])),
                        "niche_count": len(hashtag_data.get('niche_hashtags', [])),
                        "trending_count": len(hashtag_data.get('trending_hashtags', []))
                    }
                ))
            
            if "posting_schedule" in content:
                schedule = content["posting_schedule"]
                schedule_insight = f"Optimal posting: {schedule.get('frequency', 'Not specified')}"
                if schedule.get("optimal_times"):
                    schedule_insight += f" at {', '.join(schedule['optimal_times'][:3])}"
                
                insights.append(ResearchInsight(
                    source="parallel_ai_task",
                    insight=schedule_insight,
                    confidence=0.8,
                    metadata={
                        "type": "posting_schedule",
                        "frequency": schedule.get("frequency"),
                        "optimal_times": schedule.get("optimal_times", [])
                    }
                ))
            
            if "engagement_tactics" in content:
                for tactic in content["engagement_tactics"][:5]:  # Limit to top 5
                    insights.append(ResearchInsight(
                        source="parallel_ai_task",
                        insight=f"Engagement tactic: {tactic}",
                        confidence=0.75,
                        metadata={
                            "type": "engagement_tactic"
                        }
                    ))
            
            # Add citation-based insights
            for basis_item in basis:
                field = basis_item.get("field", "unknown")
                reasoning = basis_item.get("reasoning", "")
                confidence_level = basis_item.get("confidence", "medium")
                
                confidence_map = {"high": 0.9, "medium": 0.7, "low": 0.5}
                confidence = confidence_map.get(confidence_level, 0.7)
                
                if reasoning:
                    insights.append(ResearchInsight(
                        source="parallel_ai_citations",
                        insight=f"Research finding ({field}): {reasoning}",
                        confidence=confidence,
                        metadata={
                            "type": "research_finding",
                            "field": field,
                            "confidence_level": confidence_level,
                            "citations_count": len(basis_item.get("citations", []))
                        }
                    ))
        
        except Exception as e:
            self.logger.error(f"Error processing task result: {e}")
            # Fallback insight
            insights.append(ResearchInsight(
                source="parallel_ai_task_error",
                insight=f"Task completed but result processing failed: {str(e)[:200]}",
                confidence=0.3,
                metadata={"error": True, "processing_error": str(e)}
            ))
        
        return insights
    
    def _process_search_result(self, result_data: Dict[str, Any], query: str) -> List[ResearchInsight]:
        """Convert Search API result to ResearchInsight objects"""
        insights = []
        
        try:
            results = result_data.get("results", [])
            
            for idx, result in enumerate(results[:5]):  # Limit to top 5 results
                url = result.get("url", "")
                title = result.get("title", "")
                excerpts = result.get("excerpts", [])
                
                # Combine excerpts into a single insight
                combined_excerpt = " ".join(excerpts[:3])  # Max 3 excerpts per result
                
                if combined_excerpt:
                    insights.append(ResearchInsight(
                        source="parallel_ai_search",
                        insight=f"From {title}: {combined_excerpt[:300]}...",
                        confidence=0.6 + (0.1 * (5 - idx)),  # Higher confidence for top results
                        metadata={
                            "type": "search_result",
                            "url": url,
                            "title": title,
                            "query": query,
                            "result_rank": idx + 1
                        }
                    ))
        
        except Exception as e:
            self.logger.error(f"Error processing search result: {e}")
        
        return insights
    
    def _check_search_rate_limit(self) -> bool:
        """Check if Search API rate limit allows new request"""
        now = time.time()
        
        # Remove calls older than rate window
        self._search_api_calls = [
            call_time for call_time in self._search_api_calls 
            if now - call_time < self._search_rate_window
        ]
        
        # Check if under limit
        return len(self._search_api_calls) < self.config.search_rate_limit
    
    def _record_search_api_call(self):
        """Record a Search API call for rate limiting"""
        self._search_api_calls.append(time.time())
    
    def _update_performance_metrics(self, start_time: float, success: bool, api_type: str):
        """Update performance metrics"""
        duration = time.time() - start_time
        
        self.performance_metrics["total_requests"] += 1
        self.performance_metrics[f"{api_type}_api_calls"] += 1
        
        if success:
            self.performance_metrics["successful_requests"] += 1
        
        # Update moving average for response time
        current_avg = self.performance_metrics["avg_response_time"]
        total = self.performance_metrics["total_requests"]
        self.performance_metrics["avg_response_time"] = (current_avg * (total - 1) + duration) / total
        
        # Update error rate
        self.performance_metrics["error_rate"] = 1 - (
            self.performance_metrics["successful_requests"] / total
        )
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics.copy()
    
    # Instagram-specific research methods
    async def instagram_competitor_analysis(self, competitors: List[str]) -> List[ResearchInsight]:
        """Specialized Instagram competitor analysis using Task API"""
        
        task_spec = {
            "output_schema": {
                "type": "json",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "competitor_strategies": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "competitor": {"type": "string"},
                                    "content_strategy": {"type": "string"},
                                    "engagement_tactics": {"type": "array", "items": {"type": "string"}},
                                    "posting_frequency": {"type": "string"},
                                    "unique_approaches": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        }
                    }
                }
            }
        }
        
        task_input = {
            "competitors": competitors,
            "analysis_focus": "Instagram content strategy, engagement tactics, and growth approaches"
        }
        
        try:
            run_data = await self._create_task_run(task_input, task_spec)
            result_data = await self._poll_task_result(run_data["run_id"])
            return self._process_task_result(result_data, f"competitor analysis: {', '.join(competitors)}")
        except Exception as e:
            self.logger.error(f"Competitor analysis failed: {e}")
            return []
    
    async def instagram_trend_analysis(self, niche: str, timeframe: str = "current") -> List[ResearchInsight]:
        """Specialized Instagram trend analysis"""
        
        if self.config.enable_search_api and self._check_search_rate_limit():
            # Use Search API for trend analysis (faster, more current)
            search_payload = {
                "objective": f"Current Instagram trends and viral content strategies in {niche} niche. Focus on 2025 trends.",
                "search_queries": [
                    f"{niche} Instagram trends 2025",
                    f"viral {niche} content Instagram",
                    f"{niche} Instagram growth trends"
                ],
                "processor": "pro",  # Use pro for trend analysis
                "max_results": 8,
                "max_chars_per_result": 3000
            }
            
            try:
                headers = {"x-api-key": self.config.api_key, "Content-Type": "application/json"}
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.config.search_base_url}/search",
                        headers=headers,
                        json=search_payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            self._record_search_api_call()
                            return self._process_search_result(result, f"{niche} trends")
            
            except Exception as e:
                self.logger.warning(f"Trend analysis via Search API failed: {e}")
        
        # Fallback to Task API
        return await self.task_api_research(f"{niche} Instagram trends {timeframe}", research_type="trend_analysis")
