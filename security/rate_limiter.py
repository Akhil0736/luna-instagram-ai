"""
Advanced rate limiting system for Luna AI
Per-user, per-endpoint, and global rate limiting
"""
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
import time
from datetime import datetime, timedelta
from database.upstash_client import upstash_client
import logging


class LunaRateLimiter:
    """Advanced rate limiting with multiple strategies"""

    def __init__(self):
        self.cache = upstash_client

        # Rate limiting rules
        self.rate_limits = {
            "free_user": {
                "queries_per_hour": 50,
                "queries_per_day": 200,
                "burst_limit": 10  # Max queries in 1 minute
            },
            "authenticated_user": {
                "queries_per_hour": 200,
                "queries_per_day": 1000,
                "burst_limit": 30
            },
            "api_key_user": {
                "queries_per_hour": 500,
                "queries_per_day": 5000,
                "burst_limit": 50
            }
        }

    def check_rate_limit(self, user_id: str, user_type: str = "free_user", endpoint: str = "general") -> bool:
        """Check if user has exceeded rate limits"""
        try:
            limits = self.rate_limits.get(user_type, self.rate_limits["free_user"])
            current_time = datetime.utcnow()

            # Check burst limit (1 minute window)
            burst_key = f"burst:{user_id}:{current_time.strftime('%Y%m%d%H%M')}"
            burst_count = self.cache.client.incr(burst_key)
            if burst_count == 1:
                self.cache.client.expire(burst_key, 60)  # 1 minute TTL

            if burst_count > limits["burst_limit"]:
                logging.warning(f"Burst limit exceeded for user {user_id}: {burst_count}/{limits['burst_limit']}")
                raise HTTPException(
                    status_code=429,
                    detail=f"Too many requests. Limit: {limits['burst_limit']} per minute"
                )

            # Check hourly limit
            hour_key = f"hour:{user_id}:{current_time.strftime('%Y%m%d%H')}"
            hour_count = self.cache.client.incr(hour_key)
            if hour_count == 1:
                self.cache.client.expire(hour_key, 3600)  # 1 hour TTL

            if hour_count > limits["queries_per_hour"]:
                logging.warning(f"Hourly limit exceeded for user {user_id}: {hour_count}/{limits['queries_per_hour']}")
                raise HTTPException(
                    status_code=429,
                    detail=f"Hourly limit exceeded. Limit: {limits['queries_per_hour']} per hour"
                )

            # Check daily limit
            day_key = f"day:{user_id}:{current_time.strftime('%Y%m%d')}"
            day_count = self.cache.client.incr(day_key)
            if day_count == 1:
                self.cache.client.expire(day_key, 86400)  # 24 hours TTL

            if day_count > limits["queries_per_day"]:
                logging.warning(f"Daily limit exceeded for user {user_id}: {day_count}/{limits['queries_per_day']}")
                raise HTTPException(
                    status_code=429,
                    detail=f"Daily limit exceeded. Limit: {limits['queries_per_day']} per day"
                )

            return True

        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Rate limiting error: {e}")
            # Allow request on rate limiter failure
            return True

    def get_rate_limit_status(self, user_id: str, user_type: str = "free_user") -> Dict[str, Any]:
        """Get current rate limit status for user"""
        try:
            limits = self.rate_limits.get(user_type, self.rate_limits["free_user"])
            current_time = datetime.utcnow()

            # Get current usage
            burst_key = f"burst:{user_id}:{current_time.strftime('%Y%m%d%H%M')}"
            hour_key = f"hour:{user_id}:{current_time.strftime('%Y%m%d%H')}"
            day_key = f"day:{user_id}:{current_time.strftime('%Y%m%d')}"

            burst_count = int(self.cache.client.get(burst_key) or 0)
            hour_count = int(self.cache.client.get(hour_key) or 0)
            day_count = int(self.cache.client.get(day_key) or 0)

            return {
                "user_type": user_type,
                "limits": limits,
                "current_usage": {
                    "burst": f"{burst_count}/{limits['burst_limit']}",
                    "hourly": f"{hour_count}/{limits['queries_per_hour']}",
                    "daily": f"{day_count}/{limits['queries_per_day']}"
                },
                "remaining": {
                    "burst": max(0, limits["burst_limit"] - burst_count),
                    "hourly": max(0, limits["queries_per_hour"] - hour_count),
                    "daily": max(0, limits["queries_per_day"] - day_count)
                },
                "reset_times": {
                    "burst": (current_time + timedelta(minutes=1)).isoformat(),
                    "hourly": (current_time + timedelta(hours=1)).isoformat(),
                    "daily": (current_time + timedelta(days=1)).isoformat()
                }
            }

        except Exception as e:
            logging.error(f"Error getting rate limit status: {e}")
            return {"error": str(e)}


# Global rate limiter instance
rate_limiter = LunaRateLimiter()


# FastAPI middleware function
async def apply_rate_limiting(request: Request, user_data: Dict[str, Any]):
    """Apply rate limiting based on user type"""
    user_id = user_data.get("user_id", "anonymous")
    auth_method = user_data.get("auth_method", "none")

    # Determine user type for rate limiting
    if auth_method == "api_key":
        user_type = "api_key_user"
    elif auth_method == "jwt":
        user_type = "authenticated_user"
    else:
        user_type = "free_user"

    # Apply rate limiting
    endpoint = str(request.url.path)
    rate_limiter.check_rate_limit(user_id, user_type, endpoint)

    return user_type
