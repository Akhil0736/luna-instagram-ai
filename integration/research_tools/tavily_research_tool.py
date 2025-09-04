from __future__ import annotations

import os
import asyncio
from typing import List, Dict, Any, Optional

import aiohttp

from integration.models import ResearchInsight
from .base import ResearchTool


DEFAULT_INCLUDE_DOMAINS = [
    # Community and forums
    "reddit.com", "www.reddit.com",
    "quora.com", "www.quora.com",
    "stackoverflow.com",
    # Video platforms
    "youtube.com", "www.youtube.com",
    # Blogs and articles
    "medium.com", "www.medium.com",
    "substack.com",
    "blogspot.com",
    # Social media and tools
    "later.com", "buffer.com", "hootsuite.com",
    # General web
    "google.com", "news.google.com",
]


class EnhancedTavilyResearchTool(ResearchTool):
    """
    Enhanced Tavily integration configured for deep research across the web.

    - Parallelizes multi-query search
    - Requests deeper search (where supported)
    - Returns structured ResearchInsight with confidence scoring
    - Extracts top findings and metadata (titles/urls/snippets)
    """

    name = "tavily_enhanced"

    def __init__(
        self,
        api_key: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        max_results: int = 10,
        search_depth: str = "advanced",  # basic | advanced
        timeout_s: int = 30,
    ) -> None:
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.include_domains = include_domains or DEFAULT_INCLUDE_DOMAINS
        self.max_results = max_results
        self.search_depth = search_depth
        self.timeout_s = timeout_s

    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        if not self.api_key:
            # fallback stub for dev
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
                        insight=f"Search failed for '{q}': {res}",
                        confidence=0.3,
                        metadata={"error": True},
                    )
                )
                continue

            # Aggregate top titles/urls as succinct insight
            top_titles = "; ".join((r.get("title") or r.get("url", "")).strip() for r in res[:5] if r)
            confidence = self._estimate_confidence(res)
            insights.append(
                ResearchInsight(
                    source=self.name,
                    insight=f"Key findings for '{q}': {top_titles}",
                    confidence=confidence,
                    metadata={"results": res, "query": q},
                )
            )
        return insights

    async def _search_query(self, session: aiohttp.ClientSession, query: str) -> List[Dict[str, Any]]:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": self.max_results,
            "search_depth": self.search_depth,
            "include_domains": self.include_domains,
            # Prefer recent content where possible
            "days": 365,  # last year focus (2024-2025 window)
        }
        headers = {"Content-Type": "application/json"}
        async with session.post(url, json=payload, headers=headers, timeout=self.timeout_s) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("results", [])

    def _estimate_confidence(self, results: List[Dict[str, Any]]) -> float:
        if not results:
            return 0.3
        # Simple heuristic: more sources and presence of known domains -> higher confidence
        score = 0.4
        urls = [r.get("url", "") for r in results]
        domain_hits = sum(any(d in (u or "") for d in self.include_domains) for u in urls)
        diversity = len({(u.split("/")[2] if "/" in u else u) for u in urls if u})
        score += min(0.3, 0.03 * domain_hits)
        score += min(0.3, 0.02 * diversity)
        return round(min(0.95, score), 2)
