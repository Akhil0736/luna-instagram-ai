import pytest
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from orchestration.luna_master_orchestrator import LunaMasterOrchestrator

@pytest.fixture
async def orchestrator():
    return LunaMasterOrchestrator()

@pytest.mark.asyncio
async def test_breathwork_coach_scenario(orchestrator):
    """Test the complete breathwork coach scenario"""
    
    user_input = "hey im a breathwork coach and i help entrepreneurs regulate their nervous system so that they can function better and live better life, my goal is to get leads/clients for my program through organic content with instagram reels"
    user_id = "test_user_123"
    
    # Phase 1: Initial consultation
    result1 = await orchestrator.initiate_luna_consultation(user_input, user_id)
    assert result1["status"] == "conversation_active"
    assert len(result1["questions"]) > 3
    
    # Phase 2: Response processing  
    responses = {
        "content_type": "breathing exercises and entrepreneur stress management",
        "competitors": "davidmeltzer, breathwithsandy, thestresscoach",
        "current_followers": "1200",
        "lead_magnet": "5-minute morning breathing routine"
    }
    
    result2 = await orchestrator.process_user_responses(user_id, responses)
    assert result2["status"] in ["initiating_research", "additional_questions"]
    
    print("✅ Breathwork coach scenario test passed")

if __name__ == "__main__":
    asyncio.run(test_breathwork_coach_scenario(LunaMasterOrchestrator()))
