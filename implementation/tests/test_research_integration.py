"""Integration tests covering research-backed systems in the implementation layer."""

from __future__ import annotations

import asyncio
import random
from typing import Any, Dict

import pytest

from implementation.agents.content_strategist import ContentStrategistAgent
from implementation.agents.engagement_expert import EngagementExpertAgent
from implementation.agents.growth_hacker import GrowthHackerAgent
from implementation.integration.riona_integration import RionaHumanBehaviorEngine
from implementation.knowledge_base.instagram_2025_algorithm import INSTAGRAM_2025_ALGORITHM
from implementation.orchestration.agent_orchestrator import AgentOrchestrator


@pytest.fixture()
def sample_user_context() -> Dict[str, Any]:
    return {
        "audience": "wellness_coaches",
        "primary_goal": "unconnected_reach",
        "offer": "signature breathwork intensive",
        "audience_type": "optimal_times_b2b",
        "focus_formats": ["reels", "videos", "stories"],
        "timezone": "UTC",
    }


@pytest.fixture()
def sample_research_data() -> Dict[str, Any]:
    return {
        "research_synthesis": {
            "top_hooks": {
                "educational": "This breathwork shift doubled client retention",
                "entertainment": "Watch how stress leaves in 30 seconds",
                "social_proof": "Client results: 10x calmer mornings",
                "behind_scenes": "Inside our 5am routine",
                "promotional": "Secure your VIP breathwork slot",
            },
            "value_props": {
                "educational": "Share the science-backed breathing stack",
                "entertainment": "Deliver a transformation story arc",
            },
            "cta_templates": {
                "educational": "Comment \"breath\" to get the protocol",
                "entertainment": "Tag a friend who needs calm",
            },
        },
        "viral_sends": [
            {"title": "Reset vagus nerve", "send_rate": 0.12},
            {"title": "30 second calm", "send_rate": 0.15},
        ],
        "watch_time_insights": [
            "Hook with visual contrast in first second",
            "Use countdown timers for retention",
        ],
        "collaboration_targets": [
            {"handle": "@calmcoach", "audience_overlap": 0.32, "followers": 4500},
            {"handle": "@mindfulceo", "audience_overlap": 0.27, "followers": 9800},
        ],
        "competitors": [
            {
                "handle": "@breathboss",
                "avg_watch_time": 0.61,
                "send_rate": 0.09,
                "top_posts": ["Breath reset", "Founder story"],
            }
        ],
    }


@pytest.fixture()
def execution_plan() -> Dict[str, Any]:
    return {
        "automation_scope": {
            "actions": [
                {"type": "like", "target": "@calmcoach"},
                {"type": "comment", "target": "@mindfulceo"},
                {"type": "follow", "target": "@flowmentor"},
                {"type": "story_view", "target": "@breathboss"},
                {"type": "dm", "target": "@breathboss"},
            ]
        }
    }


@pytest.mark.asyncio
async def test_2025_algorithm_compliance(sample_user_context, sample_research_data):
    content_agent = ContentStrategistAgent()
    content_plan = await content_agent.analyze_and_plan(sample_user_context, sample_research_data)

    assert content_plan["watch_time_enrichment"], "Watch time enrichment should be generated"
    for enrichment in content_plan["watch_time_enrichment"]:
        targets = enrichment["watch_time_targets"]
        assert targets["reels"] >= 0.6
        assert "pattern_interrupts" in enrichment

    growth_agent = GrowthHackerAgent()
    growth_plan = await growth_agent.generate_growth_tactics(sample_user_context, sample_research_data)

    watch_program = growth_plan["watch_time_program"]
    assert "mandatory" in watch_program["audio_integration"].lower()

    send_strategy = growth_plan["send_rate_strategy"]
    assert len(send_strategy["tactics"]) >= 3

    trials_feature = growth_plan["trials_feature"]
    assert trials_feature["description"].startswith("Test content")
    assert trials_feature["success_criteria"]["send_rate"] >= 0.08


@pytest.mark.asyncio
async def test_hook_effectiveness(sample_user_context, sample_research_data):
    content_agent = ContentStrategistAgent()
    content_plan = await content_agent.analyze_and_plan(sample_user_context, sample_research_data)

    allocations = content_plan["pillar_allocation"]
    expected_allocations = {
        "educational": 0.30,
        "entertainment": 0.25,
        "social_proof": 0.20,
        "behind_scenes": 0.15,
        "promotional": 0.10,
    }
    assert allocations == expected_allocations

    testing_framework = content_plan["testing_framework"]
    total_ideas = sum(len(bucket) for bucket in testing_framework.values())
    assert total_ideas > 0
    assert len(testing_framework["proven"]) >= int(total_ideas * 0.5)
    assert len(testing_framework["experimental"]) <= max(1, int(total_ideas * 0.2))

    engagement_agent = EngagementExpertAgent()
    engagement_plan = await engagement_agent.optimize_engagement(sample_user_context, content_plan)

    hashtag_tiers = engagement_plan["hashtag_strategy"]["tiers"]
    assert set(hashtag_tiers.keys()) == {
        "broad_popular",
        "mid_tier",
        "niche_specific",
        "brand_custom",
    }

    assert content_plan["golden_window_minutes"] == 20


@pytest.mark.asyncio
async def test_multi_agent_system(sample_user_context, sample_research_data):
    orchestrator = AgentOrchestrator()
    strategy_output = await orchestrator.orchestrate_strategy(sample_user_context, sample_research_data)

    assert strategy_output["debate_transcript"], "Debate transcript should be recorded"
    methods = {entry["method"] for entry in strategy_output["debate_transcript"]}
    assert methods == {"conventional", "single_text", "visioning"}

    performance = strategy_output["performance_projection"]
    assert 0.5 <= performance["watch_time_score"] <= 1.0
    assert performance["weighted_projection"] >= 0.5

    final_strategy = strategy_output["final_strategy"]
    assert "content" in final_strategy and "engagement" in final_strategy
    assert "compliance" in final_strategy and "performance" in final_strategy


@pytest.mark.asyncio
async def test_human_behavior_simulation(execution_plan):
    random.seed(42)
    behavior_engine = RionaHumanBehaviorEngine()

    account_config = {"timezone": "UTC", "weekend_mode": True}
    result = await behavior_engine.execute_engagement_strategy(execution_plan["automation_scope"], account_config)

    schedule = result["schedule"]
    assert schedule["engagement_windows"], "Usage peaks should be scheduled"

    safety_report = result["safety_report"]
    assert not safety_report["violations"], "No safety limits should be violated"
    assert safety_report["bot_detection_risk"] <= behavior_engine.detection_threshold

    compliance = result["algorithm_compliance"]
    assert set(compliance["rules_checked"]) == set(
        INSTAGRAM_2025_ALGORITHM["recommendation_rules"].keys()
    )
    assert all(compliance["flags"].values())
