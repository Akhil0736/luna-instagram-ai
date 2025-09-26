"""Orchestrator coordinating Luna implementation agents with 2025 algorithm awareness."""

from __future__ import annotations

import asyncio
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List, Tuple

from ..agents.content_strategist import ContentStrategistAgent, ContentStrategist
from ..agents.engagement_expert import EngagementExpertAgent, EngagementExpert
from ..agents.growth_hacker import GrowthHackerAgent, GrowthHacker
from ..agents.funnel_architect import FunnelArchitect  # TODO: upgrade to async agent
from ..knowledge_base.instagram_2025_algorithm import INSTAGRAM_2025_ALGORITHM
from .consensus_engine import ConsensusEngine


class AgentOrchestrator:
    """Coordinates specialist agents, debates outputs, and enforces algorithm priorities."""

    def __init__(self) -> None:
        self.specialist_agents: Dict[str, Any] = {
            "content_strategist": _resolve_agent(ContentStrategistAgent, ContentStrategist),
            "engagement_expert": _resolve_agent(EngagementExpertAgent, EngagementExpert),
            "growth_hacker": _resolve_agent(GrowthHackerAgent, GrowthHacker),
            "funnel_architect": FunnelArchitect(),
        }

        self.algorithm_weights: Dict[str, float] = {
            "watch_time": 0.50,
            "likes_per_reach": 0.25,
            "sends_per_reach": 0.25,
        }
        self.consensus_methods: List[str] = ["conventional", "single_text", "visioning"]
        self.consensus_engine = ConsensusEngine()
        self.algorithm_spec = INSTAGRAM_2025_ALGORITHM

    async def orchestrate_strategy(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run multi-agent pipeline aligned with Instagram 2025 signaling."""

        # Phase 1: Algorithm-prioritized analysis
        agent_outputs = await self._collect_agent_outputs(user_context, research_data)

        # Phase 2: Multi-agent debate and refinement (AutoGen-inspired)
        debate_transcript = await self._run_multiagent_debate(agent_outputs)

        # Phase 3: Algorithm compliance validation
        compliance_report = self._validate_algorithm_compliance(agent_outputs)

        # Phase 4: Performance prediction using 2025 factors
        performance_projection = self._predict_performance(agent_outputs)

        # Phase 5: Final strategy synthesis
        final_strategy = self._synthesize_strategy(
            agent_outputs,
            debate_transcript,
            compliance_report,
            performance_projection,
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm_weights": self.algorithm_weights,
            "agent_outputs": agent_outputs,
            "debate_transcript": debate_transcript,
            "compliance_report": compliance_report,
            "performance_projection": performance_projection,
            "final_strategy": final_strategy,
        }

    async def _collect_agent_outputs(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Gather specialized outputs while prioritizing watch time intelligence."""

        content_agent = self.specialist_agents["content_strategist"]
        content_plan = await content_agent.analyze_and_plan(user_context, research_data)

        engagement_agent = self.specialist_agents["engagement_expert"]
        engagement_plan = await engagement_agent.optimize_engagement(user_context, content_plan)

        growth_agent = self.specialist_agents["growth_hacker"]
        growth_plan = await growth_agent.generate_growth_tactics(user_context, research_data)

        funnel_agent = self.specialist_agents["funnel_architect"]
        funnel_plan = await asyncio.to_thread(
            funnel_agent.analyze,
            {
                "user_context": user_context,
                "growth_plan": growth_plan,
                "content_plan": content_plan,
                "research_data": research_data,
            },
        )

        return {
            "content": content_plan,
            "engagement": engagement_plan,
            "growth": growth_plan,
            "funnel": funnel_plan,
        }

    async def _run_multiagent_debate(self, agent_outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate Microsoft AutoGen-style debate across consensus methods."""

        transcript: List[Dict[str, Any]] = []

        for method in self.consensus_methods:
            if method == "conventional":
                summary = self._conventional_consensus(agent_outputs)
            elif method == "single_text":
                summary = self._single_text_iteration(agent_outputs)
            else:
                summary = self._visioning_alignment(agent_outputs)

            transcript.append({"method": method, "summary": summary})

        await asyncio.sleep(0)  # ensure cooperative scheduling in async loops
        return transcript

    def _conventional_consensus(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Round-robin rebuttal emphasizing watch time as primary objective."""

        watch_focus = agent_outputs["content"].get("watch_time_enrichment", [])
        engagement_ctas = agent_outputs["engagement"].get("cta_framework", {})
        growth_trials = agent_outputs["growth"].get("trials_feature", {})

        return {
            "watch_time_alignment": watch_focus[:2],
            "engagement_rebuttal": engagement_ctas.get("samples", [])[:2],
            "growth_counterpoints": growth_trials.get("testing_protocol", [])[:2],
        }

    def _single_text_iteration(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Single-text debate where agents iteratively refine a shared strategy."""

        shared_doc: Dict[str, Any] = {
            "hook_strategy": agent_outputs["content"].get("hook_samples", []),
            "engagement_protocol": agent_outputs["engagement"].get("engagement_schedule", {}),
            "growth_levers": agent_outputs["growth"].get("growth_techniques", []),
        }

        shared_doc["revision_notes"] = [
            "Content agent introduces watch-time mandates",
            "Engagement agent injects 20-minute response loop",
            "Growth agent layers trials feature pressure test",
        ]
        return shared_doc

    def _visioning_alignment(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Future-back scenario planning for the next 90 days."""

        return {
            "vision_statement": "Achieve compounding discovery reach via high send-rate content",
            "milestones": [
                "Week 1-2: Deploy trials content and capture baseline",
                "Week 3-6: Scale collaborations hitting 30% overlap",
                "Week 7-12: Automate retention loops with experimental hooks",
            ],
            "risk_controls": agent_outputs["growth"].get("competitor_analysis", {}).get(
                "monitoring_stack", []
            ),
        }

    def _validate_algorithm_compliance(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure each plan aligns with Adam Mosseri's 2025 guidance."""

        recommendation_rules = self.algorithm_spec["recommendation_rules"]
        trials_feature = self.algorithm_spec["trials_feature"]

        compliance_checks = {
            "watch_time_present": bool(agent_outputs["content"].get("watch_time_enrichment")),
            "audio_integration": "audio_integration" in agent_outputs["growth"]["watch_time_program"],
            "trials_utilized": "description" in agent_outputs["growth"]["trials_feature"],
            "recommendation_rules": list(recommendation_rules.keys()),
        }

        compliance_checks["notes"] = [
            "Ensure no watermarks on trial content",
            "Confirm account status remains in good standing before scaling",
            f"Trials benefit: {trials_feature['benefit']}",
        ]

        return compliance_checks

    def _predict_performance(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Heuristic scorecard combining agent outputs with algorithm weights."""

        watch_signal = self._score_watch_time(agent_outputs["content"])
        like_signal = self._score_likes(agent_outputs["engagement"])
        send_signal = self._score_sends(agent_outputs["growth"])

        weighted_score = round(
            watch_signal * self.algorithm_weights["watch_time"]
            + like_signal * self.algorithm_weights["likes_per_reach"]
            + send_signal * self.algorithm_weights["sends_per_reach"],
            4,
        )

        return {
            "watch_time_score": watch_signal,
            "likes_score": like_signal,
            "sends_score": send_signal,
            "weighted_projection": weighted_score,
        }

    def _score_watch_time(self, content_plan: Dict[str, Any]) -> float:
        enrichments = content_plan.get("watch_time_enrichment", [])
        targets = [item.get("watch_time_targets", {}) for item in enrichments]
        if not targets:
            return 0.5
        averages: List[float] = []
        for target in targets:
            averages.append(mean(target.values()) if target else 0.5)
        return round(min(1.0, max(0.5, mean(averages))), 4)

    def _score_likes(self, engagement_plan: Dict[str, Any]) -> float:
        cta_samples = engagement_plan.get("cta_framework", {}).get("samples", [])
        hashtag_depth = len(engagement_plan.get("hashtag_strategy", {}).get("tiers", {}))
        score = 0.5
        if cta_samples:
            score += 0.2
        if hashtag_depth >= 4:
            score += 0.2
        return round(min(1.0, score), 4)

    def _score_sends(self, growth_plan: Dict[str, Any]) -> float:
        tactics = growth_plan.get("send_rate_strategy", {}).get("tactics", [])
        references = growth_plan.get("send_rate_strategy", {}).get("reference_examples", [])
        score = 0.5
        if len(tactics) >= 3:
            score += 0.2
        if references:
            score += 0.1
        return round(min(1.0, score), 4)

    def _synthesize_strategy(
        self,
        agent_outputs: Dict[str, Any],
        debate_transcript: List[Dict[str, Any]],
        compliance_report: Dict[str, Any],
        performance_projection: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge agent proposals using consensus engine and debate insights."""

        consensus_ready = {
            "content": agent_outputs["content"],
            "engagement": agent_outputs["engagement"],
            "growth": agent_outputs["growth"],
            "funnel": agent_outputs["funnel"],
            "debate": debate_transcript,
            "compliance": compliance_report,
            "performance": performance_projection,
        }

        return self.consensus_engine.align(consensus_ready)


def _resolve_agent(preferred_cls, legacy_cls):
    """Instantiate preferred agent class, falling back to legacy alias if required."""

    if preferred_cls is legacy_cls:
        return preferred_cls()
    try:
        return preferred_cls()
    except Exception:  # pragma: no cover - fallback safety
        return legacy_cls()


# Backwards compatibility for older imports
ImplementationAgentOrchestrator = AgentOrchestrator
