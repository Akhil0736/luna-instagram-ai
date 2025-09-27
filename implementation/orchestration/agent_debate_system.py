"""Agent Debate System - Multi-Agent Collaborative Decision Making"""
from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json

from ..agents.content_strategist import ContentStrategistAgent
from ..agents.engagement_expert import EngagementExpertAgent
from ..agents.growth_hacker import GrowthHackerAgent
from ..agents.funnel_architect import FunnelArchitectAgent


class AgentDebateSystem:
    """Orchestrates multi-agent debates for collaborative decision making."""

    def __init__(self) -> None:
        self.agents = {
            "content_strategist": ContentStrategistAgent(),
            "engagement_expert": EngagementExpertAgent(),
            "growth_hacker": GrowthHackerAgent(),
            "funnel_architect": FunnelArchitectAgent(),
        }
        self.debate_history: List[Dict[str, Any]] = []
        self.consensus_threshold = 0.7

    def initiate_debate(
        self,
        topic: str,
        context: Dict[str, Any],
        participating_agents: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Initiate multi-agent debate on strategic decision."""

        if participating_agents is None:
            participating_agents = list(self.agents.keys())

        debate_session: Dict[str, Any] = {
            "topic": topic,
            "context": context,
            "timestamp": datetime.now(),
            "participants": participating_agents,
            "rounds": [],
            "consensus_reached": False,
            "final_decision": None,
        }

        max_rounds = 3
        for round_num in range(max_rounds):
            round_results = self._conduct_debate_round(
                topic, context, participating_agents, round_num + 1
            )

            debate_session["rounds"].append(round_results)

            consensus_result = self._evaluate_consensus(round_results["positions"])

            if consensus_result["consensus_achieved"]:
                debate_session["consensus_reached"] = True
                debate_session["final_decision"] = consensus_result["consensus_position"]
                break

            context.update({"previous_round_insights": round_results["key_insights"]})

        if not debate_session["consensus_reached"]:
            debate_session["final_decision"] = self._make_weighted_decision(
                debate_session["rounds"][-1]["positions"]
            )

        self.debate_history.append(debate_session)

        return debate_session

    def _conduct_debate_round(
        self,
        topic: str,
        context: Dict[str, Any],
        participants: List[str],
        round_num: int,
    ) -> Dict[str, Any]:
        """Conduct single round of agent debate."""

        positions: Dict[str, Dict[str, Any]] = {}
        arguments: Dict[str, Dict[str, Any]] = {}

        for agent_name in participants:
            agent = self.agents[agent_name]

            try:
                position = agent.debate_position(topic, context)
                positions[agent_name] = position
                arguments[agent_name] = {
                    "stance": position.get("position", ""),
                    "reasoning": position.get("reasoning", ""),
                    "evidence": position.get("evidence", []),
                    "confidence": position.get("confidence", 0.5),
                }
            except Exception as exc:  # pragma: no cover - defensive fallback
                positions[agent_name] = self._generate_fallback_position(agent_name, topic, exc)

        conflicts = self._identify_conflicts(positions)
        challenges = self._generate_challenges(positions)

        return {
            "round": round_num,
            "positions": positions,
            "arguments": arguments,
            "conflicts": conflicts,
            "challenges": challenges,
            "key_insights": self._extract_round_insights(positions, conflicts),
        }

    def _evaluate_consensus(self, positions: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if consensus has been reached among agents."""

        stances: List[str] = []
        confidences: List[float] = []

        for position in positions.values():
            stances.append(position.get("position", "").lower())
            confidences.append(position.get("confidence", 0.5))

        consensus_score = self._calculate_consensus_score(stances, confidences)
        consensus_achieved = consensus_score >= self.consensus_threshold

        if consensus_achieved:
            consensus_position = self._synthesize_consensus_position(positions)
        else:
            consensus_position = None

        return {
            "consensus_achieved": consensus_achieved,
            "consensus_score": consensus_score,
            "consensus_position": consensus_position,
            "agreement_areas": self._identify_agreement_areas(positions),
            "disagreement_areas": self._identify_disagreement_areas(positions),
        }

    def _calculate_consensus_score(
        self, stances: List[str], confidences: List[float]
    ) -> float:
        """Calculate consensus score based on stance similarity and confidence."""

        if len(stances) < 2:
            return 1.0

        similarity_scores: List[float] = []

        for i in range(len(stances)):
            for j in range(i + 1, len(stances)):
                words_i = set(stances[i].split())
                words_j = set(stances[j].split())

                if not words_i or not words_j:
                    similarity = 0.0
                else:
                    intersection = len(words_i.intersection(words_j))
                    union = len(words_i.union(words_j))
                    similarity = intersection / union if union else 0.0

                weight = (confidences[i] + confidences[j]) / 2
                similarity_scores.append(similarity * weight)

        return sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0

    def _synthesize_consensus_position(
        self, positions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize consensus position from individual agent positions."""

        all_evidence: List[str] = []
        all_reasoning: List[str] = []
        weighted_confidence = 0.0

        for agent_name, position in positions.items():
            all_evidence.extend(position.get("evidence", []))
            all_reasoning.append(f"{agent_name}: {position.get('reasoning', '')}")
            weighted_confidence += position.get("confidence", 0.5)

        weighted_confidence /= len(positions)
        stances = [pos.get("position", "") for pos in positions.values()]
        consensus_stance = self._find_common_elements(stances)

        return {
            "consensus_stance": consensus_stance,
            "combined_reasoning": all_reasoning,
            "supporting_evidence": list(dict.fromkeys(all_evidence)),
            "consensus_confidence": weighted_confidence,
            "contributing_agents": list(positions.keys()),
            "synthesis_method": "weighted_combination",
        }

    def _make_weighted_decision(self, positions: Dict[str, Any]) -> Dict[str, Any]:
        """Make weighted decision when consensus isn't reached."""

        weighted_positions: List[Dict[str, Any]] = []

        for agent_name, position in positions.items():
            confidence = position.get("confidence", 0.5)
            expertise_weights = {
                "content_strategist": 1.0,
                "engagement_expert": 0.9,
                "growth_hacker": 0.9,
                "funnel_architect": 0.85,
            }
            expertise_weight = expertise_weights.get(agent_name, 0.8)
            total_weight = confidence * expertise_weight

            weighted_positions.append(
                {
                    "agent": agent_name,
                    "position": position,
                    "weight": total_weight,
                }
            )

        weighted_positions.sort(key=lambda item: item["weight"], reverse=True)
        dominant_position = weighted_positions[0]

        return {
            "decision_method": "weighted_selection",
            "selected_position": dominant_position["position"],
            "selected_agent": dominant_position["agent"],
            "selection_weight": dominant_position["weight"],
            "alternative_positions": [
                {"agent": pos["agent"], "weight": pos["weight"]}
                for pos in weighted_positions[1:]
            ],
            "decision_confidence": dominant_position["weight"],
        }

    def _identify_conflicts(self, positions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify conflicting positions between agents."""

        conflicts: List[Dict[str, Any]] = []
        agent_names = list(positions.keys())

        for i in range(len(agent_names)):
            for j in range(i + 1, len(agent_names)):
                agent_a = agent_names[i]
                agent_b = agent_names[j]

                pos_a = positions[agent_a].get("position", "")
                pos_b = positions[agent_b].get("position", "")

                if self._detect_conflict(pos_a, pos_b):
                    conflicts.append(
                        {
                            "agents": [agent_a, agent_b],
                            "conflict_type": "stance_disagreement",
                            "position_a": pos_a,
                            "position_b": pos_b,
                            "resolution_needed": True,
                        }
                    )

        return conflicts

    def _detect_conflict(self, stance_a: str, stance_b: str) -> bool:
        """Detect if two stances are in conflict."""

        conflict_indicators = [
            ("prioritize", "avoid"),
            ("increase", "decrease"),
            ("focus on", "ignore"),
            ("essential", "unnecessary"),
            ("high priority", "low priority"),
        ]

        stance_a_lower = stance_a.lower()
        stance_b_lower = stance_b.lower()

        for indicator_a, indicator_b in conflict_indicators:
            if (indicator_a in stance_a_lower and indicator_b in stance_b_lower) or (
                indicator_b in stance_a_lower and indicator_a in stance_b_lower
            ):
                return True

        return False

    def _generate_challenges(self, positions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cross-agent challenges and questions."""

        challenges: List[Dict[str, Any]] = []

        for challenger_name, challenger_pos in positions.items():
            for target_name, target_pos in positions.items():
                if challenger_name == target_name:
                    continue

                challenge = self._create_challenge(
                    challenger_name, challenger_pos, target_name, target_pos
                )
                if challenge:
                    challenges.append(challenge)

        return challenges

    def _create_challenge(
        self,
        challenger: str,
        challenger_pos: Dict[str, Any],
        target: str,
        target_pos: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Create specific challenge between two agents."""

        challenger_confidence = challenger_pos.get("confidence", 0.5)
        target_confidence = target_pos.get("confidence", 0.5)

        if challenger_confidence <= target_confidence:
            return None

        return {
            "challenger": challenger,
            "target": target,
            "challenge_type": "evidence_request",
            "question": (
                "How does your position account for the evidence that "
                f"{challenger_pos.get('reasoning', '')}?"
            ),
            "challenger_evidence": challenger_pos.get("evidence", []),
            "confidence_gap": challenger_confidence - target_confidence,
        }

    def get_debate_summary(self, debate_id: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of debate session."""

        if debate_id is None and self.debate_history:
            debate = self.debate_history[-1]
        else:
            debate = next(
                (session for session in self.debate_history if session.get("id") == debate_id),
                None,
            )

        if not debate:
            return {"error": "Debate session not found"}

        return {
            "topic": debate["topic"],
            "participants": debate["participants"],
            "total_rounds": len(debate["rounds"]),
            "consensus_reached": debate["consensus_reached"],
            "final_decision": debate["final_decision"],
            "key_insights": self._extract_debate_insights(debate),
            "decision_confidence": self._calculate_decision_confidence(debate),
            "implementation_recommendations": self._generate_implementation_recommendations(
                debate
            ),
        }

    def _extract_round_insights(
        self, positions: Dict[str, Any], conflicts: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract insights from a single debate round."""

        insights: List[str] = []

        for position in positions.values():
            insights.extend(position.get("evidence", []))

        if conflicts:
            insights.append("Conflicting stances identified")

        return list(dict.fromkeys(insights))

    def _extract_debate_insights(self, debate: Dict[str, Any]) -> List[str]:
        """Extract key insights from debate session."""

        insights: List[str] = []

        for round_data in debate["rounds"]:
            round_insights = round_data.get("key_insights", [])
            insights.extend(round_insights)

        return list(dict.fromkeys(insights))

    def _calculate_decision_confidence(self, debate: Dict[str, Any]) -> float:
        """Calculate confidence in final decision."""

        if debate["consensus_reached"]:
            final = debate["final_decision"] or {}
            return final.get("consensus_confidence", 0.8)

        final = debate["final_decision"] or {}
        return final.get("decision_confidence", 0.6)

    def _generate_implementation_recommendations(
        self, debate: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on debate outcome."""

        if debate["consensus_reached"]:
            stance = debate["final_decision"].get("consensus_stance", "")
            return [f"Implement consensus stance: {stance}"]

        selection = debate["final_decision"].get("selected_agent", "unknown")
        return [f"Proceed with weighted decision from {selection}"]

    def _find_common_elements(self, stances: List[str]) -> str:
        """Find common keywords across stances."""

        if not stances:
            return ""

        keyword_counts: Dict[str, int] = {}
        for stance in stances:
            for keyword in stance.split():
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        sorted_keywords = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)
        top_keywords = [keyword for keyword, count in sorted_keywords if count > 1]
        return " ".join(top_keywords)

    def _identify_agreement_areas(self, positions: Dict[str, Any]) -> List[str]:
        """Identify areas of agreement."""

        stances = [position.get("position", "") for position in positions.values()]
        return [self._find_common_elements(stances)] if stances else []

    def _identify_disagreement_areas(self, positions: Dict[str, Any]) -> List[str]:
        """Identify areas of disagreement."""

        conflicts = self._identify_conflicts(positions)
        return [json.dumps(conflict) for conflict in conflicts]

    def _generate_fallback_position(
        self, agent_name: str, topic: str, error: Exception
    ) -> Dict[str, Any]:
        """Generate fallback position for agent failure."""

        return {
            "position": f"Unable to provide detailed stance on {topic}",
            "reasoning": f"Fallback due to error: {error}",
            "evidence": [],
            "confidence": 0.3,
        }


AgentDebate = AgentDebateSystem
