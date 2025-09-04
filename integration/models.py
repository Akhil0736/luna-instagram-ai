from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Literal


# Core data models for LunaAgent orchestration


@dataclass
class GrowthGoal:
    """
    Represents a user's growth objective on Instagram.

    Example:
      target_metric = "followers"
      target_increase = 0.20    # 20%
      timeline_days = 60
      niche = "fitness"
      current_followers = 1200
    """

    target_metric: Literal["followers", "engagement", "reach"]
    target_increase: float
    timeline_days: int
    niche: str
    current_followers: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class ResearchInsight:
    """
    Insights aggregated from research tools.
    """

    source: str  # e.g., "reddit", "youtube", "quora", "tavily"
    insight: str
    confidence: float = 0.5  # 0..1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentRecommendation:
    """
    Recommendation for a single piece of content.
    """

    post_type: Literal["reel", "photo", "carousel", "story", "live"]
    theme: str
    caption_template: str
    hashtags: List[str]
    best_time: Optional[str] = None


@dataclass
class AutomationTask:
    """
    Automation instruction to be executed (pending user approval) by Riona.
    """

    action_type: Literal["like", "comment", "follow", "dm"]
    target_criteria: Dict[str, Any]
    daily_limit: int
    message_template: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
