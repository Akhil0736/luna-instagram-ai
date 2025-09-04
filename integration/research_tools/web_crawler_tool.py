from __future__ import annotations

import asyncio
import re
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import aiohttp
from bs4 import BeautifulSoup

from integration.models import ResearchInsight
from .base import ResearchTool


TARGET_SITES = [
    # Growth forums / communities / blogs likely discussing Instagram growth
    "https://www.reddit.com/r/Instagram/",
    "https://www.reddit.com/r/InstagramMarketing/",
    "https://www.quora.com/",
    "https://medium.com/",
    "https://buffer.com/resources/",
    "https://later.com/blog/",
    "https://hootsuite.com/resources",
]

USER_AGENT = "LunaResearchBot/0.1 (+https://example.com/bot)"


@dataclass
class CrawlResult:
    url: str
    title: Optional[str]
    snippet: Optional[str]


class WebCrawlerTool(ResearchTool):
    """
    Polite, targeted async crawler to fetch and extract text from known sources.
    - Respects robots.txt
    - Limits concurrency
    - Extracts title/snippets
    """

    name = "web_crawler"

    def __init__(self, max_concurrency: int = 5, per_host_delay: float = 1.0, timeout_s: int = 20) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.per_host_delay = per_host_delay
        self.timeout_s = timeout_s
        self._last_req_time: Dict[str, float] = {}

    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        # Generate candidate URLs from target sites + queries (simple heuristic)
        candidate_urls = self._generate_candidate_urls(queries)
        async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
            tasks = [self._fetch_and_extract(session, url) for url in candidate_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        insights: List[ResearchInsight] = []
        for res in results:
            if isinstance(res, Exception) or res is None:
                continue
            insight_text = f"{res.title or res.url}: {res.snippet or ''}"
            insights.append(
                ResearchInsight(
                    source=self.name,
                    insight=insight_text.strip(),
                    confidence=0.5,
                    metadata={"url": res.url, "title": res.title},
                )
            )
        return insights

    def _generate_candidate_urls(self, queries: List[str]) -> List[str]:
        urls: List[str] = []
        for base in TARGET_SITES:
            for q in queries:
                keyword = re.sub(r"\s+", "+", q)
                if "reddit.com" in base:
                    urls.append(f"{base}search?q={keyword}&restrict_sr=1")
                elif "quora.com" in base:
                    urls.append(f"{base}search?q={keyword}")
                elif "medium.com" in base:
                    urls.append(f"{base}search?q={keyword}")
                else:
                    urls.append(base)
        # Deduplicate
        seen = set()
        deduped = []
        for u in urls:
            if u not in seen:
                deduped.append(u)
                seen.add(u)
        return deduped[:50]

    async def _fetch_and_extract(self, session: aiohttp.ClientSession, url: str) -> Optional[CrawlResult]:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if not self._allowed_by_robots(base, url):
            return None
        await self._respect_rate_limit(parsed.netloc)

        async with self.semaphore:
            try:
                async with session.get(url, timeout=self.timeout_s) as resp:
                    if resp.status != 200 or not resp.headers.get("content-type", "").startswith("text"):
                        return None
                    text = await resp.text(errors="ignore")
                    title, snippet = self._extract_text(text)
                    return CrawlResult(url=url, title=title, snippet=snippet)
            except Exception:
                return None

    def _allowed_by_robots(self, base: str, url: str) -> bool:
        try:
            rp = robotparser.RobotFileParser()
            rp.set_url(urljoin(base, "/robots.txt"))
            rp.read()
            return rp.can_fetch(USER_AGENT, url)
        except Exception:
            return False

    async def _respect_rate_limit(self, host: str) -> None:
        last = self._last_req_time.get(host, 0)
        now = time.time()
        elapsed = now - last
        if elapsed < self.per_host_delay:
            await asyncio.sleep(self.per_host_delay - elapsed)
        self._last_req_time[host] = time.time()

    def _extract_text(self, html: str) -> tuple[Optional[str], Optional[str]]:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        # Basic heuristic: first paragraph of meaningful length
        paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        snippet = next((p for p in paras if len(p) > 80), (paras[0] if paras else None))
        return title, snippet
