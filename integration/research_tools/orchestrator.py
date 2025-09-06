from __future__ import annotations

import asyncio
import logging
import time
from typing import List, Dict, Any

from integration.models import ResearchInsight
from .tavily_research_tool import EnhancedTavilyResearchTool
from .tavily_tool import TavilyResearchTool
from .scrapedo_tool import ScrapeDoResearchTool
from .apify_tool import ApifyResearchTool
from .synthesis_tool import SynthesisTool


class LunaResearchOrchestrator:
    """
    Orchestrates comprehensive research by running multiple providers in parallel
    and synthesizing their outputs into actionable intelligence specific to
    Instagram growth.
    """

    def __init__(self) -> None:
        self.providers = {
            "tavily": EnhancedTavilyResearchTool(),
            "tavily_basic": TavilyResearchTool(),
            "scrapedo": ScrapeDoResearchTool(),
            "apify": ApifyResearchTool(),
        }
        self.synthesizer = SynthesisTool()
        self.logger = logging.getLogger(__name__)
        # Semantic engine is optional: import lazily
        try:
            from integration.openmanus_service.semantic import EmbeddingsEngine  # type: ignore
            self._embed_engine = EmbeddingsEngine()
        except Exception:
            self._embed_engine = None

    async def conduct_comprehensive_research(self, niche: str, goal: str) -> Dict[str, Any]:
        """
        Run parallel research across all providers and synthesize findings.
        Returns both raw insights and synthesized patterns.
        """
        topic = f"{niche} Instagram growth 2025"
        tasks = [
            self.providers["tavily"].search_trends(topic),
            self.providers["scrapedo"].deep_crawl_blogs(f"{niche} Instagram strategies"),
            self.providers["apify"].scrape_reddit_success_stories(niche),
            self.providers["apify"].analyze_youtube_creators(niche),
        ]
        start = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)

        insights: List[ResearchInsight] = []
        for res in results:
            if isinstance(res, Exception):
                insights.append(
                    ResearchInsight(
                        source="orchestrator",
                        insight=f"Provider error: {res}",
                        confidence=0.3,
                        metadata={"error": True},
                    )
                )
            else:
                insights.extend(res)

        # Optional semantic prioritization by goal/niche
        insights = await self._prioritize_semantic(insights, query=goal)
        duration = time.time() - start
        self.logger.info("conduct_comprehensive_research completed: %d insights in %.2fs", len(insights), duration)
        if not insights:
            self.logger.warning("No insights from comprehensive research; falling back to tavily_basic trends")
            try:
                insights = await self.providers["tavily_basic"].search_instagram_trends(niche)
            except Exception as e:
                self.logger.exception("Fallback tavily_basic failed: %s", e)

        synthesized = self.synthesizer.synthesize(insights)
        return self.synthesize_intelligence(insights, synthesized, niche=niche, goal=goal)

    async def conduct_raw_insights(
        self,
        niche: str,
        goal: str,
        *,
        research_types: List[str] | None = None,
    ) -> List[ResearchInsight]:
        """
        Return a flat list of ResearchInsight from providers using smart query routing.
        research_types: optional hints like ["trends", "success_stories", "strategies"].
        """
        topic = f"{niche} Instagram growth 2025"
        tasks = []
        rtypes = set(research_types or ["trends", "strategies", "success_stories"]) 

        # Smart routing based on type hints
        if "trends" in rtypes:
            tasks.append(self.providers["tavily"].search_trends(topic))
        if "trends_realtime" in rtypes:
            tasks.append(self.providers["tavily_basic"].search_instagram_trends(niche))
        if "strategies" in rtypes:
            tasks.append(self.providers["scrapedo"].deep_crawl_blogs(f"{niche} Instagram strategies"))
            tasks.append(self.providers["scrapedo"].crawl_growth_forums(niche))
        if "success_stories" in rtypes:
            tasks.append(self.providers["apify"].scrape_reddit_success_stories(niche))
            tasks.append(self.providers["scrapedo"].fetch_success_stories(niche))
        if "creators" in rtypes or "youtube" in rtypes:
            tasks.append(self.providers["apify"].analyze_youtube_creators(niche))

        start = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)

        insights: List[ResearchInsight] = []
        for res in results:
            if isinstance(res, Exception):
                insights.append(
                    ResearchInsight(
                        source="orchestrator",
                        insight=f"Provider error: {res}",
                        confidence=0.3,
                        metadata={"error": True},
                    )
                )
            else:
                insights.extend(res)
        # Optional semantic prioritization by goal/niche
        insights = await self._prioritize_semantic(insights, query=goal)
        duration = time.time() - start
        self.logger.info("conduct_raw_insights completed: %d insights in %.2fs", len(insights), duration)
        if not insights:
            self.logger.warning("No insights from raw_insights; falling back to tavily_basic trends")
            try:
                insights = await self.providers["tavily_basic"].search_instagram_trends(niche)
            except Exception as e:
                self.logger.exception("Fallback tavily_basic failed: %s", e)
        return insights

    def synthesize_intelligence(
        self,
        insights: List[ResearchInsight],
        synthesized: List[Any],
        *,
        niche: str,
        goal: str,
    ) -> Dict[str, Any]:
        """Package raw and synthesized insights with context."""
        return {
            "niche": niche,
            "goal": goal,
            "raw_insights": [
                {
                    "source": i.source,
                    "insight": i.insight,
                    "confidence": i.confidence,
                    "metadata": i.metadata,
                }
                for i in insights
            ],
            "synthesized_insights": [
                {
                    "pattern": s.pattern,
                    "confidence": s.confidence,
                    "metadata": s.metadata,
                    "evidence": [
                        {
                            "source": e.source,
                            "insight": e.insight,
                            "confidence": e.confidence,
                            "metadata": e.metadata,
                        }
                        for e in s.evidence
                    ],
                }
                for s in synthesized
            ],
        }
