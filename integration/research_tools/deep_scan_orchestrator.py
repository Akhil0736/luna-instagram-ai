from __future__ import annotations

import os
import time
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from .scrapedo_tool import ScrapeDoResearchTool


@dataclass
class DeepScanConfig:
    min_credibility: float
    max_items: int
    premium_weekly_scans_enabled: bool


class DeepScanOrchestrator:
    """Aggregates ScrapeDo deep scans into a comprehensive niche intelligence report.

    It extracts follower growth numbers, engagement rates, and timelines; maps
    trending strategies across validated sources; and surfaces success patterns.
    """

    def __init__(self, cfg: DeepScanConfig | None = None) -> None:
        if cfg is None:
            cfg = DeepScanConfig(
                min_credibility=float(os.getenv("DEEP_SCAN_MIN_CREDIBILITY", "0.6")),
                max_items=int(os.getenv("DEEP_SCAN_MAX_ITEMS", "50")),
                premium_weekly_scans_enabled=os.getenv("PREMIUM_WEEKLY_SCANS_ENABLED", "false").lower() == "true",
            )
        self.cfg = cfg
        self.scrapedo = ScrapeDoResearchTool()

    async def generate_report(self, niche: str) -> Dict[str, Any]:
        t0 = time.time()
        base = await self.scrapedo.deep_extraction_scan(niche)
        items: List[Dict[str, Any]] = list(base.get("items", []))[: self.cfg.max_items]
        # Compute derived insights
        metrics_summary = self._summarize_metrics(items)
        strategies = self._trending_strategies(items)
        patterns = self._success_patterns(items)
        duration = time.time() - t0
        report = {
            "niche": base.get("niche", niche),
            "generated_at": int(time.time()),
            "success": True,
            "items": items,
            "metrics_summary": metrics_summary,
            "trending_strategies": strategies,
            "success_patterns": patterns,
            "stats": {
                "item_count": len(items),
                "duration_seconds": round(duration, 2),
                "min_credibility": self.cfg.min_credibility,
            },
            "premium_weekly_scans_enabled": self.cfg.premium_weekly_scans_enabled,
        }
        return report

    def _valid_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for it in items:
            cred = float(it.get("credibility", 0))
            if cred >= self.cfg.min_credibility:
                out.append(it)
        return out

    def _summarize_metrics(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid = self._valid_items(items)
        followers: List[int] = []
        growth_rates: List[float] = []
        engagement_rates: List[float] = []
        timelines: List[int] = []
        for it in valid:
            m = it.get("metrics") or {}
            # Followers mentions
            for tok in (m.get("followers_mentions") or []):
                val = _parse_num_token(tok)
                if val:
                    followers.append(val)
            # Growth rate mentions
            for tok in (m.get("growth_rate_mentions") or []):
                try:
                    growth_rates.append(float(tok))
                except Exception:
                    pass
            # Engagement rates
            for tok in (m.get("engagement_rate_mentions") or []):
                try:
                    engagement_rates.append(float(tok))
                except Exception:
                    pass
            # Timelines
            for tok in (m.get("timeline_mentions") or []):
                try:
                    timelines.append(int(tok))
                except Exception:
                    pass
        def pct(p: float, arr: List[float]) -> float:
            if not arr:
                return 0.0
            arr2 = sorted(arr)
            k = max(0, min(len(arr2) - 1, int(round(p * (len(arr2) - 1)))))
            return float(arr2[k])
        return {
            "followers_max": max(followers) if followers else 0,
            "followers_median": int(pct(0.5, followers)) if followers else 0,
            "growth_rate_avg_pct": round(sum(growth_rates) / len(growth_rates), 2) if growth_rates else 0.0,
            "engagement_rate_avg_pct": round(sum(engagement_rates) / len(engagement_rates), 2) if engagement_rates else 0.0,
            "timeline_common_days": int(pct(0.5, timelines)) if timelines else 0,
            "samples": {
                "followers_samples": followers[:10],
                "growth_rate_samples": growth_rates[:10],
                "engagement_rate_samples": engagement_rates[:10],
                "timeline_samples": timelines[:10],
            },
        }

    def _trending_strategies(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid = self._valid_items(items)
        # Strategy keywords
        keywords = {
            "reels": ["reels", "shorts"],
            "hashtags": ["hashtag"],
            "giveaway": ["giveaway", "contest"],
            "ugc": ["ugc", "user-generated"],
            "collab": ["collab", "collaboration", "partner"],
            "carousel": ["carousel"],
            "posting_time": ["posting time", "best time", "timing"],
            "stories": ["stories"],
            "cross_promo": ["cross-promot", "cross promot", "crosspost"],
            "seo": ["seo", "search"],
        }
        counts: Dict[str, float] = {k: 0.0 for k in keywords.keys()}
        samples: Dict[str, List[str]] = {k: [] for k in keywords.keys()}
        for it in valid:
            text = (it.get("insight") or "") + " "
            s = (it.get("structured") or {})
            for field in ("tactics_sample", "posts_sample", "tutorial_steps_sample"):
                for t in (s.get(field) or []):
                    text += f" {t}"
            cred = float(it.get("credibility", 0.5))
            tl = text.lower()
            for key, kws in keywords.items():
                if any(k in tl for k in kws):
                    counts[key] += max(0.2, min(1.0, cred))
                    if len(samples[key]) < 5:
                        samples[key].append(it.get("url") or "")
        ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        return [
            {"strategy": k, "weight": round(v, 2), "sample_sources": [u for u in samples[k] if u][:5]}
            for k, v in ranked if v > 0
        ]

    def _success_patterns(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid = self._valid_items(items)
        patterns: Dict[str, Tuple[float, List[str]]] = {}
        rex = [
            ("case_study", re.compile(r"case study|results|grew|increased", re.I)),
            ("playbook", re.compile(r"playbook|framework|step\s*\d+", re.I)),
            ("data_driven", re.compile(r"data|statistic|survey|study", re.I)),
        ]
        for it in valid:
            text = (it.get("insight") or "")
            s = (it.get("structured") or {})
            cred = float(it.get("credibility", 0.5))
            url = it.get("url") or ""
            blob = text + " " + " ".join(map(str, s.values()))
            for name, r in rex:
                if r.search(blob):
                    if name not in patterns:
                        patterns[name] = (0.0, [])
                    sc, arr = patterns[name]
                    sc += max(0.2, min(1.0, cred))
                    if len(arr) < 5:
                        arr.append(url)
                    patterns[name] = (sc, arr)
        ranked = sorted(patterns.items(), key=lambda kv: kv[1][0], reverse=True)
        return [
            {"pattern": k, "weight": round(v[0], 2), "sample_sources": v[1]} for k, v in ranked
        ]


# Helpers reused from ScrapeDo numeric parsing (duplicate minimal to avoid a hard import cycle)
_num_re = re.compile(r"(\d+(?:\.\d+)?)([kKmM]?)")

def _parse_num_token(tok: Any) -> int:
    if tok is None:
        return 0
    if isinstance(tok, (int, float)):
        return int(tok)
    s = str(tok).strip().lower()
    m = _num_re.match(s)
    if not m:
        return 0
    val = float(m.group(1))
    suf = m.group(2).lower()
    if suf == "k":
        val *= 1_000
    elif suf == "m":
        val *= 1_000_000
    return int(val)
