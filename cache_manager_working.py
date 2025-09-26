import asyncio
import hashlib
import json
import time
from typing import Optional, Dict, Any
from cachetools import LRUCache
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingLunaCacheManager:
    def __init__(self, l1_cache_size: int = 1024):
        self.l1_cache = LRUCache(maxsize=l1_cache_size)
        self.l1_lock = threading.RLock()
        
        # Metrics
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_cost_saved = 0.0
        # User query history for memory hand-off
        self.user_histories: Dict[str, List[Dict[str, Any]]] = {}

    async def init_redis(self):
        logger.info("🔌 Memory-optimized cache ready (no Redis dependency)")

    def generate_cache_key(self, query: str, model: str, user_id: str = "default") -> str:
        normalized_query = query.strip().lower()
        combined = f"{user_id}:{model}:{normalized_query}"
        return f"luna:mem:{hashlib.sha256(combined.encode()).hexdigest()}"

    def determine_ttl(self, query_type: str, model: str) -> int:
        """Smart TTL for different query types"""
        ttl_map = {
            "simple_chat": 86400,      # 24 hours - stable responses
            "instagram_research": 600, # 10 minutes - fresh data needed
            "competitor_analysis": 1800, # 30 minutes - moderate freshness
            "coding": 43200,           # 12 hours - solutions stable
            "general": 3600            # 1 hour - default
        }
        base_ttl = ttl_map.get(query_type, 3600)
        
        # Adjust for research models
        if "research" in model or "parallel" in model:
            base_ttl = min(base_ttl, 1800)
        elif "phi-3-mini" in model:
            base_ttl *= 1.5  # Simple responses cache longer
            
        return base_ttl

    async def get_cached_response(self, cache_key: str) -> Optional[Dict[Any, Any]]:
        start_time = time.perf_counter()
        
        with self.l1_lock:
            if cache_key in self.l1_cache:
                cached_item = self.l1_cache[cache_key]
                
                # Check if item is still valid (TTL-based)
                if time.time() - cached_item["cached_at"] < cached_item["ttl"]:
                    self.cache_hits += 1
                    self.total_cost_saved += 0.02  # Estimate $0.02 saved per hit
                    
                    response = cached_item["data"].copy()
                    response["cache_level"] = "Memory"
                    response["cached"] = True
                    response["cache_age"] = int(time.time() - cached_item["cached_at"])
                    
                    logger.info(f"🎯 Cache HIT: {cache_key[:16]}... ({time.perf_counter() - start_time:.3f}s)")
                    return response
                else:
                    # Expired, remove from cache
                    del self.l1_cache[cache_key]
        
        self.cache_misses += 1
        logger.info(f"❌ Cache MISS: {cache_key[:16]}...")
        return None

    async def set_cached_response(self, cache_key: str, response: Dict[Any, Any], 
                                query_type: str, model: str) -> None:
        ttl = self.determine_ttl(query_type, model)
        
        cache_item = {
            "data": response.copy(),
            "cached_at": time.time(),
            "ttl": ttl,
            "query_type": query_type,
            "model_used": model
        }
        
        with self.l1_lock:
            self.l1_cache[cache_key] = cache_item
        
        logger.info(f"💾 Cached: {cache_key[:16]}... (TTL: {ttl}s)")

    def store_query_response(self, user_id: str, query: str, response: str) -> None:
        """Persist user-specific query/response for lightweight memory."""
        if not user_id:
            return

        history = self.user_histories.setdefault(user_id, [])
        history.append(
            {
                "query": query,
                "response": response,
                "timestamp": time.time(),
            }
        )

        # Trim history to latest 20 entries per user to bound memory usage
        if len(history) > 20:
            del history[:-20]

    def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Return recorded history for a user."""
        return list(self.user_histories.get(user_id, []))

    def get_cache_stats(self) -> Dict[str, Any]:
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_size": len(self.l1_cache),
            "cache_type": "Memory Only (Production Ready)",
            "total_requests": total_requests,
            "estimated_cost_saved": round(self.total_cost_saved, 2),
            "cache_effectiveness": "High" if hit_rate > 60 else "Medium" if hit_rate > 30 else "Building"
        }

    async def close(self):
        stats = self.get_cache_stats()
        logger.info(f"👋 Cache closed. Final stats: {stats['hit_rate_percent']:.1f}% hit rate, ${stats['estimated_cost_saved']:.2f} saved")

# Global instance
enhanced_cache_manager = WorkingLunaCacheManager()
