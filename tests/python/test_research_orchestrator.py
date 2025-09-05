from __future__ import annotations

import asyncio
import os
import pytest

from integration.research_tools.orchestrator import LunaResearchOrchestrator


@pytest.mark.asyncio
async def test_conduct_raw_insights_fitness_monkeypatched_env(monkeypatch):
    # Ensure no API keys required to run (tools have graceful stubs)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("SCRAPEDO_API_KEY", raising=False)
    monkeypatch.delenv("APIFY_TOKEN", raising=False)

    orch = LunaResearchOrchestrator()
    insights = await orch.conduct_raw_insights(
        niche="fitness",
        goal="Grow followers by 20% in 60 days",
        research_types=["trends", "trends_realtime", "strategies", "success_stories", "creators"],
    )

    # Expect at least stubbed insights when keys are missing
    assert isinstance(insights, list)
    assert all(hasattr(i, "source") and hasattr(i, "insight") for i in insights)


@pytest.mark.asyncio
async def test_conduct_comprehensive_research_has_synthesized(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("SCRAPEDO_API_KEY", raising=False)
    monkeypatch.delenv("APIFY_TOKEN", raising=False)

    orch = LunaResearchOrchestrator()
    out = await orch.conduct_comprehensive_research(niche="fitness", goal="Grow followers by 20% in 60 days")

    assert isinstance(out, dict)
    assert "raw_insights" in out
    assert "synthesized" in out
    assert isinstance(out["raw_insights"], list)
    # synthesized can be empty depending on stubs, but structure should exist


@pytest.mark.asyncio
async def test_provider_fallback_when_no_insights(monkeypatch):
    # Force providers to return empty and verify fallback to tavily_basic is attempted
    orch = LunaResearchOrchestrator()

    async def empty_trends(topic: str):
        return []

    async def empty_blogs(topic: str):
        return []

    async def empty_reddit(niche: str):
        return []

    async def empty_youtube(niche: str):
        return []

    # Patch providers to return no results
    orch.providers["tavily"].search_trends = empty_trends  # type: ignore
    orch.providers["scrapedo"].deep_crawl_blogs = empty_blogs  # type: ignore
    orch.providers["apify"].scrape_reddit_success_stories = empty_reddit  # type: ignore
    orch.providers["apify"].analyze_youtube_creators = empty_youtube  # type: ignore

    # Patch fallback provider to return a stub
    async def fallback_stub(niche: str):
        from integration.models import ResearchInsight
        return [ResearchInsight(source="tavily_basic", insight="fallback trend", confidence=0.4)]

    orch.providers["tavily_basic"].search_instagram_trends = fallback_stub  # type: ignore

    insights = await orch.conduct_raw_insights(
        niche="fitness",
        goal="Grow followers by 20% in 60 days",
        research_types=["trends", "strategies", "success_stories", "creators"],
    )

    assert any(i.source == "tavily_basic" for i in insights)
