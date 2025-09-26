"""Unit coverage for Luna implementation agents."""
from implementation.agents.content_strategist import ContentStrategist

def test_content_strategist_returns_context():
    strategist = ContentStrategist()
    result = strategist.analyze({"topic": "growth"})
    assert "context" in result
