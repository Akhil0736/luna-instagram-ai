"""Funnel Architect Agent - Content Funnel Strategy & Conversion Optimization"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List

from ..knowledge_base import (
    CONTENT_STRATEGY_FRAMEWORK,
    VIRAL_CONTENT_PATTERNS,
    CTA_EFFECTIVENESS_FRAMEWORK,
    get_content_pillar_mix,
    get_action_verbs,
    create_cta,
)
from .base_agent import AgentBase


class FunnelArchitectAgent(AgentBase):
    """Expert in content funnels, conversion optimization, and strategic content architecture."""

    def __init__(self) -> None:
        super().__init__()
        self.agent_name = "Funnel Architect"
        self.expertise_areas = [
            "content_funnels",
            "conversion_optimization",
            "content_architecture",
            "cta_optimization",
            "audience_journey_mapping",
        ]
        self.confidence_threshold = 0.85

    # === Funnel Design ===
    def design_content_funnel(
        self,
        business_goal: str,
        target_audience: str,
        current_content_mix: Dict[str, float],
    ) -> Dict[str, Any]:
        """Design a full content funnel spanning TOF, MOF, and BOF."""

        pillar_strategy = VIRAL_CONTENT_PATTERNS["proven_pillar_strategy"]
        funnel_architecture = CONTENT_STRATEGY_FRAMEWORK["funnel_based_architecture"]

        funnel_design = {
            "top_of_funnel": self._design_tof_strategy(target_audience, funnel_architecture),
            "middle_of_funnel": self._design_mof_strategy(business_goal, funnel_architecture),
            "bottom_of_funnel": self._design_bof_strategy(business_goal, funnel_architecture),
            "content_pillar_allocation": self._optimize_pillar_allocation(
                pillar_strategy, business_goal
            ),
            "conversion_touchpoints": self._identify_conversion_points(business_goal),
            "content_progression_map": self._create_progression_map(
                target_audience, business_goal
            ),
        }

        funnel_metrics = self._calculate_funnel_metrics(
            funnel_design, current_content_mix
        )

        return {
            "funnel_design": funnel_design,
            "predicted_metrics": funnel_metrics,
            "implementation_priority": self._prioritize_implementation(funnel_design),
            "optimization_opportunities": self._identify_optimization_opportunities(
                current_content_mix, pillar_strategy
            ),
            "success_indicators": self._define_success_indicators(business_goal),
            "confidence": 0.88,
        }

    def optimize_conversion_points(
        self,
        current_ctas: List[str],
        conversion_goal: str,
        audience_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Optimize CTAs and conversion touchpoints with research-backed data."""

        cta_framework = CTA_EFFECTIVENESS_FRAMEWORK
        current_analysis = self._analyze_current_ctas(current_ctas, cta_framework)
        optimized_ctas = self._generate_optimized_ctas(
            conversion_goal, audience_data, cta_framework
        )
        ab_testing_plan = self._design_cta_ab_tests(
            current_ctas, optimized_ctas, cta_framework
        )

        return {
            "current_cta_analysis": current_analysis,
            "optimized_ctas": optimized_ctas,
            "improvement_predictions": self._predict_cta_improvements(
                optimized_ctas
            ),
            "ab_testing_plan": ab_testing_plan,
            "placement_optimization": self._optimize_cta_placement(conversion_goal),
            "personalization_opportunities": self._identify_personalization_opportunities(
                audience_data
            ),
            "implementation_guide": self._create_cta_implementation_guide(optimized_ctas),
        }

    def analyze_audience_journey(
        self,
        audience_segments: List[Dict[str, Any]],
        content_performance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze audience journeys and prescribe optimizations for each segment."""

        journey_analysis: Dict[str, Any] = {}

        for segment in audience_segments:
            segment_name = segment["name"]
            current_journey = self._map_current_journey(segment, content_performance)
            friction_points = self._identify_friction_points(current_journey, segment)
            optimized_journey = self._design_optimized_journey(segment, friction_points)

            journey_analysis[segment_name] = {
                "current_journey": current_journey,
                "friction_points": friction_points,
                "optimized_journey": optimized_journey,
                "expected_improvement": self._calculate_journey_improvement(
                    current_journey, optimized_journey
                ),
                "implementation_priority": self._prioritize_journey_optimizations(
                    friction_points
                ),
            }

        return {
            "segment_analysis": journey_analysis,
            "cross_segment_insights": self._identify_cross_segment_patterns(
                journey_analysis
            ),
            "universal_optimizations": self._identify_universal_optimizations(
                journey_analysis
            ),
            "personalization_strategy": self._design_personalization_strategy(
                journey_analysis
            ),
            "success_metrics": self._define_journey_success_metrics(),
        }

    def debate_position(self, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Produce a stance for funnel-related debates."""

        topic_lower = topic.lower()
        if "funnel" in topic_lower or "conversion" in topic_lower:
            position = self._debate_funnel_strategy(context)
        elif "cta" in topic_lower:
            position = self._debate_cta_strategy(context)
        elif "content mix" in topic_lower:
            position = self._debate_content_mix_strategy(context)
        elif "audience journey" in topic_lower:
            position = self._debate_audience_journey_strategy(context)
        else:
            position = self._general_funnel_position(context)

        return {
            "agent": self.agent_name,
            "position": position["stance"],
            "reasoning": position["reasoning"],
            "evidence": position["evidence"],
            "confidence": position["confidence"],
            "conversion_impact": position.get("conversion_impact", "medium"),
            "implementation_complexity": position.get("complexity", "medium"),
        }

    # === Strategy Helpers ===
    def _design_tof_strategy(
        self, audience: str, architecture: Dict[str, Any]
    ) -> Dict[str, Any]:
        tof_config = architecture["top_of_funnel_discovery"]
        return {
            "primary_formats": ["reels", "carousels"],
            "reels_strategy": {
                "frequency": tof_config["reels"]["frequency"],
                "purpose": tof_config["reels"]["purpose"],
                "expected_reach_boost": tof_config["reels"]["reach_boost"],
                "content_focus": "trending topics, broad appeal, entertainment",
            },
            "carousel_strategy": {
                "purpose": tof_config["carousels"]["purpose"],
                "expected_engagement_boost": tof_config["carousels"]["engagement_boost"],
                "content_focus": "educational, value-driven, shareable",
            },
            "discovery_optimization": [
                "Use trending hashtags for maximum visibility",
                "Create thumb-stopping content in first 3 seconds",
                "Focus on broad, universal appeal topics",
            ],
        }

    def _design_mof_strategy(
        self, goal: str, architecture: Dict[str, Any]
    ) -> Dict[str, Any]:
        mof_config = architecture["middle_of_funnel_engagement"]
        return {
            "primary_formats": ["photos", "stories"],
            "photos_strategy": {
                "purpose": mof_config["photos"],
                "content_focus": "brand storytelling, behind-scenes, community building",
            },
            "stories_strategy": {
                "frequency": mof_config["stories"]["frequency"],
                "content_types": mof_config["stories"]["content"].split(", "),
                "daily_users_reach": mof_config["stories"]["daily_users"],
                "urgency_factor": mof_config["stories"]["urgency"],
            },
            "engagement_tactics": [
                "Increase comment-to-like ratio through questions",
                "Use polls and interactive stickers in stories",
                "Create conversation-starting content",
            ],
        }

    def _design_bof_strategy(
        self, goal: str, architecture: Dict[str, Any]
    ) -> Dict[str, Any]:
        bof_config = architecture["bottom_of_funnel_loyalty"]
        return {
            "primary_formats": ["lives", "channels", "direct_outreach"],
            "live_strategy": {
                "purpose": bof_config["lives"],
                "frequency": "weekly",
                "content_focus": "Q&A, product demos, exclusive announcements",
            },
            "channel_strategy": {
                "purpose": bof_config["channels"],
                "content_focus": "VIP updates, exclusive content, early access",
            },
            "conversion_tactics": [
                "Personalized outreach to high-engaged users",
                "Exclusive offers for loyal community members",
                "Direct consultation/demo offers",
            ],
        }

    def _optimize_pillar_allocation(
        self, pillar_strategy: Dict[str, Any], goal: str
    ) -> Dict[str, Any]:
        base_allocation = get_content_pillar_mix()
        optimized = base_allocation.copy()

        if goal == "lead_generation":
            optimized["educational"] = 0.35
            optimized["social_proof"] = 0.25
            optimized["promotional"] = 0.15
            optimized["entertainment"] = 0.20
            optimized["behind_scenes"] = 0.05
        elif goal == "brand_awareness":
            optimized["entertainment"] = 0.35
            optimized["behind_scenes"] = 0.25
            optimized["educational"] = 0.25
            optimized["social_proof"] = 0.10
            optimized["promotional"] = 0.05

        return {
            "optimized_allocation": optimized,
            "changes_from_base": self._calculate_allocation_changes(
                base_allocation, optimized
            ),
            "reasoning": f"Optimized for {goal} based on conversion research",
        }

    def _identify_conversion_points(self, goal: str) -> List[str]:
        return [
            "Story swipe-up to lead magnet",
            "Live Q&A with time-bound offer",
            "Carousel end-slide CTA",
            "Profile link tree with segmented offers",
        ]

    def _create_progression_map(
        self, audience: str, goal: str
    ) -> Dict[str, List[str]]:
        return {
            "awareness": ["reels", "viral hooks", "trend collaborations"],
            "interest": ["educational carousels", "stories", "community posts"],
            "decision": ["live demos", "case studies", "DM consults"],
        }

    def _calculate_funnel_metrics(
        self, funnel_design: Dict[str, Any], mix: Dict[str, float]
    ) -> Dict[str, Any]:
        reach = mix.get("reach", 0.0) * 1.4
        engagement = mix.get("engagement", 0.0) * 1.3
        conversion = mix.get("conversion", 0.0) * 1.25
        return {
            "reach_projection": reach,
            "engagement_projection": engagement,
            "conversion_projection": conversion,
        }

    def _prioritize_implementation(
        self, funnel_design: Dict[str, Any]
    ) -> List[str]:
        return [
            "Launch TOF reels cadence",
            "Build story-based MOF engagement loop",
            "Schedule BOF live conversion events",
        ]

    def _identify_optimization_opportunities(
        self, mix: Dict[str, float], pillars: Dict[str, Any]
    ) -> List[str]:
        return [
            "Reduce over-indexed pillars and rebalance",
            "Add social proof stories if underrepresented",
            "Expand CTA diversity across formats",
        ]

    def _define_success_indicators(self, goal: str) -> Dict[str, Any]:
        return {
            "primary_goal": goal,
            "leading": ["watch_time", "save_rate", "profile_visits"],
            "lagging": ["leads", "sales", "retention"],
        }

    def _analyze_current_ctas(
        self, current_ctas: List[str], framework: Dict[str, Any]
    ) -> Dict[str, Any]:
        components = framework["essential_cta_components"]
        analysis: List[Dict[str, Any]] = []
        for cta in current_ctas:
            analysis.append(
                {
                    "cta": cta,
                    "has_action_verb": any(verb in cta for verb in components["action_verbs"]),
                    "has_urgency": any(urg in cta for urg in components["urgency"]),
                    "has_personalization": any(
                        term.lower() in cta.lower()
                        for term in components["personalization"]
                    ),
                }
            )
        return {"cta_analysis": analysis}

    def _generate_optimized_ctas(
        self, goal: str, audience: Dict[str, Any], framework: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        action_verbs = get_action_verbs()
        urgency_phrases = framework["essential_cta_components"]["urgency"]
        personalization_phrases = framework["essential_cta_components"]["personalization"]

        optimized_ctas: List[Dict[str, Any]] = []
        scenarios = ["posts", "stories", "reels", "carousels"]

        for scenario in scenarios:
            for idx in range(3):
                verb = action_verbs[idx % len(action_verbs)]
                urgency = (
                    urgency_phrases[idx % len(urgency_phrases)] if idx % 2 == 0 else ""
                )
                personalization = (
                    personalization_phrases[idx % len(personalization_phrases)]
                    if idx % 3 == 0
                    else ""
                )

                cta_text = create_cta(verb, urgency, personalization)
                optimized_ctas.append(
                    {
                        "text": cta_text,
                        "scenario": scenario,
                        "predicted_improvement": "25-43%",
                        "optimal_placement": framework["cta_placement_strategy"].get(
                            scenario, "end of caption"
                        ),
                    }
                )

        return optimized_ctas

    def _predict_cta_improvements(
        self, optimized_ctas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            "expected_ctr_lift": 0.3,
            "expected_conversion_lift": 0.25,
            "personalization_impact": 0.43,
        }

    def _design_cta_ab_tests(
        self,
        current_ctas: List[str],
        optimized_ctas: List[Dict[str, Any]],
        framework: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        tests: List[Dict[str, Any]] = []
        for idx, cta in enumerate(optimized_ctas[:3]):
            tests.append(
                {
                    "test_name": f"cta_test_{idx + 1}",
                    "current_variant": current_ctas[idx % len(current_ctas)]
                    if current_ctas
                    else "current_default",
                    "optimized_variant": cta["text"],
                    "measurement_window_days": 7,
                    "success_metric": "conversion_rate",
                }
            )
        return tests

    def _optimize_cta_placement(self, goal: str) -> List[str]:
        return [
            "End-of-caption CTA with line break",
            "Story overlay button with swipe link",
            "Reels on-screen text CTA",
            "Carousel final slide CTA",
        ]

    def _identify_personalization_opportunities(
        self, audience_data: Dict[str, Any]
    ) -> List[str]:
        return [
            "Segment CTAs by buyer stage",
            "Use audience name or role in CTA",
            "Trigger CTAs based on interaction history",
        ]

    def _create_cta_implementation_guide(
        self, optimized_ctas: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        guide: List[Dict[str, Any]] = []
        for cta in optimized_ctas[:5]:
            guide.append(
                {
                    "cta": cta["text"],
                    "scenario": cta["scenario"],
                    "placement": cta["optimal_placement"],
                    "owner": "content_team",
                    "go_live": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                }
            )
        return guide

    def _map_current_journey(
        self, segment: Dict[str, Any], performance: Dict[str, Any]
    ) -> List[str]:
        return performance.get(segment["name"], ["reels", "stories", "CTA"])

    def _identify_friction_points(
        self, journey: List[str], segment: Dict[str, Any]
    ) -> List[str]:
        friction = [step for step in journey if "drop" in step.lower()]
        return friction or ["low_save_rate", "limited_dm_replies"]

    def _design_optimized_journey(
        self, segment: Dict[str, Any], friction_points: List[str]
    ) -> List[str]:
        return [
            "Reels -> Stories -> Carousel",
            "Stories -> DM -> Live demo",
            "Carousel -> Email lead magnet -> Call",
        ]

    def _calculate_journey_improvement(
        self, current_journey: List[str], optimized_journey: List[str]
    ) -> Dict[str, Any]:
        return {
            "conversion_uplift": 0.3,
            "engagement_uplift": 0.25,
            "retention_improvement": 0.2,
        }

    def _prioritize_journey_optimizations(
        self, friction_points: List[str]
    ) -> List[str]:
        return [f"Resolve {point}" for point in friction_points]

    def _identify_cross_segment_patterns(
        self, journey_analysis: Dict[str, Any]
    ) -> List[str]:
        return ["High drop between stories and DM", "Low CTA response"]

    def _identify_universal_optimizations(
        self, journey_analysis: Dict[str, Any]
    ) -> List[str]:
        return ["Strengthen mid-funnel nurturing", "Expand social proof content"]

    def _design_personalization_strategy(
        self, journey_analysis: Dict[str, Any]
    ) -> List[str]:
        return ["Segment journeys by buyer stage", "Automate DM pathways"]

    def _define_journey_success_metrics(self) -> Dict[str, Any]:
        return {
            "conversion_rate": "funnel_conversion_rate",
            "time_to_conversion": "days_to_convert",
            "retention": "60_day_retention",
        }

    def _calculate_allocation_changes(
        self, base: Dict[str, float], optimized: Dict[str, float]
    ) -> Dict[str, float]:
        return {
            pillar: round(optimized[pillar] - base.get(pillar, 0.0), 2)
            for pillar in optimized
        }

    # === Debate Positions ===
    def _debate_funnel_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Implement systematic funnel architecture over ad-hoc content creation",
            "reasoning": "Funnel-based approach increases conversion rates by 35-50% through strategic audience progression",
            "evidence": [
                "Top-of-funnel (Reels) provides 67% higher reach for discovery",
                "Middle-of-funnel (Stories) maintains daily engagement with 500M users",
                "Bottom-of-funnel (Lives) builds trust and drives conversions",
                "Systematic approach allows measurement and optimization at each stage",
            ],
            "confidence": 0.9,
            "conversion_impact": "high",
            "complexity": "medium - requires content planning but uses existing formats",
        }

    def _debate_cta_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Prioritize CTA optimization - 30-43% conversion improvement potential",
            "reasoning": "CTA improvements provide immediate, measurable conversion gains with minimal effort",
            "evidence": [
                "Button CTAs show 30% higher click-through than text-only",
                "Urgent language increases immediate actions by 25%",
                "Personalized CTAs achieve 43% higher engagement rates",
                "CTA placement optimization can double conversion rates",
            ],
            "confidence": 0.95,
            "conversion_impact": "very high",
            "complexity": "low - easy to implement and test",
        }

    def _debate_content_mix_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Align content pillars to business objectives",
            "reasoning": "Balanced pillar mix fuels each funnel stage and prevents algorithm fatigue",
            "evidence": [
                "Educational and social proof pillars drive lead generation",
                "Entertainment and behind-the-scenes fuel brand awareness",
                "Promotional pillar keeps conversions top-of-mind without overwhelming",
            ],
            "confidence": 0.87,
            "conversion_impact": "medium",
            "complexity": "medium",
        }

    def _debate_audience_journey_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Map end-to-end journeys to eliminate friction",
            "reasoning": "Clarity on journey stages surfaces drop-offs and accelerates conversion",
            "evidence": [
                "Journey mapping uncovers hidden friction points",
                "Personalized pathways increase retention",
                "Segmented journeys boost conversion rates",
            ],
            "confidence": 0.86,
            "conversion_impact": "high",
            "complexity": "high - requires data instrumentation",
        }

    def _general_funnel_position(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "stance": "Adopt a 70-20-10 funnel testing cadence",
            "reasoning": "Balances proven conversion plays with innovation",
            "evidence": [
                "70% stable funnel programs maintain predictability",
                "20% iterative tests drive incremental improvement",
                "10% moonshots unlock breakthrough conversions",
            ],
            "confidence": 0.8,
            "conversion_impact": "medium",
            "complexity": "medium",
        }


FunnelArchitect = FunnelArchitectAgent
