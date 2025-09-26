import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)


class TestLunaAPIIntegration:
    """Test Luna AI API integration"""

    def test_luna_health_endpoint(self):
        """Test Luna health check"""
        response = client.get("/luna/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["prompt_modules"] == 10
        assert "prompt_manager" in data["systems"]

    def test_luna_prompt_modules_endpoint(self):
        """Test prompt modules information"""
        response = client.get("/luna/prompt-modules")
        assert response.status_code == 200
        data = response.json()
        assert data["total_modules"] == 10
        assert len(data["core_modules"]) == 3
        assert "strategy_consultation" in data["query_types"]

    def test_strategy_consultation_query(self):
        """Test strategy consultation query type"""
        request_data = {
            "query": "I'm a fitness coach with 2,500 followers and want to grow to 10K in 3 months. My engagement rate is around 4% and I post 3 times per week. What strategy should I follow?",
            "user_id": "test_user_1",
            "account_context": {
                "followers": 2500,
                "engagement_rate": 0.04,
                "posting_frequency": 3,
                "niche": "fitness"
            }
        }

        response = client.post("/luna/query", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert data["query_type"] == "strategy_consultation"
        assert data["confidence"] >= 80
        assert "Instagram Growth Strategy Analysis" in data["response"]
        assert len(data["modules_used"]) >= 2
        assert data["session_id"] is not None

    def test_content_creation_query(self):
        """Test content creation query type"""
        request_data = {
            "query": "I need content ideas for my travel blog. What should I post to get more engagement?",
            "user_id": "test_user_2",
            "account_context": {
                "niche": "travel",
                "followers": 1200
            }
        }

        response = client.post("/luna/query", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert data["query_type"] == "content_creation"
        assert "SPARK" in data["response"] or "content" in data["response"].lower()
        assert len(data["citations"]) >= 1

    def test_growth_troubleshooting_query(self):
        """Test growth troubleshooting query type"""
        request_data = {
            "query": "My reach suddenly dropped 60% last week and I think I might be shadow-banned. Help!",
            "user_id": "test_user_3"
        }

        response = client.post("/luna/query", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert data["query_type"] == "growth_troubleshooting"
        assert data["confidence"] >= 85
        assert "shadow" in data["response"].lower() or "troubleshooting" in data["response"].lower()

    def test_competitor_research_query(self):
        """Test competitor research query type"""
        request_data = {
            "query": "Can you analyze my competitor accounts and tell me what they're doing better?",
            "user_id": "test_user_4",
            "account_context": {
                "niche": "fitness",
                "competitors": ["@fitnessguru", "@workoutqueen"]
            }
        }

        response = client.post("/luna/query", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert data["query_type"] == "competitor_research"
        assert "competitive_intelligence" in data["modules_used"]

    def test_trend_analysis_query(self):
        """Test trend analysis query type"""
        request_data = {
            "query": "What are the trending content formats on Instagram right now?",
            "user_id": "test_user_5"
        }

        response = client.post("/luna/query", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert data["query_type"] == "trend_analysis"
        assert "trend" in data["response"].lower()

    def test_enhanced_chat_endpoint(self):
        """Test enhanced chat endpoint using Luna"""
        request_data = {
            "message": "Help me create a content strategy for my bakery account",
            "user_id": "test_bakery",
            "context": {
                "business_type": "bakery",
                "location": "local"
            }
        }

        response = client.post("/chat", json=request_data)
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "query_type" in data
        assert "confidence" in data
        assert data["confidence"] >= 50

    def test_memory_persistence(self):
        """Test that user memory persists across queries"""
        user_id = "memory_test_user"

        # First query
        request1 = {
            "query": "I'm a fitness coach with 5000 followers",
            "user_id": user_id,
            "account_context": {"followers": 5000, "niche": "fitness"}
        }

        response1 = client.post("/luna/query", json=request1)
        session_id = response1.json()["session_id"]

        # Second query referencing previous context
        request2 = {
            "query": "What content strategy should I use based on my account?",
            "user_id": user_id,
            "session_id": session_id
        }

        response2 = client.post("/luna/query", json=request2)

        assert response2.status_code == 200
        # Response should reference fitness context from previous interaction

    def test_error_handling(self):
        """Test API error handling"""
        # Test with invalid request
        response = client.post("/luna/query", json={"invalid": "request"})
        assert response.status_code == 422  # Validation error

        # Test with empty query
        response = client.post("/luna/query", json={"query": ""})
        assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
