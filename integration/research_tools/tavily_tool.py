from __future__ import annotations

import os
import time
from typing import List, Dict, Any, Tuple

import asyncio
import aiohttp

from integration.models import ResearchInsight
from .base import ResearchTool


class TavilyResearchTool(ResearchTool):
    """
    Lightweight wrapper over the Tavily Search API.
    Falls back to a stubbed response if TAVILY_API_KEY is not set.
    """

    name = "tavily"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        # Simple in-memory TTL cache: key -> (expires_at, results)
        self._cache: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}
        self._cache_ttl_seconds = 300  # 5 minutes default TTL
        # Rate limiting controls
        self._semaphore = asyncio.Semaphore(5)  # max concurrent Tavily calls
        self._min_interval = 0.25  # seconds between individual calls
        self._last_call_ts = 0.0

    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        if not self.api_key:
            # Fallback stubbed results to keep flows working in local/dev
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"Stubbed insight for: {q}",
                    confidence=0.4,
                    metadata={"stub": True},
                )
                for q in queries
            ]

        async with aiohttp.ClientSession() as session:
            tasks = [self._search_query(session, q) for q in queries]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        insights: List[ResearchInsight] = []
        for q, res in zip(queries, results):
            if isinstance(res, Exception):
                insights.append(
                    ResearchInsight(
                        source=self.name,
                        insight=f"Failed to fetch insights for: {q} ({res})",
                        confidence=0.2,
                        metadata={"error": True},
                    )
                )
            else:
                # collapse top results into a single summarized line per query
                top = "; ".join(r.get("title") or r.get("url", "") for r in res[:3])
                insights.append(
                    ResearchInsight(
                        source=self.name,
                        insight=f"Top findings for '{q}': {top}",
                        confidence=self._score_confidence(res),
                        metadata={"raw": res},
                    )
                )
        return insights

    async def _search_query(self, session: aiohttp.ClientSession, query: str):
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": 5,
            "search_depth": "basic",
        }
        headers = {"Content-Type": "application/json"}
        cache_key = self._cache_key(url, payload)
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        async with self._semaphore:
            await self._respect_rate_limit()
            async with session.post(url, json=payload, headers=headers, timeout=30) as resp:
                resp.raise_for_status()
                data = await resp.json()
                results = data.get("results", [])
                self._cache_set(cache_key, results)
                return results

    # ---------------- Instagram-specific fast helpers ----------------

    async def research_instagram_fast(self, queries: List[str]) -> List[ResearchInsight]:
        """Fast, lightweight searches optimized for real-time responsiveness."""
        if not self.api_key:
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"[Fast Stub] {q}",
                    confidence=0.35,
                    metadata={"stub": True, "mode": "fast"},
                )
                for q in queries
            ]
        async with aiohttp.ClientSession() as session:
            # Reduce depth and results to speed up
            async def fast_query(q: str):
                url = "https://api.tavily.com/search"
                payload = {
                    "api_key": self.api_key,
                    "query": q,
                    "max_results": 3,
                    "search_depth": "basic",
                }
                headers = {"Content-Type": "application/json"}
                cache_key = self._cache_key(url, payload)
                cached = self._cache_get(cache_key)
                if cached is not None:
                    return cached
                async with self._semaphore:
                    await self._respect_rate_limit()
                    async with session.post(url, json=payload, headers=headers, timeout=20) as resp:
                        resp.raise_for_status()
                        data = await resp.json()
                        results = data.get("results", [])
                        self._cache_set(cache_key, results)
                        return results

            results = await asyncio.gather(*(fast_query(q) for q in queries), return_exceptions=True)

        insights: List[ResearchInsight] = []
        for q, res in zip(queries, results):
            if isinstance(res, Exception):
                insights.append(
                    ResearchInsight(
                        source=self.name,
                        insight=f"Fast lookup failed for: {q} ({res})",
                        confidence=0.2,
                        metadata={"error": True, "mode": "fast"},
                    )
                )
            else:
                top = "; ".join(r.get("title") or r.get("url", "") for r in res[:2])
                insights.append(
                    ResearchInsight(
                        source=self.name,
                        insight=f"Fast findings for '{q}': {top}",
                        confidence=self._score_confidence(res, fast=True),
                        metadata={"raw": res, "mode": "fast"},
                    )
                )
        return insights

    async def search_instagram_trends(self, niche: str) -> List[ResearchInsight]:
        """Instagram-specific trend queries for the niche."""
        queries = [
            f"{niche} Instagram trending topics",
            f"{niche} Instagram reels trends 2025",
            f"trending hashtags {niche} instagram",
            f"{niche} instagram viral content now",
        ]
        return await self.research_instagram_fast(queries)

    async def monitor_real_time(
        self,
        keywords: List[str],
        *,
        duration_seconds: int = 60,
        poll_interval: int = 10,
    ) -> List[ResearchInsight]:
        """
        Polls Tavily quickly to capture evolving/trending results over a short window.
        Results are deduplicated and summarized per keyword.
        """
        if duration_seconds <= 0 or poll_interval <= 0:
            return []

        seen: Dict[str, Dict[str, Any]] = {}
        start = time.time()
        while time.time() - start < duration_seconds:
            batch = await self.research_instagram_fast(keywords)
            for ins in batch:
                # Deduplicate by top url/title string
                key = ins.insight
                if key not in seen or ins.confidence > seen[key]["confidence"]:
                    seen[key] = {
                        "insight": ins,
                        "confidence": ins.confidence,
                    }
            await asyncio.sleep(min(poll_interval, max(1, poll_interval)))

        # Return the unique, highest-confidence snapshots
        return [v["insight"] for v in seen.values()]

    # ---------------- Internals: caching, rate, scoring ----------------

    def _cache_key(self, url: str, payload: Dict[str, Any]) -> str:
        # Stable key for TTL cache
        return f"{url}|{payload.get('query')}|{payload.get('max_results')}|{payload.get('search_depth')}"

    def _cache_get(self, key: str) -> List[Dict[str, Any]] | None:
        item = self._cache.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            # expired
            self._cache.pop(key, None)
            return None
        return value

    def _cache_set(self, key: str, value: List[Dict[str, Any]]):
        self._cache[key] = (time.time() + self._cache_ttl_seconds, value)

    async def _respect_rate_limit(self):
        # Ensure minimal spacing between requests
        now = time.time()
        elapsed = now - self._last_call_ts
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_call_ts = time.time()

    def _score_confidence(self, results: List[Dict[str, Any]], fast: bool = False) -> float:
        if not results:
            return 0.3
        # Simple heuristic: more results + presence of recency hints boosts confidence
        count_score = min(1.0, len(results) / (3 if fast else 5))
        # If any result hints at recency
        recency_hint = any(
            any(k in (r.get("title") or "").lower() for k in ["2024", "2025", "today", "latest"]) for r in results
        )
        recency_score = 0.15 if recency_hint else 0.0
        base = 0.45 if fast else 0.55
        return max(0.3, min(0.9, base + count_score * 0.25 + recency_score))
