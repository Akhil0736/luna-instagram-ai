"""
Riona API Client for Luna AI Integration
Production-ready Instagram automation client
"""
import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RionaAPIClient:
    """Production Riona API client with full Instagram automation capabilities"""
    
    def __init__(self, base_url: str = "http://localhost:8080", api_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.session = None
        self.rate_limits = {
            "likes_per_hour": 60,
            "follows_per_hour": 30, 
            "comments_per_hour": 15
        }
    
    async def initialize(self) -> bool:
        """Initialize the Riona API client"""
        try:
            self.session = httpx.AsyncClient(timeout=30.0)
            
            # Test connection
            response = await self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                logger.info("✅ Riona API client initialized successfully")
                return True
            else:
                logger.error(f"❌ Riona API connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Riona API initialization failed: {e}")
            return False
    
    async def execute_like_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Instagram like task via Riona"""
        try:
            url = f"{self.base_url}/api/v1/engagement/like"
            headers = self._get_headers()
            
            response = await self.session.post(url, json=task_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Like task completed: {result.get('likes_count', 0)} likes")
                return {"success": True, "result": result}
            else:
                error = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Like task failed: {error}")
                return {"success": False, "error": error}
                
        except Exception as e:
            logger.error(f"❌ Like task exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def execute_follow_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Instagram follow task via Riona"""
        try:
            url = f"{self.base_url}/api/v1/engagement/follow"
            headers = self._get_headers()
            
            response = await self.session.post(url, json=task_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Follow task completed: {result.get('follows_count', 0)} follows")
                return {"success": True, "result": result}
            else:
                error = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Follow task failed: {error}")
                return {"success": False, "error": error}
                
        except Exception as e:
            logger.error(f"❌ Follow task exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def execute_comment_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Instagram comment task via Riona"""
        try:
            url = f"{self.base_url}/api/v1/engagement/comment"
            headers = self._get_headers()
            
            response = await self.session.post(url, json=task_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Comment task completed: {result.get('comments_count', 0)} comments")
                return {"success": True, "result": result}
            else:
                error = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Comment task failed: {error}")
                return {"success": False, "error": error}
                
        except Exception as e:
            logger.error(f"❌ Comment task exception: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authentication"""
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers
    
    async def close(self):
        """Close the HTTP client"""
        if self.session:
            await self.session.aclose()

