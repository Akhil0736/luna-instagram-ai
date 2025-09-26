"""
Upstash Redis client for Luna AI caching and session management
Free tier: 10K commands/day, 256MB storage
"""
import os
from upstash_redis import Redis
from typing import Dict, Any, Optional, List
import json
import logging
from datetime import datetime, timedelta


class UpstashClient:
    """Upstash Redis client wrapper for Luna AI"""

    def __init__(self):
        self.url = os.getenv("UPSTASH_REDIS_REST_URL", "")
        self.token = os.getenv("UPSTASH_REDIS_REST_TOKEN", "")

        if not self.url or not self.token:
            raise ValueError("UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN required")

        self.client = Redis(url=self.url, token=self.token)

    def set_session(self, session_id: str, session_data: Dict[str, Any], ttl: int = 3600) -> bool:
        """Store session data with TTL (default 1 hour)"""
        try:
            serialized_data = json.dumps(session_data, default=str)
            result = self.client.setex(f"session:{session_id}", ttl, serialized_data)
            return result == "OK"
        except Exception as e:
            logging.error(f"Error setting session: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            data = self.client.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logging.error(f"Error getting session: {e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            result = self.client.delete(f"session:{session_id}")
            return result > 0
        except Exception as e:
            logging.error(f"Error deleting session: {e}")
            return False

    def cache_query_response(self, cache_key: str, response_data: Dict[str, Any], ttl: int = 1800) -> bool:
        """Cache query response (30 min default TTL)"""
        try:
            serialized_data = json.dumps(response_data, default=str)
            result = self.client.setex(f"cache:query:{cache_key}", ttl, serialized_data)
            return result == "OK"
        except Exception as e:
            logging.error(f"Error caching query response: {e}")
            return False

    def get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached query response"""
        try:
            data = self.client.get(f"cache:query:{cache_key}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logging.error(f"Error getting cached response: {e}")
            return None

    def increment_rate_limit(self, user_id: str, window: int = 3600) -> int:
        """Increment rate limit counter (default 1 hour window)"""
        try:
            key = f"rate_limit:{user_id}:{datetime.now().strftime('%Y%m%d%H')}"
            count = self.client.incr(key)
            if count == 1:
                self.client.expire(key, window)
            return count
        except Exception as e:
            logging.error(f"Error incrementing rate limit: {e}")
            return 0

    def get_rate_limit_count(self, user_id: str) -> int:
        """Get current rate limit count for user"""
        try:
            key = f"rate_limit:{user_id}:{datetime.now().strftime('%Y%m%d%H')}"
            count = self.client.get(key)
            return int(count) if count else 0
        except Exception as e:
            logging.error(f"Error getting rate limit count: {e}")
            return 0

    def store_user_context(self, user_id: str, context_data: Dict[str, Any], ttl: int = 86400) -> bool:
        """Store temporary user context (24 hour default)"""
        try:
            serialized_data = json.dumps(context_data, default=str)
            result = self.client.setex(f"context:{user_id}", ttl, serialized_data)
            return result == "OK"
        except Exception as e:
            logging.error(f"Error storing user context: {e}")
            return False

    def get_user_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get temporary user context"""
        try:
            data = self.client.get(f"context:{user_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logging.error(f"Error getting user context: {e}")
            return None

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            # Get approximate cache statistics
            keys = self.client.keys("*")
            total_keys = len(keys) if keys else 0

            return {
                "total_keys": total_keys,
                "cache_status": "connected",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}


# Global Upstash client instance
upstash_client = UpstashClient()
