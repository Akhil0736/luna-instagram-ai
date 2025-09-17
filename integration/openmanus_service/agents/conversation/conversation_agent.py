import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime

class ConversationAgent:
    def __init__(self):
        self.conversation_history = {}
    
    async def process_initial_input(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Process initial user input and extract context"""
        
        context = {
            "niche": self._extract_niche(user_input),
            "goals": self._extract_goals(user_input),
            "platform": "instagram" if "instagram" in user_input.lower() else "social_media",
            "target_audience": self._extract_audience(user_input)
        }
        
        questions = self._generate_contextual_questions(context, user_input)
        
        return {
            "conversation_id": user_id,
            "context": context,
            "follow_up_questions": questions,
            "stage": "awaiting_responses",
            "next_action": "collect_detailed_context"
        }
    
    def _extract_niche(self, user_input: str) -> str:
        """Extract niche from user input"""
        niche_keywords = {
            "breathwork": ["breathwork", "breathing", "breath"],
            "fitness": ["fitness", "workout", "training", "gym"],
            "business": ["business", "entrepreneur", "coaching", "consulting"],
            "wellness": ["wellness", "health", "mindfulness", "meditation"],
            "nutrition": ["nutrition", "diet", "food", "nutritionist"]
        }
        
        user_lower = user_input.lower()
        for niche, keywords in niche_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                return niche
        return "general"
    
    def _extract_goals(self, user_input: str) -> str:
        """Extract goals from user input"""
        if any(word in user_input.lower() for word in ["lead", "client", "customer"]):
            return "lead_generation"
        elif any(word in user_input.lower() for word in ["grow", "follower", "audience"]):
            return "audience_growth"
        return "general_growth"
    
    def _extract_audience(self, user_input: str) -> str:
        """Extract target audience"""
        if "entrepreneur" in user_input.lower():
            return "entrepreneurs"
        elif "business" in user_input.lower():
            return "business_owners"
        return "general"
    
    def _generate_contextual_questions(self, context: Dict[str, Any], user_input: str) -> List[Dict[str, str]]:
        """Generate context-aware questions"""
        niche = context.get("niche", "general")
        
        return [
            {"category": "content", "question": f"What type of {niche} content are you currently creating or planning?", "priority": "high"},
            {"category": "competitors", "question": f"Who are 3-5 {niche} coaches you admire on Instagram?", "priority": "high"},
            {"category": "audience", "question": "What's your current follower count and engagement rate?", "priority": "medium"},
            {"category": "goals", "question": "What are your specific growth and revenue targets for the next 3-6 months?", "priority": "high"},
            {"category": "resources", "question": "How much time can you dedicate to Instagram content creation daily?", "priority": "medium"}
        ]
