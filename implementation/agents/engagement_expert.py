"""Engagement Expert Agent - Hashtag Optimization & Timing Specialist"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..knowledge_base import (
    HASHTAG_STRATEGY_2025,
    POSTING_OPTIMIZATION,
    get_hashtag_mix_counts,
    get_optimal_hashtag_count,
    validate_hashtag_strategy,
    is_peak_engagement_time,
)
from .base_agent import AgentBase


class EngagementExpertAgent(AgentBase):
    """Expert in hashtag optimization, timing strategies, and engagement maximization."""

    def __init__(self) -> None:
        super().__init__()
        self.agent_name = "Engagement Expert"
        self.expertise_areas = [
            "hashtag_optimization",
            "posting_timing",
            "engagement_strategies",
            "audience_analysis",
            "viral_timing",
        ]
        self.confidence_threshold = 0.8

    # === Public Capabilities ===
    def analyze_hashtag_strategy(
        self,
        content_topic: str,
        target_audience: str,
        niche: str,
    ) -> Dict[str, Any]:
        """Analyze and recommend optimal hashtag strategy."""

        framework = HASHTAG_STRATEGY_2025["proven_hashtag_framework"]
        mix_strategy = framework["mix_strategy"]

        hashtag_recommendations = {
            "broad_popular": self._generate_broad_hashtags(
                content_topic,
                mix_strategy["broad_popular"]["count_range"],
            ),
            "mid_tier": self._generate_mid_tier_hashtags(
                content_topic,
                niche,
                mix_strategy["mid_tier"]["count_range"],
            ),
            "niche_specific": self._generate_niche_hashtags(
                niche,
                target_audience,
                mix_strategy["niche_specific"]["count_range"],
            ),
            "brand_custom": self._generate_brand_hashtags(
                target_audience,
                mix_strategy["brand_custom"]["count_range"],
            ),
        }

        total_count = sum(len(tags) for tags in hashtag_recommendations.values())
        validation = validate_hashtag_strategy(hashtag_recommendations)

        return {
            "hashtag_recommendations": hashtag_recommendations,
            "total_hashtag_count": total_count,
            "optimal_count": get_optimal_hashtag_count(),
            "strategy_validation": validation,
            "performance_prediction": self._predict_hashtag_performance(
                hashtag_recommendations
            ),
            "confidence_score": 0.85,
            "reasoning": "Based on 2025 algorithm evolution and computer vision updates",
        }

    def optimize_posting_timing(
        self,
        audience_type: str,
        content_type: str,
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        """Optimize posting timing for maximum engagement."""

        optimal_times = POSTING_OPTIMIZATION["optimal_posting_times"]
        base_times = optimal_times.get(audience_type, optimal_times["b2c"])

        content_multipliers = {
            "reels": 1.2,
            "carousels": 1.1,
            "photos": 1.0,
            "stories": 0.9,
        }
        multiplier = content_multipliers.get(content_type, 1.0)

        now = datetime.now()
        next_optimal_times: List[datetime] = []

        for day_offset in range(7):
            target_date = now + timedelta(days=day_offset)

            for time_str in base_times["times"]:
                hour = int(time_str.split(":")[0])
                base_minute = random.randint(0, 59)
                minute_variance = random.randint(-15, 15)
                minute = min(max(base_minute + minute_variance, 0), 59)
                second = random.randint(0, 59)

                target_time = target_date.replace(
                    hour=hour,
                    minute=minute,
                    second=second,
                    microsecond=0,
                )

                if target_time > now:
                    next_optimal_times.append(target_time)

        next_optimal_times.sort()
        shortlisted_times = next_optimal_times[:5]

        return {
            "audience_type": audience_type,
            "content_type": content_type,
            "timezone": timezone,
            "next_optimal_times": shortlisted_times,
            "optimal_days": base_times["days"],
            "peak_engagement_prediction": self._predict_engagement_by_time(
                shortlisted_times[:3]
            ),
            "timing_confidence": min(0.95, 0.75 * multiplier),
            "current_peak_status": is_peak_engagement_time(),
            "recommendations": self._generate_timing_recommendations(
                audience_type, content_type
            ),
        }

    def debate_position(self, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide expert position on engagement-related decisions."""

        topic_lower = topic.lower()
        if "hashtag" in topic_lower:
            position = self._debate_hashtag_strategy(context)
        elif "timing" in topic_lower:
            position = self._debate_timing_strategy(context)
        elif "engagement" in topic_lower:
            position = self._debate_engagement_strategy(context)
        else:
            position = self._general_engagement_position(context)

        return {
            "agent": self.agent_name,
            "position": position["stance"],
            "reasoning": position["reasoning"],
            "evidence": position["evidence"],
            "confidence": position["confidence"],
            "suggested_tests": position.get("tests", []),
            "risk_assessment": position.get("risks", "low"),
        }

    # === Internal Utilities ===
    def _generate_broad_hashtags(self, topic: str, count_range: List[int]) -> List[str]:
        templates = [
            f"#{topic.lower()}",
            f"#viral{topic.lower()}",
            f"#trending{topic.lower()}",
            "#instagram",
            "#viral",
            "#trending",
            "#explore",
            "#fyp",
        ]
        count = random.randint(count_range[0], count_range[1])
        return random.sample(templates, min(count, len(templates)))

    def _generate_mid_tier_hashtags(
        self,
        topic: str,
        niche: str,
        count_range: List[int],
    ) -> List[str]:
        templates = [
            f"#{niche.lower()}{topic.lower()}",
            f"#{topic.lower()}tips",
            f"#{topic.lower()}expert",
            f"#{niche.lower()}community",
            f"#{topic.lower()}strategy",
            f"#{niche.lower()}growth",
        ]
        count = random.randint(count_range[0], count_range[1])
        return random.sample(templates, min(count, len(templates)))

    def _generate_niche_hashtags(
        self,
        niche: str,
        audience: str,
        count_range: List[int],
    ) -> List[str]:
        templates = [
            f"#{niche.lower()}{audience.lower()}",
            f"#{audience.lower()}{niche.lower()}",
            f"#{niche.lower()}insider",
            f"#{audience.lower()}community",
            f"#{niche.lower()}secrets",
            f"#{audience.lower()}tips",
        ]
        count = random.randint(count_range[0], count_range[1])
        return random.sample(templates, min(count, len(templates)))

    def _generate_brand_hashtags(
        self,
        audience: str,
        count_range: List[int],
    ) -> List[str]:
        templates = [
            f"#luna{audience.lower()}",
            f"#{audience.lower()}luna",
            "#lunaaigrowth",
            "#lunacommunity",
        ]
        count = random.randint(count_range[0], count_range[1])
        return random.sample(templates, min(count, len(templates)))

    def _predict_hashtag_performance(
        self,
        hashtags: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        total_reach_potential = 0
        engagement_potential = 0.0

        for category, tags in hashtags.items():
            tag_count = len(tags)
            if category == "broad_popular":
                total_reach_potential += tag_count * 100_000
                engagement_potential += tag_count * 0.02
            elif category == "mid_tier":
                total_reach_potential += tag_count * 10_000
                engagement_potential += tag_count * 0.05
            elif category == "niche_specific":
                total_reach_potential += tag_count * 1_000
                engagement_potential += tag_count * 0.12
            elif category == "brand_custom":
                total_reach_potential += tag_count * 100
                engagement_potential += tag_count * 0.25

        return {
            "estimated_reach": total_reach_potential,
            "estimated_engagement_rate": min(engagement_potential, 0.15),
            "virality_potential": "medium" if engagement_potential > 0.08 else "low",
            "recommendation": "Optimal mix for balanced reach and engagement",
        }

    def _predict_engagement_by_time(
        self, times: List[datetime]
    ) -> Dict[str, Any]:
        predictions: List[Dict[str, Any]] = []

        for time in times:
            hour = time.hour

            if hour in [12, 13, 19, 20, 21]:
                engagement_multiplier = 1.5
                expected_engagement = "high"
            elif hour in [11, 14, 18, 22]:
                engagement_multiplier = 1.2
                expected_engagement = "medium-high"
            elif hour in [9, 10, 15, 16, 17]:
                engagement_multiplier = 1.0
                expected_engagement = "medium"
            else:
                engagement_multiplier = 0.7
                expected_engagement = "low"

            predictions.append(
                {
                    "time": time,
                    "expected_engagement": expected_engagement,
                    "multiplier": engagement_multiplier,
                    "confidence": 0.8,
                }
            )

        return {"time_predictions": predictions}

    def _generate_timing_recommendations(
        self,
        audience_type: str,
        content_type: str,
    ) -> List[str]:
        recommendations: List[str] = []

        if audience_type == "b2b":
            recommendations.extend(
                [
                    "Avoid weekends for B2B content",
                    "Focus on Tuesday-Thursday for highest engagement",
                    "Post during business hours (10am-3pm) for professional audience",
                ]
            )
        elif audience_type == "b2c":
            recommendations.extend(
                [
                    "Leverage evening peak hours (7-9pm) for maximum reach",
                    "Tuesday-Thursday optimal for algorithm visibility",
                    "Consider lunch hour posts (12-2pm) for mid-day engagement",
                ]
            )

        if content_type == "reels":
            recommendations.append(
                "Reels perform well during entertainment hours (7-10pm)"
            )
        elif content_type == "carousels":
            recommendations.append(
                "Carousels work best when audience has time to engage (lunch, evening)"
            )

        return recommendations

    def _debate_hashtag_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Prioritize 10-15 strategic hashtags over maximum 30",
            "reasoning": "2025 algorithm evolution favors quality over quantity due to computer vision improvements",
            "evidence": [
                "Computer vision now understands content without hashtag dependence",
                "Targeted hashtag mix (broad+niche) outperforms generic high-volume approach",
                "Quality hashtags improve content categorization accuracy",
            ],
            "confidence": 0.9,
            "tests": ["A/B test 10 vs 30 hashtags on similar content"],
            "risks": "low",
        }

    def _debate_timing_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Consistency beats perfect timing",
            "reasoning": "Algorithm rewards consistent posting patterns over sporadic optimal timing",
            "evidence": [
                "Consistent posting builds audience expectations",
                "Algorithm favors accounts with predictable content patterns",
                "Audience retention higher with consistent schedule",
            ],
            "confidence": 0.85,
            "tests": ["Track engagement: consistent schedule vs optimal timing"],
            "risks": "medium - may miss some peak opportunities",
        }

    def _debate_engagement_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Balance watch-time hooks with community interaction",
            "reasoning": "Watch-time signals open reach while community responses convert",
            "evidence": [
                "Watch-time remains the #1 algorithm signal",
                "Comments and sends unlock unconnected reach",
                "Community management during golden window boosts conversions",
            ],
            "confidence": 0.88,
            "tests": ["Compare retention vs interaction weighted campaigns"],
            "risks": "low",
        }

    def _general_engagement_position(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Adopt a 70-20-10 testing mix across hooks and formats",
            "reasoning": "Balances proven assets with experimentation for algorithm freshness",
            "evidence": [
                "70-20-10 split aligns with hook testing best practices",
                "Algorithm prioritizes originality plus consistent retention",
                "Diverse content mix hedges against volatility",
            ],
            "confidence": 0.8,
            "tests": ["Maintain experimentation log with performance deltas"],
            "risks": "moderate - requires disciplined tracking",
        }


EngagementExpert = EngagementExpertAgent
