"""Integration coverage for the new implementation orchestration layer."""
from implementation.orchestration.agent_orchestrator import ImplementationAgentOrchestrator

def test_orchestrator_pipeline():
    orchestrator = ImplementationAgentOrchestrator()
    output = orchestrator.run_pipeline({"topic": "growth"})
    assert "aligned_strategy" in output
