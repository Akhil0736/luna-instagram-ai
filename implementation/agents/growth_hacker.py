"""Growth specialist focused on compounding loops for Instagram 2025."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List

from .base_agent import AgentBase
from implementation.knowledge_base.instagram_2025_algorithm import (
    INSTAGRAM_2025_ALGORITHM,
    VIRAL_CONTENT_PATTERNS,
)


class GrowthHackerAgent(AgentBase):
    """Deploys research-backed growth tactics aligned with the 2025 algorithm."""

    def __init__(self) -> None:
        self.algorithm_hacks: Dict[str, str] = {
            "trials_exploitation": "Test viral potential without follower spam",
            "send_rate_optimization": "Create highly shareable content",
            "watch_time_hacking": "Hook-heavy, retention-focused content",
            "audio_integration": "Leverage Instagram's audio preference",
            "status_monitoring": "Maintain recommendation eligibility",
        }
        self.growth_techniques: List[str] = [
            "strategic_timing",
            "collaboration_networks",
            "hashtag_farming",
            "comment_strategy",
            "story_engagement",
            "trend_jacking",
            "community_building",
            "competitor_analysis",
            "viral_engineering",
            "audience_retention_loops",
        ]
        self.collaboration_criteria: Dict[str, List[float]] = {
            "optimal_overlap": [0.20, 0.40],
            "engagement_overlap": [0.40, 0.60],
            "follower_range": [1_000, 100_000],
        }
        self.algorithm = INSTAGRAM_2025_ALGORITHM
        self.posting_patterns = VIRAL_CONTENT_PATTERNS["posting_schedule"]

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy synchronous entrypoint."""

        user_context = context.get("user_context", context)
        research_data = context.get("research_data", {})

        return asyncio.run(
            self.generate_growth_tactics(
                user_context=user_context,
                research_data=research_data,
            )
        )

    async def generate_growth_tactics(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Produce a growth strategy exploiting the 2025 algorithm shift."""

        trials = self._build_trials_playbook(user_context)
        send_rate = self._optimize_send_rate(research_data)
        watch_time = self._maximize_watch_time(user_context, research_data)
        collaborations = self._collaboration_blueprint(user_context, research_data)
        techniques = self._growth_technique_matrix(user_context)
        competitor = self._competitor_intelligence(research_data)

        return {
            "algorithm_hacks": self.algorithm_hacks,
            "trials_feature": trials,
            "send_rate_strategy": send_rate,
            "watch_time_program": watch_time,
            "collaboration_strategy": collaborations,
            "growth_techniques": techniques,
            "competitor_analysis": competitor,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _build_trials_playbook(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Leverage the Trials feature for safe viral testing."""

        trials_meta = self.algorithm["trials_feature"]
        audience = user_context.get("audience", "core")

        return {
            "description": trials_meta["description"],
            "testing_protocol": [
                "Launch 3 trial posts per week targeting discovery audiences",
                "Use experimental hooks sourced from Hormozi database",
                "Track watch time and send rate before moving to main feed",
            ],
            "audience_segment": f"Target non-followers adjacent to {audience}",
            "success_criteria": {
                "watch_time": 0.55,
                "send_rate": 0.08,
                "follow_through": ">3% non-follower conversions",
            },
        }

    def _optimize_send_rate(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map tactics to increase sends for unconnected reach."""

        send_factor = self.algorithm["top_3_ranking_factors"]["sends_per_reach"]
        high_performing = research_data.get("viral_sends", [])[:3]

        return {
            "priority": send_factor["priority"],
            "description": send_factor["description"],
            "tactics": [
                "Embed explicit 'send this to' prompts in caption and on-screen",
                "Design swipe files and cheat-sheets with save/send CTA",
                "Produce staggered storytelling to encourage sharing part two",
            ],
            "reference_examples": high_performing,
        }

    def _maximize_watch_time(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Deploy retention tactics aligned with watch time dominance."""

        watch_factor = self.algorithm["top_3_ranking_factors"]["watch_time"]
        target_formats = user_context.get("focus_formats", ["reels", "videos"])
        best_practices = research_data.get("watch_time_insights", [])

        return {
            "priority": watch_factor["priority"],
            "description": watch_factor["description"],
            "formats": target_formats,
            "tactics": [
                "Cold open with pattern interrupt in first 1.5 seconds",
                "Hard cut pacing every 2-3 seconds",
                "Add progress bars or countdown timers",
                "Use cliffhanger before final reveal",
            ],
            "audio_integration": "Mandatory voiceover or trending sound",
            "supporting_research": best_practices,
        }

    def _collaboration_blueprint(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Outline co-creation strategy within optimal overlap windows."""

        candidate_pool = research_data.get("collaboration_targets", [])
        vetted_candidates: List[Dict[str, Any]] = []
        for candidate in candidate_pool:
            overlap = candidate.get("audience_overlap", 0.0)
            followers = candidate.get("followers", 0)
            if (
                self.collaboration_criteria["optimal_overlap"][0]
                <= overlap
                <= self.collaboration_criteria["optimal_overlap"][1]
                and self.collaboration_criteria["follower_range"][0]
                <= followers
                <= self.collaboration_criteria["follower_range"][1]
            ):
                vetted_candidates.append(candidate)

        return {
            "criteria": self.collaboration_criteria,
            "shortlist": vetted_candidates[:5],
            "activation_playbook": [
                "Co-create reels with dual hooks",
                "Run shared live sessions during golden windows",
                "Cross-post stories with collaborative CTAs",
            ],
        }

    def _growth_technique_matrix(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Map growth techniques to user goals and posting schedule."""

        goal = user_context.get("primary_goal", "unconnected_reach")
        optimal_times = self.posting_patterns.get(
            user_context.get("audience_type", "optimal_times_b2c"),
            self.posting_patterns["optimal_times_b2c"],
        )

        return {
            "goal": goal,
            "techniques": self.growth_techniques,
            "execution_windows": optimal_times,
            "stack_order": [
                "Watch-time hacking first",
                "Send-rate optimization",
                "Collaborations",
                "Community deepening",
            ],
        }

    def _competitor_intelligence(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize competitor insights and real-time monitoring plan."""

        competitors = research_data.get("competitors", [])
        snapshots = []
        for competitor in competitors[:5]:
            snapshots.append(
                {
                    "handle": competitor.get("handle"),
                    "avg_watch_time": competitor.get("avg_watch_time", 0.0),
                    "send_rate": competitor.get("send_rate", 0.0),
                    "recent_wins": competitor.get("top_posts", [])[:2],
                }
            )

        return {
            "monitoring_stack": [
                "Track watch time delta weekly",
                "Scrape send rates per format",
                "Log trials feature usage",
                "Alert on sudden follower spikes",
            ],
            "competitive_snapshots": snapshots,
            "action_items": [
                "Reverse engineer top performing hooks",
                "Identify collaboration backdoors",
                "Deploy counter-programming within 48 hours",
            ],
        }


# Preserve backwards-compatible class name
GrowthHacker = GrowthHackerAgent
