"""Content strategy specialist powered by Instagram's 2025 algorithm intelligence."""

from __future__ import annotations

import asyncio
import random
from datetime import datetime
from typing import Any, Dict, List, Tuple

from .base_agent import AgentBase
from implementation.knowledge_base.instagram_2025_algorithm import (
    ALEX_HORMOZI_HOOKS,
    INSTAGRAM_2025_ALGORITHM,
    VIRAL_CONTENT_PATTERNS,
)


class ContentStrategistAgent(AgentBase):
    """Transforms research signals into cohesive content plans optimized for 2025."""

    def __init__(self) -> None:
        self.algorithm = INSTAGRAM_2025_ALGORITHM
        self.hooks = ALEX_HORMOZI_HOOKS
        self.patterns = VIRAL_CONTENT_PATTERNS
        self.test_mix: Dict[str, float] = {"proven": 0.70, "adjacent": 0.20, "experimental": 0.10}
        self.watch_targets: Dict[str, float] = {"reels": 0.75, "videos": 0.60, "stories": 0.80}

        self.shareability_triggers: List[str] = [
            "valuable_tips",
            "relatable_moments",
            "shocking_facts",
            "funny_content",
            "inspirational_stories",
            "useful_hacks",
        ]

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_context = context.get("user_context", context)
        research = context.get("research_data", {})
        return asyncio.run(self.analyze_and_plan(user_context, research))

    async def analyze_and_plan(
        self,
        user_ctx: Dict[str, Any],
        research: Dict[str, Any],
    ) -> Dict[str, Any]:
        await asyncio.sleep(0)

        base_plan = {
            "strategy_name": "pillar-plan",
            "hooks_sample": self._select_hooks(user_ctx, 10),
            "weekly_pillar_mix": self.patterns["content_pillars"],
            "posting_windows": self.patterns["posting_schedule"],
            "watch_time_goal": self.watch_targets,
        }

        detailed_plan = self._compose_content_blueprint(user_ctx, research)
        detailed_plan.update(base_plan)

        enriched = self._optimize_for_watch_time(detailed_plan)
        enriched["send_triggers"] = self._maximize_send_potential(enriched["content_ideas"])
        enriched["testing_framework"] = self._build_testing_framework(enriched["content_ideas"])
        enriched["algorithm_alignment"] = self._summarize_algorithm_focus()
        enriched["timestamp"] = datetime.utcnow().isoformat()

        return enriched

    def _select_hooks(self, user_ctx: Dict[str, Any], n: int) -> List[str]:
        pools: List[List[str]] = [
            self.hooks.get("labels", []),
            self.hooks.get("questions", []),
            self.hooks.get("commands", []),
            self.hooks.get("viral_templates", []),
        ]
        available = [hook for pool in pools for hook in pool]
        random.shuffle(available)
        if not available:
            return []

        buckets = {
            "proven": max(1, int(n * self.test_mix["proven"])),
            "adjacent": max(1, int(n * self.test_mix["adjacent"])),
            "experimental": max(1, int(n * self.test_mix["experimental"])),
        }

        selection: List[str] = []
        cursor = 0
        for bucket, count in buckets.items():
            end = cursor + count
            selection.extend(available[cursor:end])
            cursor = end

        if len(selection) < n:
            selection.extend(available[cursor:cursor + (n - len(selection))])

        return selection[:n]

    def _compose_content_blueprint(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        pillars = self.patterns["content_pillars"]
        return {
            "audience": user_context.get("audience", "general"),
            "pillar_allocation": pillars,
            "content_ideas": self._create_content_ideas(user_context, research_data, pillars),
            "hook_samples": self._select_hooks(user_context, 5),
            "golden_window_minutes": self.patterns["posting_schedule"]["golden_window_minutes"],
        }

    def _create_content_ideas(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
        pillars: Dict[str, float],
    ) -> List[Dict[str, Any]]:
        research_insights = research_data.get("research_synthesis", {})
        base_hooks = self._select_hooks(user_context, len(pillars) or 1)

        ideas: List[Dict[str, Any]] = []
        for index, pillar in enumerate(pillars):
            ideas.append(
                {
                    "pillar": pillar,
                    "hook": base_hooks[index % len(base_hooks)] if base_hooks else "Hook needed",
                    "formula": self._build_viral_formula(pillar, research_insights),
                    "audio_integration": "Required",
                }
            )
        return ideas

    def _build_viral_formula(
        self,
        pillar: str,
        insights: Dict[str, Any],
    ) -> Dict[str, str]:
        return {
            "hook": insights.get("top_hooks", {}).get(pillar, "Provocative opening"),
            "value": insights.get("value_props", {}).get(pillar, "Deliver 1 key outcome"),
            "engagement_trigger": insights.get("cta_templates", {}).get(
                pillar, "Comment your biggest challenge"
            ),
            "shareability": self.shareability_triggers[len(pillar) % len(self.shareability_triggers)],
        }

    def _optimize_for_watch_time(self, content_plan: Dict[str, Any]) -> Dict[str, Any]:
        enrichments: List[Dict[str, Any]] = []
        for idea in content_plan["content_ideas"]:
            enrichments.append(
                {
                    "pillar": idea["pillar"],
                    "hook_strength": "3s capture applied",
                    "pattern_interrupts": [
                        "Visual switch at 1.5s",
                        "Mid-video question",
                        "Cliffhanger before CTA",
                    ],
                    "watch_time_targets": self.watch_targets,
                }
            )

        content_plan["watch_time_enrichment"] = enrichments
        return content_plan

    def _maximize_send_potential(
        self,
        content_ideas: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        send_blueprints: List[Dict[str, str]] = []
        for idea in content_ideas:
            send_blueprints.append(
                {
                    "pillar": idea["pillar"],
                    "share_trigger": idea["formula"]["shareability"],
                    "send_prompt": "Send to a friend who needs this",
                    "discovery_note": "Optimized for unconnected reach",
                }
            )
        return send_blueprints

    def _build_testing_framework(
        self,
        content_ideas: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        framework: Dict[str, List[Dict[str, Any]]] = {"proven": [], "adjacent": [], "experimental": []}
        total = len(content_ideas) or 1
        thresholds: List[Tuple[str, int]] = []
        running_total = 0
        for bucket, ratio in self.test_mix.items():
            running_total += max(1, round(ratio * total))
            thresholds.append((bucket, running_total))

        for index, idea in enumerate(content_ideas, start=1):
            for bucket, threshold in thresholds:
                if index <= threshold:
                    framework[bucket].append(idea)
                    break

        return framework

    def _summarize_algorithm_focus(self) -> Dict[str, Any]:
        factors = self.algorithm["top_3_ranking_factors"]
        return {
            "primary": factors["watch_time"],
            "secondary": factors["likes_per_reach"],
            "tertiary": factors["sends_per_reach"],
            "trials_feature": self.algorithm["trials_feature"],
        }


ContentStrategist = ContentStrategistAgent
