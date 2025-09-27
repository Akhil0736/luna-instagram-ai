"""Luna Autonomous Agent - OpenManus-Inspired Base Architecture"""
from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, model_validator
import asyncio
import uuid
import json
from dataclasses import dataclass


class AgentState(Enum):
    """Agent operational states inspired by OpenManus"""

    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    LEARNING = "learning"
    ERROR = "error"
    FINISHED = "finished"


class DecisionConfidence(Enum):
    """Decision confidence levels"""

    VERY_HIGH = "very_high"  # 90-100%
    HIGH = "high"  # 75-89%
    MEDIUM = "medium"  # 50-74%
    LOW = "low"  # 25-49%
    VERY_LOW = "very_low"  # 0-24%


@dataclass
class AgentMemoryEntry:
    """Memory entry for agent experiences"""

    timestamp: datetime
    action: str
    context: Dict[str, Any]
    outcome: Dict[str, Any]
    success_score: float
    lesson_learned: str


@dataclass
class AutonomousDecision:
    """Autonomous decision data structure"""

    decision_id: str
    timestamp: datetime
    agent_name: str
    decision_type: str
    context: Dict[str, Any]
    reasoning: str
    confidence: DecisionConfidence
    expected_outcome: Dict[str, Any]
    risk_assessment: Dict[str, Any]


class InstagramContext(BaseModel):
    """Instagram-specific context for Luna agents"""

    user_id: Optional[str] = None
    account_type: Optional[str] = None  # business, creator, personal
    follower_count: int = 0
    engagement_rate: float = 0.0
    posting_frequency: int = 0
    niche: Optional[str] = None
    goals: List[str] = Field(default_factory=list)
    recent_performance: Dict[str, Any] = Field(default_factory=dict)
    competitor_data: Dict[str, Any] = Field(default_factory=dict)


class LunaAutonomousAgent(BaseModel, ABC):
    """Enhanced autonomous agent architecture inspired by OpenManus BaseAgent"""

    # Core agent properties
    name: str = Field(..., description="Unique agent name")
    description: Optional[str] = Field(None, description="Agent description")
    agent_type: str = Field(..., description="Type of autonomous agent")

    # State management
    state: AgentState = Field(default=AgentState.IDLE)
    current_step: int = Field(default=0)
    max_steps: int = Field(default=20)

    # Instagram-specific context
    instagram_context: InstagramContext = Field(default_factory=InstagramContext)

    # Memory and learning
    memory_entries: List[AgentMemoryEntry] = Field(default_factory=list)
    decision_history: List[AutonomousDecision] = Field(default_factory=list)
    learning_parameters: Dict[str, float] = Field(default_factory=dict)

    # Performance tracking
    success_rate: float = Field(default=0.0)
    total_decisions: int = Field(default=0)
    confidence_calibration: Dict[str, float] = Field(default_factory=dict)

    # Configuration
    autonomous_mode: bool = Field(default=True)
    learning_enabled: bool = Field(default=True)
    risk_tolerance: float = Field(default=0.5)  # 0.0 = very conservative, 1.0 = very aggressive

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

    @model_validator(mode="after")
    def initialize_agent(self) -> "LunaAutonomousAgent":
        """Initialize agent with default learning parameters"""
        if not self.learning_parameters:
            self.learning_parameters = {
                "learning_rate": 0.1,
                "experience_weight": 0.8,
                "confidence_threshold": 0.7,
                "risk_adjustment_factor": 0.2,
            }
        return self

    @asynccontextmanager
    async def state_context(self, new_state: AgentState):
        """Context manager for safe agent state transitions"""
        if not isinstance(new_state, AgentState):
            raise ValueError(f"Invalid state: {new_state}")

        previous_state = self.state
        self.state = new_state

        try:
            yield
        except Exception as e:  # pylint: disable=broad-except
            self.state = AgentState.ERROR
            await self.log_error(e, previous_state)
            raise
        finally:
            # Only restore if we're not in an error state
            if self.state != AgentState.ERROR:
                self.state = previous_state

    async def run_autonomous_cycle(
        self, context: Dict[str, Any], max_iterations: int = 10
    ) -> Dict[str, Any]:
        """Execute autonomous decision-making cycle"""
        cycle_results = []
        cycle_id = str(uuid.uuid4())

        try:
            async with self.state_context(AgentState.ANALYZING):
                for iteration in range(max_iterations):
                    self.current_step = iteration + 1

                    # Step 1: Analyze current situation
                    situation_analysis = await self.analyze_situation(context)

                    # Step 2: Make autonomous decision
                    decision = await self.make_autonomous_decision(situation_analysis)

                    # Step 3: Execute decision if confidence is sufficient
                    execution_result = await self.execute_decision(decision)

                    # Step 4: Learn from outcome
                    learning_result = await self.learn_from_outcome(decision, execution_result)

                    step_result = {
                        "iteration": iteration + 1,
                        "situation_analysis": situation_analysis,
                        "decision": decision,
                        "execution_result": execution_result,
                        "learning_result": learning_result,
                        "agent_state": self.state.value,
                    }

                    cycle_results.append(step_result)

                    # Check if goal achieved or should stop
                    if execution_result.get("goal_achieved") or execution_result.get("should_stop"):
                        break

                    # Add delay for realistic decision-making
                    await asyncio.sleep(0.1)

                return {
                    "cycle_id": cycle_id,
                    "agent": self.name,
                    "total_iterations": self.current_step,
                    "results": cycle_results,
                    "final_state": self.state.value,
                    "performance_summary": self.get_performance_summary(),
                    "learning_gained": self.extract_learning_insights(),
                }

        except Exception as e:  # pylint: disable=broad-except
            await self.log_error(e, AgentState.ANALYZING)
            return {
                "cycle_id": cycle_id,
                "error": str(e),
                "agent": self.name,
                "final_state": AgentState.ERROR.value,
            }

    @abstractmethod
    async def analyze_situation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current situation and identify opportunities/challenges"""

    @abstractmethod
    async def make_autonomous_decision(
        self, situation_analysis: Dict[str, Any]
    ) -> AutonomousDecision:
        """Make autonomous decision based on situation analysis"""

    @abstractmethod
    async def execute_decision(self, decision: AutonomousDecision) -> Dict[str, Any]:
        """Execute the autonomous decision"""

    async def learn_from_outcome(
        self, decision: AutonomousDecision, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Learn from decision outcome and update agent parameters"""
        if not self.learning_enabled:
            return {"learning": "disabled"}

        # Calculate success score
        success_score = self._calculate_success_score(outcome)

        # Create memory entry
        memory_entry = AgentMemoryEntry(
            timestamp=datetime.now(),
            action=decision.decision_type,
            context=decision.context,
            outcome=outcome,
            success_score=success_score,
            lesson_learned=self._extract_lesson(decision, outcome, success_score),
        )

        self.memory_entries.append(memory_entry)

        # Update learning parameters
        learning_update = self._update_learning_parameters(success_score, decision.confidence)

        # Update performance metrics
        self._update_performance_metrics(success_score)

        # Limit memory to last 100 entries
        if len(self.memory_entries) > 100:
            self.memory_entries = self.memory_entries[-100:]

        return {
            "success_score": success_score,
            "learning_update": learning_update,
            "memory_entries_count": len(self.memory_entries),
            "updated_success_rate": self.success_rate,
        }

    def _calculate_success_score(self, outcome: Dict[str, Any]) -> float:
        """Calculate success score from outcome (0.0 to 1.0)"""
        # Base implementation - can be overridden by specific agents
        if outcome.get("error"):
            return 0.0

        success_indicators = outcome.get("success_indicators", {})
        if not success_indicators:
            return 0.5  # Neutral if no indicators

        # Weight different success indicators
        weights = {
            "goal_achieved": 0.4,
            "user_satisfaction": 0.3,
            "performance_improvement": 0.2,
            "efficiency": 0.1,
        }

        weighted_score = 0.0
        total_weight = 0.0

        for indicator, weight in weights.items():
            if indicator in success_indicators:
                weighted_score += success_indicators[indicator] * weight
                total_weight += weight

        return weighted_score / total_weight if total_weight > 0 else 0.5

    def _extract_lesson(
        self, decision: AutonomousDecision, outcome: Dict[str, Any], success_score: float
    ) -> str:
        """Extract lesson learned from decision outcome"""
        if success_score >= 0.8:
            return (
                f"High success with {decision.decision_type} in "
                f"{decision.context.get('situation', 'unknown')} context"
            )
        if success_score >= 0.6:
            return f"Moderate success with {decision.decision_type}, room for optimization"
        if success_score >= 0.4:
            return f"Mixed results with {decision.decision_type}, need refinement"
        return f"Poor outcome with {decision.decision_type}, avoid similar decisions"

    def _update_learning_parameters(
        self, success_score: float, decision_confidence: DecisionConfidence
    ) -> Dict[str, float]:
        """Update learning parameters based on outcome"""
        learning_rate = self.learning_parameters["learning_rate"]

        # Adjust learning rate based on success
        if success_score > 0.8:
            # Successful decisions -> slight increase in confidence
            self.learning_parameters["confidence_threshold"] += 0.01
        elif success_score < 0.3:
            # Poor decisions -> decrease confidence, increase learning rate
            self.learning_parameters["confidence_threshold"] -= 0.02
            self.learning_parameters["learning_rate"] = min(0.3, learning_rate * 1.1)

        # Adjust risk tolerance
        if success_score > 0.7 and self.risk_tolerance < 0.8:
            self.risk_tolerance += 0.05
        elif success_score < 0.4 and self.risk_tolerance > 0.2:
            self.risk_tolerance -= 0.05

        return self.learning_parameters.copy()

    def _update_performance_metrics(self, success_score: float):
        """Update agent performance metrics"""
        self.total_decisions += 1

        # Update success rate with exponential moving average
        alpha = 0.1  # Learning rate for moving average
        self.success_rate = (1 - alpha) * self.success_rate + alpha * success_score

    async def log_error(self, error: Exception, previous_state: AgentState):
        """Log error with context information"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "error": str(error),
            "previous_state": previous_state.value,
            "instagram_context": self.instagram_context.model_dump(),
            "current_step": self.current_step,
        }

        # In a real implementation, this would log to a proper logging system
        print(f"[ERROR] {self.name}: {error}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get agent performance summary"""
        recent_decisions = self.decision_history[-10:] if self.decision_history else []
        recent_memories = self.memory_entries[-10:] if self.memory_entries else []

        return {
            "success_rate": round(self.success_rate, 3),
            "total_decisions": self.total_decisions,
            "recent_performance": [m.success_score for m in recent_memories],
            "confidence_calibration": self.confidence_calibration,
            "learning_parameters": self.learning_parameters,
            "risk_tolerance": self.risk_tolerance,
            "memory_entries": len(self.memory_entries),
        }

    def extract_learning_insights(self) -> List[str]:
        """Extract key learning insights from memory"""
        if len(self.memory_entries) < 3:
            return ["Insufficient data for insights"]

        insights = []

        # Analyze success patterns
        successful_actions = [m for m in self.memory_entries if m.success_score >= 0.7]
        if successful_actions:
            common_contexts = self._find_common_patterns([m.context for m in successful_actions])
            if common_contexts:
                insights.append(f"Success pattern identified: {common_contexts}")

        # Analyze failure patterns
        failed_actions = [m for m in self.memory_entries if m.success_score <= 0.3]
        if failed_actions:
            failure_patterns = self._find_common_patterns([m.context for m in failed_actions])
            if failure_patterns:
                insights.append(f"Failure pattern identified: {failure_patterns}")

        # Performance trend
        if len(self.memory_entries) >= 5:
            recent_scores = [m.success_score for m in self.memory_entries[-5:]]
            avg_recent = sum(recent_scores) / len(recent_scores)
            if avg_recent > self.success_rate:
                insights.append("Performance is improving")
            elif avg_recent < self.success_rate - 0.1:
                insights.append("Performance needs attention")

        return insights or ["No significant patterns identified yet"]

    def _find_common_patterns(self, contexts: List[Dict[str, Any]]) -> str:
        """Find common patterns in contexts"""
        if not contexts:
            return ""

        # Simple pattern detection - could be enhanced with ML
        common_keys = set(contexts[0].keys())
        for context in contexts[1:]:
            common_keys &= set(context.keys())

        if common_keys:
            return f"Common context elements: {list(common_keys)[:3]}"

        return "No clear patterns"

    async def update_instagram_context(self, new_context: Dict[str, Any]):
        """Update Instagram context with new data"""
        if "user_id" in new_context:
            self.instagram_context.user_id = new_context["user_id"]
        if "follower_count" in new_context:
            self.instagram_context.follower_count = new_context["follower_count"]
        if "engagement_rate" in new_context:
            self.instagram_context.engagement_rate = new_context["engagement_rate"]
        if "niche" in new_context:
            self.instagram_context.niche = new_context["niche"]
        if "goals" in new_context:
            self.instagram_context.goals = new_context["goals"]
        if "recent_performance" in new_context:
            self.instagram_context.recent_performance = new_context["recent_performance"]

    def get_decision_recommendation(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Get decision recommendation based on past experience"""
        similar_experiences = [
            m for m in self.memory_entries if self._context_similarity(m.context, situation) > 0.7
        ]

        if not similar_experiences:
            return {
                "recommendation": "No similar experience found",
                "confidence": DecisionConfidence.LOW,
                "reasoning": "This is a new situation for the agent",
            }

        # Find most successful approach
        best_experience = max(similar_experiences, key=lambda x: x.success_score)

        confidence = (
            DecisionConfidence.HIGH if best_experience.success_score > 0.8 else DecisionConfidence.MEDIUM
        )

        return {
            "recommendation": best_experience.action,
            "confidence": confidence,
            "reasoning": (
                f"Based on similar situation with {best_experience.success_score:.1%} success rate"
            ),
            "lesson": best_experience.lesson_learned,
        }

    def _context_similarity(self, context1: Dict[str, Any], context2: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts (0.0 to 1.0)"""
        if not context1 or not context2:
            return 0.0

        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0

        similarity_scores = []
        for key in common_keys:
            val1, val2 = context1[key], context2[key]

            if isinstance(val1, str) and isinstance(val2, str):
                # Simple string similarity
                similarity_scores.append(1.0 if val1 == val2 else 0.3)
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Numerical similarity
                if val1 == 0 and val2 == 0:
                    similarity_scores.append(1.0)
                elif val1 == 0 or val2 == 0:
                    similarity_scores.append(0.0)
                else:
                    similarity_scores.append(
                        1.0 - abs(val1 - val2) / max(abs(val1), abs(val2))
                    )
            else:
                similarity_scores.append(0.5)  # Default for other types

        return sum(similarity_scores) / len(similarity_scores)
