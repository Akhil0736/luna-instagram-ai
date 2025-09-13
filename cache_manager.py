import asyncio
import hashlib
import json
import time
import random
from typing import Optional, Dict, Any
from cachetools import LRUCache
import redis.asyncio as redis
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedLunaCacheManager:
    def __init__(self, redis_url: str = "redis://redis:6379", 
                 l1_cache_size: int = 256):
        
        self.redis_url = redis_url
        self.redis_client = None
        self.l1_cache = LRUCache(maxsize=l1_cache_size)
        self.l1_lock = threading.RLock()
        
        # Simple bloom filter implementation
        self.bloom_filter = set()
        
        # Metrics
        self.cache_hits = 0
        self.cache_misses = 0
        self.background_refreshes = 0
        
        # Concurrency controls
        self.refreshing_keys = set()
        self.refreshing_lock = threading.Lock()

    async def init_redis(self):
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            logger.info("🔌 Enhanced Luna cache connected to Redis")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise

    def generate_cache_key(self, query: str, model: str, user_id: str = "default") -> str:
        normalized_query = query.strip().lower()
        combined = f"{user_id}:{model}:{normalized_query}"
        return f"luna:enhanced:{hashlib.sha256(combined.encode()).hexdigest()}"

    def determine_ttl(self, query_type: str, model: str) -> int:
        ttl_map = {
            "simple_chat": 86400,
            "instagram_research": 600,
            "competitor_analysis": 1800,
            "coding": 43200,
            "general": 3600
        }
        base_ttl = ttl_map.get(query_type, 3600)
        if "research" in model or "parallel" in model:
            base_ttl = min(base_ttl, 1800)
        elif "phi-3-mini" in model:
            base_ttl *= 2
        return base_ttl

    async def get_cached_response(self, cache_key: str) -> Optional[Dict[Any, Any]]:
        start_time = time.perf_counter()
        with self.l1_lock:
            l1_response = self.l1_cache.get(cache_key)
        if l1_response:
            self.cache_hits += 1
            logger.info(f"🎯 L1 Cache HIT: {cache_key[:16]}... ({time.perf_counter() - start_time:.3f}s)")
            if self._should_refresh_background(l1_response):
                asyncio.create_task(self._background_refresh(cache_key, l1_response))
            l1_response["cache_level"] = "L1"
            l1_response["cached"] = True
            return l1_response
        if cache_key not in self.bloom_filter:
            self.cache_misses += 1
            logger.info(f"🌸 Bloom filter: definitely not cached {cache_key[:16]}...")
            return None
        if not self.redis_client:
            self.cache_misses += 1
            return None
        try:
            cached_data = await self.redis_client.get(cache_key)
            ttl_remaining = await self.redis_client.ttl(cache_key)
            if cached_data:
                self.cache_hits += 1
                cached_response = json.loads(cached_data)
                with self.l1_lock:
                    self.l1_cache[cache_key] = cached_response
                if self._should_refresh_background(cached_response, ttl_remaining):
                    asyncio.create_task(self._background_refresh(cache_key, cached_response))
                logger.info(f"🎯 L2 Cache HIT: {cache_key[:16]}... (TTL: {ttl_remaining}s)")
                cached_response["cache_level"] = "L2"
                cached_response["cached"] = True
                cached_response["ttl_remaining"] = ttl_remaining
                return cached_response
        except Exception as e:
            logger.warning(f"⚠️ Cache retrieval error: {e}")
        self.cache_misses += 1
        logger.info(f"❌ Cache MISS: {cache_key[:16]}... ({time.perf_counter() - start_time:.3f}s)")
        return None

    async def set_cached_response(self, cache_key: str, response: Dict[Any, Any], 
                                query_type: str, model: str) -> None:
        try:
            ttl = self.determine_ttl(query_type, model)
            cache_data = {
                **response,
                "cached_at": time.time(),
                "original_ttl": ttl,
                "query_type": query_type,
                "model_used": model
            }
            if self.redis_client:
                await self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(cache_data)
                )
            with self.l1_lock:
                self.l1_cache[cache_key] = cache_data
            self.bloom_filter.add(cache_key)
            logger.info(f"💾 Multi-tier cache stored: {cache_key[:16]}... (TTL: {ttl}s)")
        except Exception as e:
            logger.warning(f"⚠️ Cache storage error: {e}")

    def _should_refresh_background(self, cached_response: Dict[Any, Any], 
                                  ttl_remaining: Optional[int] = None) -> bool:
        original_ttl = cached_response.get("original_ttl", 3600)
        cached_at = cached_response.get("cached_at", time.time())
        age = time.time() - cached_at
        if ttl_remaining:
            return ttl_remaining < (original_ttl * 0.2)
        else:
            return age > (original_ttl * 0.8)

    async def _background_refresh(self, cache_key: str, cached_response: Dict[Any, Any]) -> None:
        with self.refreshing_lock:
            if cache_key in self.refreshing_keys:
                return
            self.refreshing_keys.add(cache_key)
        try:
            self.background_refreshes += 1
            logger.info(f"🔄 Background refresh triggered: {cache_key[:16]}...")
            await asyncio.sleep(0.1)  # TODO: Integrate with AI code
        except Exception as e:
            logger.warning(f"⚠️ Background refresh failed: {e}")
        finally:
            with self.refreshing_lock:
                self.refreshing_keys.remove(cache_key)

    def get_cache_stats(self) -> Dict[str, Any]:
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "l1_cache_size": len(self.l1_cache),
            "bloom_filter_size": len(self.bloom_filter),
            "background_refreshes": self.background_refreshes,
            "total_requests": total_requests
        }

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
        logger.info("👋 Enhanced cache manager closed")

enhanced_cache_manager = EnhancedLunaCacheManager()
