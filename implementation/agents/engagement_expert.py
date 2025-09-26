"""Engagement specialist tuned for Instagram's 2025 prioritization model."""

from __future__ import annotations

import asyncio
import random
from datetime import datetime
from typing import Any, Dict, List

from .base_agent import AgentBase
from implementation.knowledge_base.instagram_2025_algorithm import (
    INSTAGRAM_2025_ALGORITHM,
    VIRAL_CONTENT_PATTERNS,
)


class EngagementExpertAgent(AgentBase):
    """Designs engagement systems aligned with Instagram 2025 ranking signals."""

    def __init__(self) -> None:
        self.priorities = INSTAGRAM_2025_ALGORITHM["top_3_ranking_factors"]
        self.timing = VIRAL_CONTENT_PATTERNS["posting_schedule"]
        self.hashtag_tiers: Dict[str, tuple[int, int, Any, Any]] = {
            "broad_popular": (1, 2, 1_000_000, None),
            "mid_tier": (3, 5, 100_000, 999_999),
            "niche_specific": (4, 6, 10_000, 99_999),
            "brand_custom": (1, 2, None, 9_999),
        }
        self.cta_parts = {
            "verbs": ["Discover", "Get", "Join", "Unlock", "Grab", "Start", "Learn"],
            "urgency": ["Limited time", "Today only", "Don't miss out"],
            "personal": ["For you", "Your perfect", "Designed for"],
        }

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_context = context.get("user_context", context)
        content_strategy = context.get("content_strategy", {})
        return asyncio.run(self.optimize(user_context, content_strategy))

    async def optimize(
        self,
        ctx: Dict[str, Any],
        strat: Dict[str, Any],
    ) -> Dict[str, Any]:
        await asyncio.sleep(0)

        reach_plan = self._balance_reach_metrics(ctx)
        watch_time = self._optimize_watch_time(strat)
        hashtag_plan = self._suggest_hashtags(ctx)
        ctas = self._build_cta(ctx)
        schedule = self._schedule_engagement(strat)

        return {
            "reach_strategy": reach_plan,
            "watch_time_prioritization": watch_time,
            "hashtag_strategy": hashtag_plan,
            "cta_framework": ctas,
            "engagement_schedule": schedule,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _optimize_watch_time(self, content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        formats = content_strategy.get("formats", ["reels", "videos", "stories"])
        audio_required = "Audio layer applied to all formats"

        plan: Dict[str, Any] = {
            "formats": [],
            "audio_requirement": audio_required,
            "micro_engagements": [
                "First 3-second hook",
                "Mid-content poll or question",
                "End-card CTA with action verb",
            ],
        }

        for fmt in formats:
            priority = self.priorities["watch_time"]
            plan["formats"].append(
                {
                    "format": fmt,
                    "target_completion_rate": content_strategy.get(
                        "watch_time_targets", {}
                    ).get(fmt, 0.60 if fmt != "stories" else 0.80),
                    "priority_reason": priority["description"],
                    "audio_integration": "Voiceover or trending sound mandatory",
                }
            )

        return plan

    def _balance_reach_metrics(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        reach_strategies = {
            "connected_reach": {"priority": "likes", "secondary": "sends"},
            "unconnected_reach": {"priority": "sends", "secondary": "likes"},
        }

        primary_goal = user_context.get("primary_goal", "unconnected_reach")
        strategy = reach_strategies.get(primary_goal, reach_strategies["unconnected_reach"])

        return {
            "goal": primary_goal,
            "primary_metric": strategy["priority"],
            "secondary_metric": strategy["secondary"],
            "tactics": {
                "likes": [
                    "Storyboard carousel micro-wins",
                    "Use persuasive captions with micro-CTAs",
                    "Feature social proof before CTA",
                ],
                "sends": [
                    "Add share prompts in caption and on-screen",
                    "Create save-and-send checklists",
                    "Highlight viral-friendly insights",
                ],
            },
        }

    def _suggest_hashtags(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        niche = user_context.get("niche", "general")
        hashtags: List[str] = []
        selections: Dict[str, List[str]] = {}

        for tier, (count_min, count_max, reach_min, reach_max) in self.hashtag_tiers.items():
            count = random.randint(count_min, count_max)
            tier_tags = [
                f"#{niche}{tier}{i}"
                for i in range(count)
            ]
            hashtags.extend(tier_tags)
            selections[tier] = tier_tags

        return {
            "total": hashtags[:15],
            "tiers": selections,
            "rotation": "Refresh every 14 days with performance audit",
        }

    def _build_cta(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        offer = user_context.get("offer", "your next step")
        verb = random.choice(self.cta_parts["verbs"])
        urgency = random.choice(self.cta_parts["urgency"])
        personalization = random.choice(self.cta_parts["personal"])

        sample = f"{verb} {offer} – {urgency}! {personalization}"

        return {
            "framework": "Clarity + Action Verb + Urgency + Personalization",
            "components": self.cta_parts,
            "sample": sample,
        }

    def _schedule_engagement(self, content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        optimal_slots = self.timing.get(
            content_strategy.get("audience_type", "optimal_times_b2c"),
            self.timing["optimal_times_b2c"],
        )

        return {
            "golden_window_minutes": self.timing["golden_window_minutes"],
            "optimal_post_times": optimal_slots,
            "response_protocol": [
                "Respond to first 10 comments within 5 minutes",
                "Trigger polls or question stickers in stories",
                "Deploy DM follow-up for high-intent engagers",
            ],
        }


EngagementExpert = EngagementExpertAgent
