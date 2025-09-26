"""Facade exposing the implementation layer to the core Luna system."""
from typing import Any, Dict
from ..orchestration.agent_orchestrator import ImplementationAgentOrchestrator 

class ImplementationOrchestratorFacade:
    """Entry point used by Luna runtime to produce execution-ready plans."""

    def __init__(self) -> None:
        self.orchestrator = ImplementationAgentOrchestrator()

    def create_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.orchestrator.run_pipeline(context)
