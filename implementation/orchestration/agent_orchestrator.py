"""Orchestrator coordinating Luna implementation agents with 2025 algorithm awareness."""

from __future__ import annotations

import asyncio
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List, Tuple

from ..agents.content_strategist import ContentStrategistAgent, ContentStrategist
from ..agents.engagement_expert import EngagementExpertAgent, EngagementExpert
from ..agents.growth_hacker import GrowthHackerAgent, GrowthHacker
from ..agents.funnel_architect import FunnelArchitectAgent, FunnelArchitect
from ..knowledge_base.instagram_2025_algorithm import INSTAGRAM_2025_ALGORITHM
from .agent_debate_system import AgentDebateSystem
from .consensus_builder import ConsensusBuilder, ConsensusMethod
from .consensus_engine import ConsensusEngine


class AgentOrchestrator:
    """Coordinates specialist agents, debates outputs, and enforces algorithm priorities."""

    def __init__(self) -> None:
        self.specialist_agents: Dict[str, Any] = {
            "content_strategist": _resolve_agent(ContentStrategistAgent, ContentStrategist),
            "engagement_expert": _resolve_agent(EngagementExpertAgent, EngagementExpert),
            "growth_hacker": _resolve_agent(GrowthHackerAgent, GrowthHacker),
            "funnel_architect": _resolve_agent(FunnelArchitectAgent, FunnelArchitect),
        }

        self.algorithm_weights: Dict[str, float] = {
            "watch_time": 0.50,
            "likes_per_reach": 0.25,
            "sends_per_reach": 0.25,
        }
        self.consensus_methods: List[str] = ["conventional", "single_text", "visioning"]
        self.consensus_engine = ConsensusEngine()
        self.debate_system = AgentDebateSystem()
        self.consensus_builder = ConsensusBuilder()
        self.algorithm_spec = INSTAGRAM_2025_ALGORITHM

    async def orchestrate_strategy(
        self,
        user_context: Dict[str, Any],
        research_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run multi-agent pipeline aligned with Instagram 2025 signaling."""

        # Phase 1: Algorithm-prioritized analysis
        agent_outputs = await self._collect_agent_outputs(user_context, research_data)

        # Phase 2: Multi-agent debate and consensus building
        debate_results = await self._run_strategic_debate(user_context, agent_outputs)
        consensus_results = self._build_strategic_consensus(debate_results)

        # Phase 3: Algorithm compliance validation
        compliance_report = self._validate_algorithm_compliance(agent_outputs)

        # Phase 4: Performance prediction using 2025 factors
        performance_projection = self._predict_performance(agent_outputs)

        # Phase 5: Final strategy synthesis
        final_strategy = self._synthesize_strategy(
            agent_outputs,
            debate_results,
            consensus_results,
            compliance_report,
            performance_projection,
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm_weights": self.algorithm_weights,
            "agent_outputs": agent_outputs,
            "debate_results": debate_results,
            "consensus_results": consensus_results,
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
        if hasattr(funnel_agent, 'design_content_funnel'):
            # New FunnelArchitectAgent
            funnel_plan = funnel_agent.design_content_funnel(
                business_goal=user_context.get("business_goal", "growth"),
                target_audience=user_context.get("target_audience", "general"),
                current_content_mix=content_plan.get("content_mix", {})
            )
        else:
            # Legacy FunnelArchitect
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

    async def _run_strategic_debate(self, user_context: Dict[str, Any], agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run strategic debates using the enhanced debate system."""
        
        # Identify key strategic decisions that need debate
        strategic_topics = self._identify_strategic_topics(agent_outputs)
        debate_results: Dict[str, Any] = {}
        
        for topic in strategic_topics:
            context = {
                "user_context": user_context,
                "agent_outputs": agent_outputs,
                "topic": topic
            }
            
            debate_session = self.debate_system.initiate_debate(
                topic=topic,
                context=context,
                participating_agents=None  # Use all agents
            )
            
            debate_results[topic] = debate_session
            
        await asyncio.sleep(0)  # ensure cooperative scheduling
        return debate_results

    def _identify_strategic_topics(self, agent_outputs: Dict[str, Any]) -> List[str]:
        """Identify key strategic topics that require multi-agent debate."""
        
        topics = []
        
        # Check for conflicting content strategies
        if "content" in agent_outputs and "engagement" in agent_outputs:
            topics.append("content_strategy_prioritization")
            
        # Check for growth vs conversion tensions
        if "growth" in agent_outputs and "funnel" in agent_outputs:
            topics.append("growth_vs_conversion_balance")
            
        # Always debate hashtag strategies if engagement data present
        if "engagement" in agent_outputs:
            topics.append("hashtag_strategy_optimization")
            
        # CTA optimization debates
        if "funnel" in agent_outputs:
            topics.append("cta_optimization_approach")
            
        return topics or ["overall_strategy_alignment"]
        
    def _build_strategic_consensus(self, debate_results: Dict[str, Any]) -> Dict[str, Any]:
        """Build consensus from debate results using multiple methods."""
        
        consensus_results: Dict[str, Any] = {}
        
        for topic, debate_session in debate_results.items():
            if not debate_session.get("consensus_reached", False):
                # Extract positions from the final round
                final_positions = {}
                if debate_session.get("rounds"):
                    final_round = debate_session["rounds"][-1]
                    final_positions = final_round.get("positions", {})
                
                # Try different consensus methods
                consensus_methods = [
                    ConsensusMethod.CONVENTIONAL,
                    ConsensusMethod.WEIGHTED_VOTE,
                    ConsensusMethod.MAJORITY_VOTE
                ]
                
                consensus_achieved = False
                for method in consensus_methods:
                    context = {
                        "topic": topic,
                        "agent_weights": {
                            "content_strategist": 1.0,
                            "engagement_expert": 0.9,
                            "growth_hacker": 0.9,
                            "funnel_architect": 0.85
                        }
                    }
                    
                    consensus_result = self.consensus_builder.build_consensus(
                        agent_positions=final_positions,
                        method=method,
                        context=context
                    )
                    
                    if consensus_result.get("success", False):
                        consensus_results[topic] = {
                            "method": method.value,
                            "result": consensus_result,
                            "confidence": consensus_result.get("consensus_confidence", 0.7)
                        }
                        consensus_achieved = True
                        break
                        
                if not consensus_achieved:
                    # Fallback to debate system decision
                    consensus_results[topic] = {
                        "method": "debate_system_fallback",
                        "result": debate_session.get("final_decision", {}),
                        "confidence": 0.6
                    }
            else:
                # Debate reached consensus
                consensus_results[topic] = {
                    "method": "debate_consensus",
                    "result": debate_session.get("final_decision", {}),
                    "confidence": 0.85
                }
                
        return consensus_results

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
        debate_results: Dict[str, Any],
        consensus_results: Dict[str, Any],
        compliance_report: Dict[str, Any],
        performance_projection: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge agent proposals using enhanced consensus and debate insights."""

        # Extract consensus decisions for each strategic area
        strategic_decisions = {}
        implementation_priority = []
        
        for topic, consensus in consensus_results.items():
            decision = consensus.get("result", {})
            confidence = consensus.get("confidence", 0.5)
            
            strategic_decisions[topic] = {
                "decision": decision,
                "confidence": confidence,
                "method": consensus.get("method", "unknown")
            }
            
            # Add to implementation priority based on confidence
            if confidence > 0.8:
                implementation_priority.append(f"High priority: {topic}")
            elif confidence > 0.6:
                implementation_priority.append(f"Medium priority: {topic}")
            else:
                implementation_priority.append(f"Low priority: {topic} (requires review)")
        
        # Legacy consensus engine integration for backward compatibility
        consensus_ready = {
            "content": agent_outputs["content"],
            "engagement": agent_outputs["engagement"],
            "growth": agent_outputs["growth"],
            "funnel": agent_outputs["funnel"],
            "strategic_decisions": strategic_decisions,
            "compliance": compliance_report,
            "performance": performance_projection,
        }
        
        legacy_consensus = self.consensus_engine.align(consensus_ready)

        return {
            "strategic_decisions": strategic_decisions,
            "implementation_priority": implementation_priority,
            "debate_insights": self._extract_debate_insights(debate_results),
            "consensus_confidence": self._calculate_overall_confidence(consensus_results),
            "legacy_alignment": legacy_consensus,
            "next_steps": self._generate_next_steps(strategic_decisions, compliance_report),
        }
        
    def _extract_debate_insights(self, debate_results: Dict[str, Any]) -> List[str]:
        """Extract key insights from debate sessions."""
        insights = []
        
        for topic, session in debate_results.items():
            if session.get("rounds"):
                for round_data in session["rounds"]:
                    insights.extend(round_data.get("key_insights", []))
                    
        return list(dict.fromkeys(insights))  # Remove duplicates
        
    def _calculate_overall_confidence(self, consensus_results: Dict[str, Any]) -> float:
        """Calculate overall confidence across all consensus decisions."""
        if not consensus_results:
            return 0.5
            
        confidences = [result.get("confidence", 0.5) for result in consensus_results.values()]
        return round(sum(confidences) / len(confidences), 3)
        
    def _generate_next_steps(self, strategic_decisions: Dict[str, Any], compliance_report: Dict[str, Any]) -> List[str]:
        """Generate actionable next steps based on strategic decisions."""
        next_steps = []
        
        # Add compliance-based next steps
        if not compliance_report.get("watch_time_present", False):
            next_steps.append("Implement watch-time optimization in content strategy")
            
        if not compliance_report.get("trials_utilized", False):
            next_steps.append("Activate trials feature for content testing")
            
        # Add decision-based next steps
        for topic, decision_data in strategic_decisions.items():
            confidence = decision_data.get("confidence", 0.5)
            if confidence > 0.8:
                next_steps.append(f"Execute high-confidence decision for {topic}")
            elif confidence < 0.6:
                next_steps.append(f"Gather more data before implementing {topic}")
                
        return next_steps or ["Review agent outputs and refine strategy"]


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
