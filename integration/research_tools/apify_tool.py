from __future__ import annotations

import os
from typing import List

import aiohttp

from integration.models import ResearchInsight


class ApifyResearchTool:
    """
    Apify-based research tool (stubbed).
    Provides helpers to scrape Reddit success stories and analyze YouTube creators.

    If APIFY_TOKEN is missing, returns stubbed insights to keep flows working.
    """

    name = "apify"

    def __init__(self) -> None:
        self.token = os.getenv("APIFY_TOKEN")

    async def scrape_reddit_success_stories(self, niche: str) -> List[ResearchInsight]:
        if not self.token:
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"[Stub] Reddit success stories for {niche}: creator grew 20% in 60 days using daily reels and community engagement.",
                    confidence=0.55,
                    metadata={"platform": "reddit", "niche": niche, "stub": True},
                )
            ]
        # Example pseudo-call to Apify actor (not executed without token)
        url = "https://api.apify.com/v2/acts/apify~reddit-scraper/run-sync?timeout=120000"
        payload = {
            "token": self.token,
            "body": {
                "search": f"{niche} instagram growth success",
                "maxItems": 20,
                "subreddit": ["Instagram", "InstagramMarketing"],
            },
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=60) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    items = data.get("items", [])
                    top = "; ".join((it.get("title") or it.get("url", "")) for it in items[:5])
                    return [
                        ResearchInsight(
                            source=self.name,
                            insight=f"Reddit findings for {niche}: {top}",
                            confidence=0.65,
                            metadata={"platform": "reddit", "raw_count": len(items)},
                        )
                    ]
        except Exception as e:
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"Apify Reddit scrape failed: {e}",
                    confidence=0.3,
                    metadata={"error": True},
                )
            ]

    async def analyze_youtube_creators(self, niche: str) -> List[ResearchInsight]:
        if not self.token:
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"[Stub] YouTube creators in {niche}: consistent shorts + collaborations drive follower growth on IG via cross-promotion.",
                    confidence=0.55,
                    metadata={"platform": "youtube", "niche": niche, "stub": True},
                )
            ]
        # Example pseudo-call to a YouTube scraping actor
        url = "https://api.apify.com/v2/acts/someone~youtube-scraper/run-sync?timeout=120000"
        payload = {"token": self.token, "body": {"search": f"{niche} growth strategy", "maxItems": 10}}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=60) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    items = data.get("items", [])
                    top = "; ".join((it.get("title") or it.get("url", "")) for it in items[:5])
                    return [
                        ResearchInsight(
                            source=self.name,
                            insight=f"YouTube creator analysis for {niche}: {top}",
                            confidence=0.6,
                            metadata={"platform": "youtube", "raw_count": len(items)},
                        )
                    ]
        except Exception as e:
            return [
                ResearchInsight(
                    source=self.name,
                    insight=f"Apify YouTube scrape failed: {e}",
                    confidence=0.3,
                    metadata={"error": True},
                )
            ]
