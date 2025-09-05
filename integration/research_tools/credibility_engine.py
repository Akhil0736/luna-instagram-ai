from __future__ import annotations

import os
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


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


def _parse_date(val: str | None) -> datetime | None:
    if not val:
        return None
    # Try ISO
    try:
        # Handle cases like '2024-08-15T12:00:00Z'
        v = val.replace("Z", "+00:00")
        return datetime.fromisoformat(v)
    except Exception:
        pass
    # Try YYYY-MM-DD
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", val)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
        except Exception:
            return None
    return None


@dataclass
class CredibilityConfig:
    domain_priors: Dict[str, float]
    author_priors: Dict[str, float]
    recency_full_days: int
    recency_min_at_1y: float
    community_weights: Dict[str, float]


class CredibilityEngine:
    """Configurable credibility engine combining domain trust, author credentials,
    time decay, and community validation signals.

    Environment variables (all optional):
    - CRED_DOMAIN_PRIORS: JSON mapping domain substring -> base score
    - CRED_AUTHOR_PRIORS: JSON mapping label -> score (e.g., {"verified_influencer": 0.8})
    - CRED_RECENCY_FULL_DAYS: int days considered 100% weight (default 30)
    - CRED_RECENCY_MIN_AT_1Y: float weight at 365 days (default 0.3)
    - CRED_COMMUNITY_WEIGHTS: JSON mapping signal -> weight multiplier base
      keys: upvotes, claps, likes, comments, subscribers
    """

    def __init__(self) -> None:
        self.cfg = self._load_config()

    def _load_config(self) -> CredibilityConfig:
        domain_default = {
            "hbr.org": 0.9,
            "harvardbusinessreview.org": 0.9,
            "medium.com": 0.6,
            "reddit.com": 0.55,
            "youtube.com": 0.65,
            "quora.com": 0.5,
        }
        author_default = {
            "verified_influencer": 0.15,
            "academic": 0.1,
            "practitioner": 0.05,
        }
        comm_default = {
            "upvotes": 0.1,
            "claps": 0.1,
            "likes": 0.06,
            "comments": 0.06,
            "subscribers": 0.06,
        }
        try:
            dp = json.loads(os.getenv("CRED_DOMAIN_PRIORS", "{}"))
            if not isinstance(dp, dict):
                dp = {}
        except Exception:
            dp = {}
        try:
            ap = json.loads(os.getenv("CRED_AUTHOR_PRIORS", "{}"))
            if not isinstance(ap, dict):
                ap = {}
        except Exception:
            ap = {}
        try:
            cw = json.loads(os.getenv("CRED_COMMUNITY_WEIGHTS", "{}"))
            if not isinstance(cw, dict):
                cw = {}
        except Exception:
            cw = {}
        full_days = int(os.getenv("CRED_RECENCY_FULL_DAYS", "30"))
        min_at_1y = float(os.getenv("CRED_RECENCY_MIN_AT_1Y", "0.3"))
        # Merge defaults with overrides
        domain_priors = {**domain_default, **{str(k): float(v) for k, v in dp.items()}}
        author_priors = {**author_default, **{str(k): float(v) for k, v in ap.items()}}
        community_weights = {**comm_default, **{str(k): float(v) for k, v in cw.items()}}
        return CredibilityConfig(
            domain_priors=domain_priors,
            author_priors=author_priors,
            recency_full_days=full_days,
            recency_min_at_1y=min_at_1y,
            community_weights=community_weights,
        )

    def _domain_base(self, url: str) -> float:
        u = url.lower()
        base = 0.5
        for k, v in self.cfg.domain_priors.items():
            if k in u:
                base = max(base, float(v))
        return base

    def _author_boost(self, structured: Dict[str, Any]) -> float:
        boost = 0.0
        author = (structured or {}).get("author")
        subs = (structured or {}).get("subscribers")
        verified = (structured or {}).get("author_verified")
        credentials = (structured or {}).get("author_credentials")
        # Heuristics
        if verified is True:
            boost += self.cfg.author_priors.get("verified_influencer", 0.15)
        if isinstance(subs, (int, float)) and subs >= 100_000:
            boost += 0.1
        # Credential keywords
        if isinstance(credentials, str):
            credl = credentials.lower()
            if any(k in credl for k in ("phd", "professor", "researcher")):
                boost += self.cfg.author_priors.get("academic", 0.1)
            if any(k in credl for k in ("founder", "marketer", "growth")):
                boost += self.cfg.author_priors.get("practitioner", 0.05)
        if isinstance(author, str) and ("phd" in author.lower()):
            boost += 0.05
        return boost

    def _community_boost(self, structured: Dict[str, Any]) -> float:
        s = structured or {}
        w = self.cfg.community_weights
        boost = 0.0
        up = s.get("upvote_mentions")
        cl = s.get("clap_mentions")
        lk = s.get("like_mentions")
        cm = s.get("comment_mentions")
        sub = s.get("subscribers")
        max_up = _max_num(up)
        max_cl = _max_num(cl)
        max_lk = _max_num(lk)
        max_cm = _max_num(cm)
        max_sub = int(sub or 0)
        # Thresholded boosts
        if max_up >= 500:
            boost += w.get("upvotes", 0.1)
        if max_cl >= 1000:
            boost += w.get("claps", 0.1)
        if max_lk >= 1000:
            boost += w.get("likes", 0.06)
        if max_cm >= 100:
            boost += w.get("comments", 0.06)
        if max_sub >= 50_000:
            boost += w.get("subscribers", 0.06)
        return boost

    def _time_weight(self, published: str | None, text: str | None) -> float:
        # 1. Try published date
        dt = _parse_date(published) if published else None
        if dt is not None:
            now = datetime.now(tz=timezone.utc)
            days = max(0, (now - dt).days)
        else:
            # 2. Heuristic on recency keywords
            if text and ("2025" in text or "2024" in text):
                return 1.0
            return 0.85  # neutral fallback
        # Linear decay from full weight at full_days to min_at_1y at 365 days
        full = self.cfg.recency_full_days
        min_w = self.cfg.recency_min_at_1y
        if days <= full:
            return 1.0
        if days >= 365:
            return min_w
        # Interpolate between (full,1.0) and (365,min_w)
        span = 365 - full
        t = (days - full) / span
        return (1.0 * (1 - t)) + (min_w * t)

    def score(self, url: str, text: str, structured: Dict[str, Any] | None = None) -> float:
        base = self._domain_base(url)
        sb = self._author_boost(structured or {})
        cb = self._community_boost(structured or {})
        published = None
        if structured:
            published = structured.get("published") or structured.get("date")
        tw = self._time_weight(published, text)
        raw = base + sb + cb
        # Clamp raw between 0.2 and 0.99, then apply time weight
        raw = max(0.2, min(0.99, raw))
        final = raw * tw
        return max(0.2, min(0.95, final))
