from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from integration.openmanus_service.app import app

client = TestClient(app)


def test_deep_scan_endpoint_stubbed_without_api_key(monkeypatch):
    # Ensure API key is not present so ScrapeDo returns a stub report
    monkeypatch.delenv("SCRAPEDO_API_KEY", raising=False)
    res = client.get("/luna/research/deep-scan", params={"niche": "fitness"})
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    assert data.get("niche") == "fitness"
    assert "items" in data
    assert isinstance(data["items"], list)
    # Expect at least one stub item
    assert len(data["items"]) >= 1
