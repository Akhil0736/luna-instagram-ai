"""Consensus Building System - Advanced Multi-Agent Agreement Protocols"""
from __future__ import annotations

from enum import Enum
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple


class ConsensusMethod(Enum):
    """Different consensus building approaches."""

    CONVENTIONAL = "conventional"
    SINGLE_TEXT = "single_text"
    VISIONING = "visioning"
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_VOTE = "weighted_vote"


class ConsensusBuilder:
    """Advanced consensus building using multiple proven methodologies."""

    def __init__(self) -> None:
        self.consensus_methods = {
            ConsensusMethod.CONVENTIONAL: self._conventional_consensus,
            ConsensusMethod.SINGLE_TEXT: self._single_text_consensus,
            ConsensusMethod.VISIONING: self._visioning_consensus,
            ConsensusMethod.MAJORITY_VOTE: self._majority_vote_consensus,
            ConsensusMethod.WEIGHTED_VOTE: self._weighted_vote_consensus,
        }

    def build_consensus(
        self,
        agent_positions: Dict[str, Any],
        method: ConsensusMethod = ConsensusMethod.CONVENTIONAL,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Build consensus using specified method."""

        consensus_function = self.consensus_methods[method]

        try:
            result = consensus_function(agent_positions, context or {})
            result["method_used"] = method.value
            result["success"] = True
            return result

        except Exception as exc:  # pragma: no cover - defensive fallback
            return {
                "success": False,
                "error": str(exc),
                "fallback_recommendation": self._generate_fallback_consensus(agent_positions),
            }

    # ---------------------------------------------------------------------
    # Conventional Consensus
    # ---------------------------------------------------------------------
    def _conventional_consensus(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Conventional consensus: Address all stakeholder interests."""

        all_interests: List[str] = []
        agent_concerns: Dict[str, List[str]] = {}

        for agent_name, position in positions.items():
            interests = self._extract_interests(position)
            concerns = self._extract_concerns(position)

            all_interests.extend(interests)
            agent_concerns[agent_name] = concerns

        unique_interests = list(dict.fromkeys(all_interests))
        comprehensive_proposals = [
            self._generate_interest_proposal(interest, agent_concerns, positions)
            for interest in unique_interests
        ]

        final_proposal = self._iterate_to_agreement(comprehensive_proposals, positions)

        return {
            "consensus_type": "comprehensive_agreement",
            "identified_interests": unique_interests,
            "stakeholder_concerns": agent_concerns,
            "final_proposal": final_proposal,
            "satisfaction_scores": self._calculate_satisfaction_scores(
                final_proposal, positions
            ),
            "implementation_confidence": 0.85,
        }

    # ---------------------------------------------------------------------
    # Single Text Consensus
    # ---------------------------------------------------------------------
    def _single_text_consensus(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Single text method: Collaborative document refinement."""

        initial_draft = self._create_neutral_draft(positions, context)
        current_draft = initial_draft
        refinement_rounds: List[Dict[str, Any]] = []
        satisfaction_level = 0.0

        for round_num in range(1, 6):
            agent_feedback: Dict[str, Dict[str, Any]] = {}
            for agent_name, position in positions.items():
                agent_feedback[agent_name] = self._get_agent_feedback(
                    agent_name, position, current_draft
                )

            refined_draft = self._apply_refinements(current_draft, agent_feedback)

            refinement_rounds.append(
                {
                    "round": round_num,
                    "draft": current_draft,
                    "feedback": agent_feedback,
                    "refinements": refined_draft["changes"],
                }
            )

            current_draft = refined_draft["text"]
            satisfaction_level = self._check_draft_satisfaction(current_draft, positions)

            if satisfaction_level >= 0.8:
                break

        return {
            "consensus_type": "collaborative_document",
            "initial_draft": initial_draft,
            "refinement_process": refinement_rounds,
            "final_document": current_draft,
            "final_satisfaction": satisfaction_level,
            "rounds_to_consensus": len(refinement_rounds),
        }

    # ---------------------------------------------------------------------
    # Visioning Consensus
    # ---------------------------------------------------------------------
    def _visioning_consensus(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Visioning approach: Focus on shared future vision."""

        long_term_goals: Dict[str, List[str]] = {}
        shared_values: List[str] = []

        for agent_name, position in positions.items():
            long_term_goals[agent_name] = self._extract_long_term_goals(position)
            shared_values.extend(self._extract_values(position))

        common_goals = self._find_common_goals(long_term_goals)
        shared_vision_elements = list(dict.fromkeys(shared_values))
        shared_vision = self._build_shared_vision(common_goals, shared_vision_elements)
        implementation_path = self._create_implementation_path(shared_vision, positions)

        return {
            "consensus_type": "shared_vision",
            "long_term_goals": long_term_goals,
            "shared_vision": shared_vision,
            "common_elements": common_goals,
            "implementation_path": implementation_path,
            "vision_alignment_score": self._calculate_vision_alignment(
                long_term_goals, shared_vision
            ),
        }

    # ---------------------------------------------------------------------
    # Majority Vote Consensus
    # ---------------------------------------------------------------------
    def _majority_vote_consensus(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Majority vote: Democratic decision making."""

        options = self._extract_voting_options(positions)
        votes: Dict[str, int] = {option: 0 for option in options}
        agent_votes: Dict[str, str] = {}

        for agent_name, position in positions.items():
            vote = self._cast_vote(agent_name, position, options)
            agent_votes[agent_name] = vote
            votes[vote] = votes.get(vote, 0) + 1

        sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
        winning_option, winning_votes = sorted_votes[0]
        total_votes = sum(votes.values()) or 1

        return {
            "consensus_type": "majority_vote",
            "options": votes,
            "agent_votes": agent_votes,
            "winning_option": winning_option,
            "winning_percentage": winning_votes / total_votes,
            "requires_runoff": len(sorted_votes) > 1 and sorted_votes[0][1] == sorted_votes[1][1],
        }

    # ---------------------------------------------------------------------
    # Weighted Vote Consensus
    # ---------------------------------------------------------------------
    def _weighted_vote_consensus(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Weighted vote: Combines expertise and confidence."""

        weights = context.get(
            "agent_weights",
            {
                "content_strategist": 1.0,
                "engagement_expert": 0.9,
                "growth_hacker": 0.9,
                "funnel_architect": 0.85,
            },
        )

        options = self._extract_voting_options(positions)
        weighted_scores: Dict[str, float] = {option: 0.0 for option in options}
        agent_support: Dict[str, Dict[str, float]] = {}

        for agent_name, position in positions.items():
            vote = self._cast_vote(agent_name, position, options)
            confidence = float(position.get("confidence", 0.5))
            weight = weights.get(agent_name, 0.8)
            score = confidence * weight

            weighted_scores[vote] = weighted_scores.get(vote, 0.0) + score
            agent_support.setdefault(vote, {})[agent_name] = score

        winning_option, winning_score = max(
            weighted_scores.items(), key=lambda item: item[1]
        )
        total_score = sum(weighted_scores.values()) or 1.0

        return {
            "consensus_type": "weighted_vote",
            "weighted_scores": weighted_scores,
            "agent_support": agent_support,
            "winning_option": winning_option,
            "winning_share": winning_score / total_score,
            "normalized_weights": weights,
        }

    # ---------------------------------------------------------------------
    # Helper Methods - Conventional Consensus
    # ---------------------------------------------------------------------
    def _extract_interests(self, position: Dict[str, Any]) -> List[str]:
        stance = position.get("position", "")
        reasoning = position.get("reasoning", "")
        evidence = position.get("evidence", [])

        interests = []
        if stance:
            interests.append(stance)
        if reasoning:
            interests.append(reasoning)
        interests.extend(evidence)

        return [interest for interest in interests if interest]

    def _extract_concerns(self, position: Dict[str, Any]) -> List[str]:
        concerns = []
        risk = position.get("risk_assessment") or position.get("risk_vs_reward")
        if isinstance(risk, dict):
            for key, value in risk.items():
                concerns.append(f"{key}: {value}")
        elif isinstance(risk, list):
            concerns.extend(risk)

        suggested_tests = position.get("suggested_tests") or position.get("experiments")
        if suggested_tests:
            concerns.extend(suggested_tests)

        return concerns or ["No explicit concerns provided"]

    def _generate_interest_proposal(
        self,
        interest: str,
        agent_concerns: Dict[str, List[str]],
        positions: Dict[str, Any],
    ) -> Dict[str, Any]:
        supporting_agents = [
            agent
            for agent, position in positions.items()
            if interest.lower() in position.get("position", "").lower()
        ]

        mitigations = [
            concern
            for agent in supporting_agents
            for concern in agent_concerns.get(agent, [])
        ]

        return {
            "interest": interest,
            "supporting_agents": supporting_agents,
            "mitigations": mitigations,
            "recommended_actions": list(dict.fromkeys(mitigations)) or [
                "Document safeguards and monitor outcomes"
            ],
        }

    def _iterate_to_agreement(
        self, proposals: List[Dict[str, Any]], positions: Dict[str, Any]
    ) -> Dict[str, Any]:
        aggregated_actions: List[str] = []
        for proposal in proposals:
            aggregated_actions.extend(proposal.get("recommended_actions", []))

        action_plan = list(dict.fromkeys(aggregated_actions))
        return {
            "proposals": proposals,
            "action_plan": action_plan,
            "review_cycle": "30_day",
        }

    def _calculate_satisfaction_scores(
        self, proposal: Dict[str, Any], positions: Dict[str, Any]
    ) -> Dict[str, float]:
        action_plan = proposal.get("action_plan", [])
        scores: Dict[str, float] = {}

        for agent_name, position in positions.items():
            stance = position.get("position", "").lower()
            if not action_plan:
                scores[agent_name] = 0.5
                continue

            matches = sum(1 for action in action_plan if action.lower() in stance)
            scores[agent_name] = max(0.3, matches / len(action_plan))

        return scores

    # ---------------------------------------------------------------------
    # Helper Methods - Single Text Consensus
    # ---------------------------------------------------------------------
    def _create_neutral_draft(
        self, positions: Dict[str, Any], context: Dict[str, Any]
    ) -> str:
        topic = context.get("topic", "strategic initiative")
        return (
            f"Draft consensus for {topic}: focus on balanced engagement, growth, "
            "and conversion priorities across agents."
        )

    def _get_agent_feedback(
        self, agent_name: str, position: Dict[str, Any], current_draft: str
    ) -> Dict[str, Any]:
        desired_keywords = set(position.get("position", "").lower().split())
        draft_keywords = set(current_draft.lower().split())
        missing = list(desired_keywords - draft_keywords)

        return {
            "agent": agent_name,
            "suggested_keywords": missing[:3],
            "confidence": position.get("confidence", 0.5),
        }

    def _apply_refinements(
        self, current_draft: str, feedback: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        additions: List[str] = []
        for item in feedback.values():
            additions.extend(item.get("suggested_keywords", []))

        unique_additions = list(dict.fromkeys(additions))[:6]
        if unique_additions:
            updated_draft = (
                f"{current_draft} Key priorities: " + ", ".join(unique_additions)
            )
        else:
            updated_draft = current_draft

        return {"text": updated_draft, "changes": unique_additions}

    def _check_draft_satisfaction(
        self, draft: str, positions: Dict[str, Any]
    ) -> float:
        if not positions:
            return 0.0

        satisfaction_levels: List[float] = []
        draft_lower = draft.lower()

        for position in positions.values():
            stance = position.get("position", "").lower()
            overlap = len(set(stance.split()).intersection(draft_lower.split()))
            satisfaction_levels.append(min(1.0, 0.2 + overlap / 10))

        return mean(satisfaction_levels)

    # ---------------------------------------------------------------------
    # Helper Methods - Visioning Consensus
    # ---------------------------------------------------------------------
    def _extract_long_term_goals(self, position: Dict[str, Any]) -> List[str]:
        evidence = position.get("evidence", [])
        reasoning = position.get("reasoning", "")
        return [*evidence, reasoning][:5]

    def _extract_values(self, position: Dict[str, Any]) -> List[str]:
        stance = position.get("position", "")
        return [word for word in stance.split() if word.isalpha()][:5]

    def _find_common_goals(
        self, goals: Dict[str, List[str]]
    ) -> List[str]:
        if not goals:
            return []

        all_goals = [set(map(str.lower, agent_goals)) for agent_goals in goals.values()]
        common = set.intersection(*all_goals) if all_goals else set()
        return list(common)

    def _build_shared_vision(
        self, common_goals: List[str], shared_values: List[str]
    ) -> str:
        goals_text = ", ".join(common_goals) if common_goals else "aligned growth"
        values_text = ", ".join(shared_values) if shared_values else "trust, innovation"
        return f"Shared vision emphasizes {goals_text} through values of {values_text}."

    def _create_implementation_path(
        self, shared_vision: str, positions: Dict[str, Any]
    ) -> List[str]:
        phases = ["Discovery", "Engagement", "Conversion", "Retention"]
        return [
            f"{phase}: Align tactics with vision statement '{shared_vision}'"
            for phase in phases
        ]

    def _calculate_vision_alignment(
        self, long_term_goals: Dict[str, List[str]], shared_vision: str
    ) -> float:
        if not long_term_goals:
            return 0.0

        vision_keywords = set(shared_vision.lower().split())
        alignment_scores: List[float] = []

        for goals in long_term_goals.values():
            goal_keywords = set(" ".join(goals).lower().split())
            if not goal_keywords:
                alignment_scores.append(0.5)
                continue
            overlap = len(goal_keywords.intersection(vision_keywords))
            alignment_scores.append(min(1.0, 0.3 + overlap / 10))

        return mean(alignment_scores)

    # ---------------------------------------------------------------------
    # Helper Methods - Voting
    # ---------------------------------------------------------------------
    def _extract_voting_options(self, positions: Dict[str, Any]) -> List[str]:
        options = [position.get("position", "undecided") for position in positions.values()]
        return list(dict.fromkeys(option or "undecided" for option in options)) or ["undecided"]

    def _cast_vote(
        self, agent_name: str, position: Dict[str, Any], options: List[str]
    ) -> str:
        stance = position.get("position", "undecided")
        if stance in options:
            return stance

        # fallback: select closest option by shared words
        stance_words = set(stance.lower().split())
        best_option = options[0]
        best_overlap = -1
        for option in options:
            overlap = len(stance_words.intersection(option.lower().split()))
            if overlap > best_overlap:
                best_option = option
                best_overlap = overlap
        return best_option

    # ---------------------------------------------------------------------
    # Helper Methods - General Utilities
    # ---------------------------------------------------------------------
    def _generate_fallback_consensus(
        self, positions: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not positions:
            return {"decision": "No agents available"}

        best_agent, best_position = max(
            positions.items(), key=lambda item: item[1].get("confidence", 0.5)
        )
        return {
            "decision": best_position.get("position", "undecided"),
            "selected_agent": best_agent,
            "confidence": best_position.get("confidence", 0.5),
        }


ConsensusEngine = ConsensusBuilder
