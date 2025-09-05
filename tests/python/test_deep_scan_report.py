from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from integration.openmanus_service.app import app

client = TestClient(app)


def test_premium_deep_scan_report_stubbed(monkeypatch):
    # Ensure no API key so ScrapeDo falls back to stub, but orchestrator still returns shape
    monkeypatch.delenv("SCRAPEDO_API_KEY", raising=False)
    res = client.get("/luna/reports/deep-scan", params={"niche": "fitness"})
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    assert data.get("niche") == "fitness"
    assert "items" in data and isinstance(data["items"], list)
    # Metrics summary block exists
    ms = data.get("metrics_summary")
    assert isinstance(ms, dict)
    for key in [
        "followers_max",
        "followers_median",
        "growth_rate_avg_pct",
        "engagement_rate_avg_pct",
        "timeline_common_days",
    ]:
        assert key in ms
    # Trending strategies and success patterns are arrays
    assert isinstance(data.get("trending_strategies"), list)
    assert isinstance(data.get("success_patterns"), list)
    # Stats present
    stats = data.get("stats")
    assert isinstance(stats, dict)
    assert "item_count" in stats and "duration_seconds" in stats
