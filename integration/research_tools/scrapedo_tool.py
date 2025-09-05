from __future__ import annotations

import os
import re
import time
import json
from typing import List, Dict, Any, Tuple

import asyncio
import aiohttp
from bs4 import BeautifulSoup

from integration.models import ResearchInsight
from .base import ResearchTool


class ScrapeDoResearchTool(ResearchTool):
    """
    Advanced Scrape.do-based crawler and extractor for blogs, forums, and stories.

    Features:
    - Deep crawl with optional headless rendering for JS-heavy sites
    - Proxy rotation / anti-bot mode (delegated to Scrape.do provider)
    - Automatic CAPTCHA bypass (best-effort via provider options)
    - Metrics extraction: follower counts, engagement rates, growth timelines
    - Credibility scoring and source validation
    - Simple in-memory TTL caching and rate limiting
    """

    name = "scrapedo"

    def __init__(self) -> None:
        self.api_key = os.getenv("SCRAPEDO_API_KEY")
        # In-memory TTL cache: key -> (expires_at, text)
        self._cache: Dict[str, Tuple[float, str]] = {}
        self._cache_ttl = 600  # 10 minutes
        # Rate limit: max 5 concurrent; min 0.3s between calls
        self._sem = asyncio.Semaphore(5)
        self._min_interval = 0.3
        self._last_call = 0.0
        # Configurable credibility priors and recency weight
        self._priors = self._load_priors()
        self._recency_weight = self._load_recency_weight()

    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        # Generic research variant for compatibility with ResearchTool
        results: List[ResearchInsight] = []
        for q in queries:
            items = await self.deep_crawl_blogs(q)
            results.extend(items)
        return results

    async def deep_crawl_blogs(self, topic: str) -> List[ResearchInsight]:
        """Crawl and extract key insights from blogs relevant to a topic."""
        if not self.api_key:
            return [self._stub_insight(f"Deep crawl (blogs) for: {topic}")]

        search_url = f"https://www.google.com/search?q={topic} instagram growth"
        html = await self._fetch(search_url, render=True, use_proxy=True)
        if html is None:
            return [self._error_insight(f"Failed to fetch SERP for '{topic}'")]

        soup = BeautifulSoup(html, "html.parser")
        links = self._extract_links_from_serp(soup)
        if not links:
            return [self._error_insight(f"No links discovered for '{topic}'")] 

        insights: List[ResearchInsight] = []
        # Fetch top N links in parallel
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch(url, render=True, use_proxy=True, session=session) for url in links[:5]]
            pages = await asyncio.gather(*tasks, return_exceptions=True)
        for url, page in zip(links[:5], pages):
            if isinstance(page, Exception) or page is None:
                insights.append(self._error_insight(f"Failed to fetch {url}", extra={"url": url}))
                continue
            content_text = self._extract_text(page)
            structured = self._extract_structured(url, page)
            metrics = self._extract_metrics(content_text)
            cred = self._credibility_score(url, content_text, structured)
            summary = self._summarize_text(content_text)
            insights.append(
                ResearchInsight(
                    source=self.name,
                    insight=f"Blog: {summary}",
                    confidence=cred,
                    metadata={"url": url, "metrics": metrics, "credibility": cred, "structured": structured},
                )
            )
        return insights

    async def crawl_growth_forums(self, niche: str) -> List[ResearchInsight]:
        if not self.api_key:
            return [self._stub_insight(f"Forum crawl for: {niche}")]
        targets = [
            f"https://www.reddit.com/r/Instagram/search/?q={niche}%20growth&sort=new",
            f"https://www.reddit.com/r/InstagramMarketing/search/?q={niche}%20growth&sort=new",
            f"https://www.quora.com/search?q={niche}%20Instagram%20growth",
        ]
        async with aiohttp.ClientSession() as session:
            pages = await asyncio.gather(
                *(self._fetch(u, render=True, use_proxy=True, session=session) for u in targets),
                return_exceptions=True,
            )
        insights: List[ResearchInsight] = []
        for url, page in zip(targets, pages):
            if isinstance(page, Exception) or page is None:
                insights.append(self._error_insight(f"Failed to fetch forum {url}", extra={"url": url}))
                continue
            text = self._extract_text(page)
            structured = self._extract_structured(url, page)
            metrics = self._extract_metrics(text)
            cred = self._credibility_score(url, text, structured)
            snippet = self._summarize_text(text)
            insights.append(
                ResearchInsight(
                    source=self.name,
                    insight=f"Forum: {snippet}",
                    confidence=cred,
                    metadata={"url": url, "metrics": metrics, "credibility": cred, "structured": structured},
                )
            )
        return insights

    async def fetch_success_stories(self, niche: str) -> List[ResearchInsight]:
        if not self.api_key:
            return [self._stub_insight(f"Success stories for: {niche}")]
        targets = [
            f"https://www.google.com/search?q={niche}+instagram+success+story+case+study",
            f"https://medium.com/search?q={niche}%20instagram%20growth%20case%20study",
            f"https://www.youtube.com/results?search_query={niche}+instagram+growth+case+study",
        ]
        insights: List[ResearchInsight] = []
        async with aiohttp.ClientSession() as session:
            pages = await asyncio.gather(
                *(self._fetch(u, render=True, use_proxy=True, session=session) for u in targets),
                return_exceptions=True,
            )
        for url, page in zip(targets, pages):
            if isinstance(page, Exception) or page is None:
                insights.append(self._error_insight(f"Failed to fetch listing {url}", extra={"url": url}))
                continue
            text = self._extract_text(page)
            structured = self._extract_structured(url, page)
            metrics = self._extract_metrics(text)
            cred = self._credibility_score(url, text, structured)
            snippet = self._summarize_text(text)
            insights.append(
                ResearchInsight(
                    source=self.name,
                    insight=f"Success: {snippet}",
                    confidence=cred,
                    metadata={"url": url, "metrics": metrics, "credibility": cred, "structured": structured},
                )
            )
        return insights

    async def deep_extraction_scan(self, niche: str) -> Dict[str, Any]:
        """Run a Scrape.do-only deep scan and return a structured JSON report.
        Includes metrics, credibility and per-domain structured fields.
        """
        if not self.api_key:
            # Return a stubbed structure preserving the shape
            return {
                "niche": niche,
                "items": [
                    {
                        "source_type": "stub",
                        "url": "",
                        "title": "Stubbed deep scan",
                        "metrics": {},
                        "credibility": 0.45,
                        "structured": {},
                    }
                ],
                "notes": "SCRAPEDO_API_KEY not set; returning stubbed scan.",
            }

        blogs = await self.deep_crawl_blogs(f"{niche} Instagram strategies")
        forums = await self.crawl_growth_forums(niche)
        stories = await self.fetch_success_stories(niche)

        def to_item(ri: ResearchInsight, source_type: str) -> Dict[str, Any]:
            return {
                "source_type": source_type,
                "url": ri.metadata.get("url"),
                "title": ri.metadata.get("title"),
                "metrics": ri.metadata.get("metrics", {}),
                "credibility": ri.metadata.get("credibility", ri.confidence),
                "structured": ri.metadata.get("structured", {}),
                "insight": ri.insight,
            }

        items = [
            *(to_item(b, "blog") for b in blogs),
            *(to_item(f, "forum") for f in forums),
            *(to_item(s, "success") for s in stories),
        ]
        return {"niche": niche, "items": items}

    # --------------------- Internals ---------------------

    async def _fetch(
        self,
        url: str,
        *,
        render: bool = False,
        use_proxy: bool = False,
        session: aiohttp.ClientSession | None = None,
    ) -> str | None:
        """Fetch a URL via Scrape.do with options. Returns HTML text or None."""
        if not self.api_key:
            return None
        cache_key = f"{url}|r={int(render)}|p={int(use_proxy)}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached
        params = {
            "api_key": self.api_key,
            "url": url,
            # Common provider options (names subject to provider API):
            "render": "true" if render else "false",
            "premium": "true" if use_proxy else "false",
            "antibot": "true",  # enable anti-bot/captcha handling if supported
            "country": "US",
        }
        close_session = False
        if session is None:
            session = aiohttp.ClientSession()
            close_session = True
        try:
            async with self._sem:
                await self._respect_rate()
                async with session.get("https://api.scrape.do/v1/fetch", params=params, timeout=30) as resp:
                    resp.raise_for_status()
                    text = await resp.text()
                    self._cache_set(cache_key, text)
                    return text
        except Exception:
            return None
        finally:
            if close_session:
                await session.close()

    def _extract_links_from_serp(self, soup: BeautifulSoup) -> List[str]:
        links: List[str] = []
        for a in soup.select("a"):
            href = a.get("href") or ""
            if href.startswith("http") and "google" not in href:
                links.append(href)
        # de-duplicate while preserving order
        seen = set()
        uniq = []
        for u in links:
            if u not in seen:
                uniq.append(u)
                seen.add(u)
        return uniq

    def _extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        # Remove script/style
        for bad in soup(["script", "style", "noscript"]):
            bad.decompose()
        text = " ".join(t.strip() for t in soup.get_text(" ").split())
        return text[:20000]  # cap to 20k chars

    def _page_title(self, html: str) -> str | None:
        try:
            soup = BeautifulSoup(html, "html.parser")
            if soup.title and soup.title.text:
                return soup.title.text.strip()[:200]
        except Exception:
            pass
        return None

    def _extract_metrics(self, text: str) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}
        # Follower counts like 10k, 250,000 etc
        followers = re.findall(r"(\d{1,3}(?:[\.,]\d{3})+|\d+(?:k|K|m|M))\s*(?:followers|subs|fans)", text)
        if followers:
            metrics["followers_mentions"] = followers[:10]
        # Engagement rates like 2.5%, 7%
        erates = re.findall(r"(\d+(?:\.\d+)?)\s*%\s*(?:engagement|ER)", text, flags=re.I)
        if erates:
            metrics["engagement_rate_mentions"] = erates[:10]
        # Timelines: 30 days, 60 days, weeks, months
        timelines = re.findall(r"(\d{1,3})\s*(?:days|day|weeks?|months?)", text, flags=re.I)
        if timelines:
            metrics["timeline_mentions"] = timelines[:10]
        # Growth percentages like grew 20%
        growth = re.findall(r"(\d+(?:\.\d+)?)\s*%\s*(?:growth|increase)", text, flags=re.I)
        if growth:
            metrics["growth_rate_mentions"] = growth[:10]
        return metrics

    def _credibility_score(self, url: str, text: str, structured: Dict[str, Any] | None = None) -> float:
        # Prefer external CredibilityEngine if available
        try:
            from .credibility_engine import CredibilityEngine  # lazy import to avoid cycles
            if getattr(self, "_cred_engine", None) is None:
                self._cred_engine = CredibilityEngine()
            return float(self._cred_engine.score(url, text, structured or {}))
        except Exception:
            # Fallback to internal heuristic
            pass
        domain = url.lower()
        base = 0.5
        for k, v in self._priors.items():
            if k in domain:
                base = max(base, float(v))
        # Boost if many metrics detected
        metrics = self._extract_metrics(text)
        richness = len("".join([",".join(v) if isinstance(v, list) else str(v) for v in metrics.values()]))
        boost = 0.0
        if richness > 10:
            boost += 0.1
        if ("2024" in text or "2025" in text):
            boost += float(self._recency_weight)
        # Community validation boost (upvotes/claps/likes/comments/subscribers)
        try:
            sv = structured or {}
            # Collect possible signals
            up = _to_int_safe(sv.get("upvote_mentions", 0)) if isinstance(sv.get("upvote_mentions"), (int, float)) else _max_num(sv.get("upvote_mentions"))
            cm = _to_int_safe(sv.get("comment_mentions", 0)) if isinstance(sv.get("comment_mentions"), (int, float)) else _max_num(sv.get("comment_mentions"))
            cl = _to_int_safe(sv.get("clap_mentions", 0)) if isinstance(sv.get("clap_mentions"), (int, float)) else _max_num(sv.get("clap_mentions"))
            lk = _to_int_safe(sv.get("like_mentions", 0)) if isinstance(sv.get("like_mentions"), (int, float)) else _max_num(sv.get("like_mentions"))
            sub = _to_int_safe(sv.get("subscribers")) if sv.get("subscribers") is not None else 0
            # Heuristic thresholds
            if up and up >= 500:
                boost += 0.1
            if cl and cl >= 1000:
                boost += 0.1
            if lk and lk >= 1000:
                boost += 0.05
            if cm and cm >= 100:
                boost += 0.05
            if sub and sub >= 50000:
                boost += 0.05
        except Exception:
            pass
        return max(0.35, min(0.9, base + boost))

    def _load_priors(self) -> Dict[str, float]:
        env_val = os.getenv("SCRAPEDO_CREDIBILITY_PRIORS")
        default = {
            "medium.com": 0.6,
            "reddit.com": 0.55,
            "quora.com": 0.5,
            "backlinko.com": 0.8,
            "ahrefs.com": 0.8,
            "neilpatel.com": 0.7,
        }
        if not env_val:
            return default
        try:
            data = json.loads(env_val)
            if isinstance(data, dict):
                # Coerce to float values
                return {str(k): float(v) for k, v in data.items()}
        except Exception:
            pass
        return default

    def _load_recency_weight(self) -> float:
        val = os.getenv("SCRAPEDO_RECENCY_WEIGHT")
        try:
            if val is not None:
                return float(val)
        except Exception:
            pass
        return 0.1

    def _extract_structured(self, url: str, html: str) -> Dict[str, Any]:
        """Domain-aware structured extraction for higher-fidelity metrics."""
        url_l = url.lower()
        title = self._page_title(html)
        if "medium.com" in url_l:
            return self._extract_medium(html, title)
        if "reddit.com" in url_l:
            return self._extract_reddit(html, title)
        if "quora.com" in url_l:
            return self._extract_quora(html, title)
        if "youtube.com" in url_l or "youtu.be" in url_l:
            return self._extract_youtube(html, title)
        # Generic blog/case study pipeline as default
        return self._extract_blog(html, title)

    def _extract_medium(self, html: str, title: str | None) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        author = None
        date_published = None
        publication = None
        try:
            # Common meta tags on Medium
            m = soup.find("meta", {"name": "author"})
            if m and m.get("content"):
                author = m.get("content")
            dt = soup.find("meta", {"property": "article:published_time"})
            if dt and dt.get("content"):
                date_published = dt.get("content")
            site = soup.find("meta", {"property": "og:site_name"})
            if site and site.get("content"):
                publication = site.get("content")
        except Exception:
            pass
        text = self._extract_text(html)
        metrics = self._extract_metrics(text)
        # Clap counts often appear as "X claps"
        claps = re.findall(r"(\d+(?:\.\d+)?[kKmM]?)\s*claps", text, flags=re.I)
        return {
            "title": title,
            "author": author,
            "published": date_published,
            "publication": publication,
            "metrics": metrics,
            "clap_mentions": claps[:10],
        }

    def _extract_reddit(self, html: str, title: str | None) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        # Try to extract upvote counts and comment counts heuristically
        text = self._extract_text(html)
        upvotes = re.findall(r"(\d+(?:\.\d+)?[kK]?)\s*(?:upvotes|points|karma)", text, flags=re.I)
        comments = re.findall(r"(\d+(?:\.\d+)?[kK]?)\s*comments", text, flags=re.I)
        posts = []
        for h in soup.select("h3, h2"):
            t = h.get_text(strip=True)
            if t:
                posts.append(t[:140])
        return {
            "title": title,
            "posts_sample": posts[:10],
            "upvote_mentions": upvotes[:10],
            "comment_mentions": comments[:10],
            "community_validation": {
                "max_upvotes": _max_num(upvotes),
                "max_comments": _max_num(comments),
            },
        }

    def _extract_quora(self, html: str, title: str | None) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        q_titles = [a.get_text(strip=True)[:160] for a in soup.select("a") if a.get("href", "").startswith("/q/")]
        return {"title": title, "questions_sample": q_titles[:10]}

    def _extract_youtube(self, html: str, title: str | None) -> Dict[str, Any]:
        text = self._extract_text(html)
        # Subscriber counts and likes/comments are often present as text in pre-rendered HTML of Scrape.do
        subs = re.findall(r"(\d+(?:\.\d+)?[kKmM]?)\s*subscribers", text, flags=re.I)
        likes = re.findall(r"(\d+(?:\.\d+)?[kKmM]?)\s*likes", text, flags=re.I)
        comments = re.findall(r"(\d+(?:\.\d+)?[kKmM]?)\s*comments", text, flags=re.I)
        views = re.findall(r"(\d+(?:\.\d+)?[kKmM]?)\s*views", text, flags=re.I)
        # Tutorial steps: detect headings or lines starting with Step or numeric steps
        steps = re.findall(r"(?:^|\s)(?:Step\s*\d+\:|\d+\)\s)[^\n]{3,120}", text)
        return {
            "title": title,
            "subscribers": _max_num(subs),
            "like_mentions": likes[:10],
            "comment_mentions": comments[:10],
            "view_mentions": views[:10],
            "tutorial_steps_sample": [s.strip()[:160] for s in steps[:10]],
        }

    def _extract_blog(self, html: str, title: str | None) -> Dict[str, Any]:
        text = self._extract_text(html)
        metrics = self._extract_metrics(text)
        # Case study signals
        case_study = bool(re.search(r"case study|results|before and after|grew|increased", text, flags=re.I))
        tactics_sample = re.findall(r"(?:Tip|Tactic|Strategy)\s*\d+\:\s*[^\n]{3,120}", text)
        return {
            "title": title,
            "case_study": case_study,
            "metrics": metrics,
            "tactics_sample": [t[:160] for t in tactics_sample[:10]],
        }

    def _summarize_text(self, text: str, max_len: int = 220) -> str:
        # crude summary: first meaningful chunk
        snippet = text[:max_len].strip()
        return snippet + ("..." if len(text) > max_len else "")

    def _stub_insight(self, msg: str) -> ResearchInsight:
        return ResearchInsight(
            source=self.name,
            insight=f"[Stub] {msg}",
            confidence=0.45,
            metadata={"stub": True},
        )

    def _error_insight(self, msg: str, *, extra: Dict[str, Any] | None = None) -> ResearchInsight:
        return ResearchInsight(
            source=self.name,
            insight=msg,
            confidence=0.3,
            metadata={"error": True, **(extra or {})},
        )

    async def _respect_rate(self):
        now = time.time()
        elapsed = now - self._last_call
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_call = time.time()

def _to_int_safe(x: Any) -> int:
    try:
        return int(x)
    except Exception:
        return 0

def _parse_num_token(tok: str | int | float | None) -> int:
    if tok is None:
        return 0
    if isinstance(tok, (int, float)):
        return int(tok)
    s = str(tok).strip().lower()
    m = re.match(r"(\d+(?:\.\d+)?)([kKmM]?)", s)
    if not m:
        return 0
    val = float(m.group(1))
    suf = m.group(2).lower()
    if suf == "k":
        val *= 1_000
    elif suf == "m":
        val *= 1_000_000
    return int(val)

def _max_num(arr: Any) -> int:
    try:
        if not arr:
            return 0
        return max(_parse_num_token(x) for x in arr)
    except Exception:
        return 0
