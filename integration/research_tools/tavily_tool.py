from __future__ import annotations

import os
from typing import List

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
                        confidence=0.6,
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
        async with session.post(url, json=payload, headers=headers, timeout=30) as resp:
            resp.raise_for_status()
            data = await resp.json()
            # Expected shape: { results: [{title, url, content,...}, ...] }
            return data.get("results", [])
