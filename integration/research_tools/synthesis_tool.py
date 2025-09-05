from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Any

from integration.models import ResearchInsight


@dataclass
class SynthesizedInsight:
    pattern: str
    evidence: List[ResearchInsight]
    confidence: float
    metadata: Dict[str, Any]


class SynthesisTool:
    """
    Content Synthesis Engine
    - Collapses raw insights into actionable patterns
    - Estimates confidence from source credibility, diversity, and recency when available
    - Extracts metrics/timelines if present in text heuristically
    """

    # crude credibility priors by source
    SOURCE_PRIOR: Dict[str, float] = {
        "tavily": 0.55,
        "tavily_enhanced": 0.65,
        "web_crawler": 0.5,
        "reddit": 0.55,
        "youtube": 0.55,
        "medium": 0.6,
        "quora": 0.5,
        "later.com": 0.7,
        "buffer.com": 0.7,
        "hootsuite.com": 0.7,
    }

    def synthesize(self, insights: List[ResearchInsight]) -> List[SynthesizedInsight]:
        if not insights:
            return []

        # 1) Cluster by coarse themes using keyword buckets
        buckets: Dict[str, List[ResearchInsight]] = defaultdict(list)
        for i in insights:
            text = self._get_insight_text(i)
            buckets[self._theme_of(text)].append(i)

        # 2) For each bucket, calculate confidence and extract metrics
        synthesized: List[SynthesizedInsight] = []
        for theme, items in buckets.items():
            conf = self._aggregate_confidence(items)
            meta = self._extract_metrics(items)
            synthesized.append(SynthesizedInsight(
                pattern=theme,
                evidence=items[:8],  # cap to keep payload tight
                confidence=round(conf, 2),
                metadata=meta,
            ))
        # sort by confidence desc
        synthesized.sort(key=lambda x: x.confidence, reverse=True)
        return synthesized

    def _theme_of(self, text: str) -> str:
        t = text.lower()
        if any(k in t for k in ["hashtag", "tags", "#"]):
            return "Hashtag strategy"
        if any(k in t for k in ["time to post", "best time", "posting time", "schedule"]):
            return "Optimal posting times"
        if any(k in t for k in ["engage", "comment", "reply", "dm", "outreach"]):
            return "Engagement tactics"
        if any(k in t for k in ["reel", "short", "video", "carousel", "photo"]):
            return "Content types that work"
        if any(k in t for k in ["automation", "rate limit", "safe actions", "daily limit"]):
            return "Safe automation"
        return "General growth insights"

    def _aggregate_confidence(self, items: List[ResearchInsight]) -> float:
        if not items:
            return 0.4
        # combine confidences with source priors and diversity bonus
        priors = []
        sources = set()
        for i in items:
            source = self._get_source(i)
            sources.add(source)
            prior = 0.55
            # URL-based prior if present
            meta = self._get_metadata(i)
            url = str(meta.get("url", "")) if isinstance(meta, dict) else ""
            domain_prior = next((self.SOURCE_PRIOR[d] for d in self.SOURCE_PRIOR if d in url), None)
            prior = domain_prior or self.SOURCE_PRIOR.get(source, prior)
            conf = self._get_confidence(i)
            priors.append((conf) * 0.6 + prior * 0.4)
        base = sum(priors) / max(1, len(priors))
        diversity_bonus = min(0.2, 0.03 * len(sources))
        return min(0.95, base + diversity_bonus)

    def _extract_metrics(self, items: List[ResearchInsight]) -> Dict[str, Any]:
        # very lightweight heuristic extraction
        metrics: Dict[str, Any] = {"mentions": 0}
        for i in items:
            txt = self._get_insight_text(i).lower()
            if any(k in txt for k in ["30 days", "60 days", "90 days", "weeks", "timeline"]):
                metrics.setdefault("timelines", []).append(self._get_insight_text(i))
            if any(k in txt for k in ["%", "growth", "increase", "engagement rate", "followers/day"]):
                metrics.setdefault("metrics", []).append(self._get_insight_text(i))
            metrics["mentions"] += 1
        return metrics

    # --------- Safe accessors to support dicts or objects ----------
    def _get_insight_text(self, item: ResearchInsight) -> str:
        try:
            text = getattr(item, "insight", None)
            if text:
                return str(text)
            if isinstance(item, dict):
                return str(item.get("insight") or item.get("text") or item.get("summary") or item)
        except Exception:
            pass
        return str(item)

    def _get_source(self, item: ResearchInsight) -> str:
        try:
            src = getattr(item, "source", None)
            if src:
                return str(src)
            if isinstance(item, dict):
                return str(item.get("source") or item.get("provider") or item.get("origin") or "unknown")
        except Exception:
            pass
        return "unknown"

    def _get_confidence(self, item: ResearchInsight) -> float:
        try:
            conf = getattr(item, "confidence", None)
            if conf is not None:
                return float(conf)
            if isinstance(item, dict):
                v = item.get("confidence")
                return float(v) if v is not None else 0.5
        except Exception:
            pass
        return 0.5

    def _get_metadata(self, item: ResearchInsight):
        try:
            meta = getattr(item, "metadata", None)
            if meta is not None:
                return meta
            if isinstance(item, dict):
                return item.get("metadata") or {}
        except Exception:
            pass
        return {}
