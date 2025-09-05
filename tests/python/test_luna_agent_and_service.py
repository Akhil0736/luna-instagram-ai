from __future__ import annotations

import os
import pytest
from fastapi.testclient import TestClient

from integration.openmanus_service.app import app


@pytest.fixture(autouse=True)
def clear_api_keys(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("SCRAPEDO_API_KEY", raising=False)
    monkeypatch.delenv("APIFY_TOKEN", raising=False)


client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body.get("ok") is True


def test_comprehensive_research_full_endpoint():
    res = client.get("/luna/research/full", params={"niche": "fitness", "goal": "Grow followers by 20% in 60 days"})
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    # Structure checks
    assert "raw_insights" in data
    assert "synthesized" in data
    assert isinstance(data["raw_insights"], list)


def test_process_goal_end_to_end_with_stubbed_research():
    payload = {
        "target_metric": "followers",
        "target_increase": 0.2,
        "timeline_days": 60,
        "niche": "fitness",
        "current_followers": 1000,
    }
    res = client.post("/luna/process-goal", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    plan = data.get("growth_plan")
    assert isinstance(plan, dict)
    # Minimal structure expectations
    assert "research_summary" in plan
    assert "content_calendar" in plan
    assert "automation_plan" in plan
