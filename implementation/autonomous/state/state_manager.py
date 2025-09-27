"""State Management System for Luna Autonomous Agents"""
from __future__ import annotations
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
from dataclasses import dataclass, asdict


class StateTransitionType(Enum):
    """Types of state transitions"""

    NORMAL = "normal"
    EMERGENCY = "emergency"
    RECOVERY = "recovery"
    LEARNING = "learning"


@dataclass
class StateTransition:
    """State transition record"""

    from_state: str
    to_state: str
    timestamp: datetime
    agent_id: str
    transition_type: StateTransitionType
    context: Dict[str, Any]
    success: bool
    duration_ms: int


class LunaStateManager:
    """Manages state transitions and persistence for autonomous agents"""

    def __init__(self):
        self.state_history: List[StateTransition] = []
        self.agent_states: Dict[str, str] = {}
        self.state_locks: Dict[str, asyncio.Lock] = {}
        self.persistence_enabled = True

    async def transition_agent_state(
        self,
        agent_id: str,
        from_state: str,
        to_state: str,
        context: Dict[str, Any] | None = None,
        transition_type: StateTransitionType = StateTransitionType.NORMAL,
    ) -> bool:
        """Safely transition agent state with locking and logging"""

        # Get or create lock for this agent
        if agent_id not in self.state_locks:
            self.state_locks[agent_id] = asyncio.Lock()

        async with self.state_locks[agent_id]:
            start_time = datetime.now()

            try:
                # Validate transition
                if not self._validate_transition(from_state, to_state):
                    return False

                # Update state
                self.agent_states[agent_id] = to_state

                # Record transition
                transition = StateTransition(
                    from_state=from_state,
                    to_state=to_state,
                    timestamp=start_time,
                    agent_id=agent_id,
                    transition_type=transition_type,
                    context=context or {},
                    success=True,
                    duration_ms=int((datetime.now() - start_time).total_seconds() * 1000),
                )

                self.state_history.append(transition)

                # Persist state if enabled
                if self.persistence_enabled:
                    await self._persist_state_change(transition)

                return True

            except Exception as e:  # pylint: disable=broad-except
                # Record failed transition
                transition = StateTransition(
                    from_state=from_state,
                    to_state=to_state,
                    timestamp=start_time,
                    agent_id=agent_id,
                    transition_type=transition_type,
                    context={"error": str(e), **(context or {})},
                    success=False,
                    duration_ms=int((datetime.now() - start_time).total_seconds() * 1000),
                )

                self.state_history.append(transition)
                return False

    def _validate_transition(self, from_state: str, to_state: str) -> bool:
        """Validate if state transition is allowed"""
        # Define allowed transitions
        allowed_transitions = {
            "idle": ["analyzing", "error"],
            "analyzing": ["planning", "idle", "error"],
            "planning": ["executing", "analyzing", "error"],
            "executing": ["learning", "analyzing", "finished", "error"],
            "learning": ["idle", "analyzing", "error"],
            "error": ["idle", "analyzing"],
            "finished": ["idle"],
        }

        return to_state in allowed_transitions.get(from_state, [])

    async def _persist_state_change(self, transition: StateTransition):
        """Persist state change to storage (placeholder for Redis/Supabase integration)"""
        # In real implementation, this would save to Redis or Supabase
        state_data = {
            "transition": asdict(transition),
            "timestamp": transition.timestamp.isoformat(),
        }
        _ = state_data  # Placeholder to indicate variable usage
        # await self.redis_client.lpush(f"state_history:{transition.agent_id}", json.dumps(state_data))

    def get_agent_state(self, agent_id: str) -> Optional[str]:
        """Get current state of an agent"""
        return self.agent_states.get(agent_id)

    def get_state_history(self, agent_id: str, limit: int = 10) -> List[StateTransition]:
        """Get state history for an agent"""
        agent_history = [t for t in self.state_history if t.agent_id == agent_id]
        return agent_history[-limit:] if agent_history else []

    def get_performance_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Get state-based performance metrics for an agent"""
        agent_transitions = [t for t in self.state_history if t.agent_id == agent_id]

        if not agent_transitions:
            return {"error": "No transition history found"}

        total_transitions = len(agent_transitions)
        successful_transitions = len([t for t in agent_transitions if t.success])

        # Average transition duration
        durations = [t.duration_ms for t in agent_transitions if t.success]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # State distribution
        state_counts: Dict[str, int] = {}
        for transition in agent_transitions:
            state_counts[transition.to_state] = state_counts.get(transition.to_state, 0) + 1

        return {
            "total_transitions": total_transitions,
            "success_rate": successful_transitions / total_transitions,
            "average_duration_ms": avg_duration,
            "state_distribution": state_counts,
            "current_state": self.get_agent_state(agent_id),
            "last_transition": agent_transitions[-1].timestamp.isoformat()
            if agent_transitions
            else None,
        }


# Global state manager instance
luna_state_manager = LunaStateManager()
