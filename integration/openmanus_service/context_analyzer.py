import re
import logging
import json
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger("luna")

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"

class ContextAnalyzer:
    def __init__(self, openrouter_function=None):
        self.call_openrouter = openrouter_function
        
        # Comprehensive niche categories for SLM classification
        self.niche_categories = [
            "Fitness & Health", "Business & Entrepreneurship", "Technology & Software",
            "Fashion & Beauty", "Food & Cooking", "Travel & Lifestyle", 
            "Education & Learning", "Finance & Investing", "Entertainment & Gaming",
            "Home & Garden", "Parenting & Family", "Art & Creative", 
            "Sports & Recreation", "Personal Development", "Healthcare & Medical"
        ]
    
    async def extract_user_context(self, query: str, user_id: str) -> Dict[str, Any]:
        """Extract comprehensive user context with SLM-based niche classification"""
        
        logger.info(f"📊 Analyzing context for user {user_id} using SLM classification")
        
        # Use SLM for intelligent niche detection
        niche_data = await self._classify_niche_with_slm(query)
        
        context = {
            "niche": niche_data["primary_niche"],
            "secondary_niches": niche_data.get("secondary_niches", []),
            "niche_confidence": niche_data.get("confidence", 0.8),
            "niche_reasoning": niche_data.get("reasoning", ""),
            "experience_level": self._assess_experience(query),
            "goals": self._extract_goals(query),
            "timeline": self._extract_timeline(query),
            "target_audience": self._identify_target_audience(query)
        }
        
        logger.info(f"✅ Context extracted: {context['niche']} (confidence: {context['niche_confidence']:.2f})")
        return context
    
    async def _classify_niche_with_slm(self, query: str) -> Dict[str, Any]:
        """Use Small Language Model for intelligent niche classification"""
        
        if not self.call_openrouter:
            return {"primary_niche": "general", "confidence": 0.5, "reasoning": "No SLM available"}
        
        classification_prompt = f"""
        Analyze this user's description and classify their niche/industry with high accuracy:
        
        USER DESCRIPTION: "{query}"
        
        AVAILABLE CATEGORIES:
        {', '.join(self.niche_categories)}
        
        CLASSIFICATION REQUIREMENTS:
        1. Identify the PRIMARY niche (most relevant category)
        2. Identify up to 2 SECONDARY niches if applicable (hybrid businesses)
        3. Provide confidence score (0.0-1.0)
        4. Explain your reasoning
        5. Handle complex descriptions like "I help SaaS founders stay healthy through biohacking"
        
        RESPONSE FORMAT (JSON):
        {{
            "primary_niche": "exact category name",
            "secondary_niches": ["category1", "category2"],
            "confidence": 0.95,
            "reasoning": "explanation of classification decision",
            "hybrid_business": true/false
        }}
        
        Be accurate and consider:
        - Synonyms and industry terminology
        - Multi-domain businesses
        - Context clues about target audience
        - Specific activities mentioned
        """
        
        try:
            # Use fast, cost-effective model for classification
            response = await self.call_openrouter(
                prompt=classification_prompt,
                task_type="classification"
            )
            
            # Parse JSON response
            classification_data = json.loads(response)
            
            # Clean and validate response
            primary_niche = classification_data.get("primary_niche", "general")
            if primary_niche not in self.niche_categories:
                primary_niche = "general"
            
            return {
                "primary_niche": primary_niche.lower().replace(" & ", "_").replace(" ", "_"),
                "secondary_niches": [
                    niche.lower().replace(" & ", "_").replace(" ", "_") 
                    for niche in classification_data.get("secondary_niches", [])
                ],
                "confidence": min(classification_data.get("confidence", 0.8), 1.0),
                "reasoning": classification_data.get("reasoning", ""),
                "hybrid_business": classification_data.get("hybrid_business", False)
            }
            
        except Exception as e:
            logger.error(f"❌ SLM classification error: {str(e)}")
            return self._fallback_niche_classification(query)
    
    def _fallback_niche_classification(self, query: str) -> Dict[str, Any]:
        """Fallback classification using keywords if SLM fails"""
        
        keyword_mapping = {
            "fitness_&_health": ["gym", "workout", "fitness", "health", "nutrition"],
            "business_&_entrepreneurship": ["business", "entrepreneur", "startup", "marketing"],
            "technology_&_software": ["tech", "software", "coding", "app", "development"],
            "fashion_&_beauty": ["fashion", "style", "beauty", "makeup", "clothing"],
            "food_&_cooking": ["food", "recipe", "cooking", "restaurant", "chef"]
        }
        
        query_lower = query.lower()
        scores = {}
        
        for niche, keywords in keyword_mapping.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                scores[niche] = score
        
        if scores:
            primary_niche = max(scores.items(), key=lambda x: x[1])[0]
            confidence = min(scores[primary_niche] * 0.2, 0.8)
            return {
                "primary_niche": primary_niche,
                "secondary_niches": [],
                "confidence": confidence,
                "reasoning": "Fallback keyword-based classification",
                "hybrid_business": False
            }
        
        return {
            "primary_niche": "general",
            "secondary_niches": [],
            "confidence": 0.3,
            "reasoning": "No clear niche indicators found",
            "hybrid_business": False
        }
    
    def _assess_experience(self, query: str) -> str:
        """Assess user's experience level"""
        beginner_indicators = [
            "new to", "just started", "beginner", "don't know", "help me start",
            "no idea", "never done", "complete novice", "getting started"
        ]
        
        advanced_indicators = [
            "scale", "optimize", "advanced", "expert", "professional",
            "experienced", "been doing", "successful", "established"
        ]
        
        query_lower = query.lower()
        
        beginner_score = sum(1 for indicator in beginner_indicators if indicator in query_lower)
        advanced_score = sum(1 for indicator in advanced_indicators if indicator in query_lower)
        
        if beginner_score > advanced_score:
            return ExperienceLevel.BEGINNER.value
        elif advanced_score > beginner_score:
            return ExperienceLevel.ADVANCED.value
        else:
            return ExperienceLevel.INTERMEDIATE.value
    
    def _extract_goals(self, query: str) -> Dict[str, Any]:
        """Extract user goals and targets"""
        goals = {}
        
        # Follower goals
        follower_match = re.search(r'(?:reach|get|grow to|want)\s+(\d+(?:,\d+)*)[k\s]*(?:followers?|subs?)', query.lower())
        if follower_match:
            target = follower_match.group(1).replace(',', '')
            if 'k' in follower_match.group(0).lower():
                target = int(target) * 1000
            else:
                target = int(target)
            goals['target_followers'] = target
        
        # Revenue goals
        revenue_match = re.search(r'(?:make|earn|generate|want)\s+\$(\d+(?:,\d+)*)[k\s]*(?:/month|monthly|per month|revenue)?', query.lower())
        if revenue_match:
            amount = revenue_match.group(1).replace(',', '')
            if 'k' in revenue_match.group(0).lower():
                amount = int(amount) * 1000
            else:
                amount = int(amount)
            goals['target_revenue'] = amount
        
        # Qualitative goals
        if any(word in query.lower() for word in ['viral', 'famous', 'popular', 'influencer']):
            goals['become_influencer'] = True
        
        if any(word in query.lower() for word in ['quit job', 'full time', 'replace income']):
            goals['financial_independence'] = True
        
        return goals
    
    def _extract_timeline(self, query: str) -> Optional[str]:
        """Extract timeline from query"""
        timeline_patterns = [
            r'in (\d+) (?:months?|weeks?|days?|years?)',
            r'by (\w+ \d{4})',
            r'within (\d+ (?:months?|weeks?|years?))',
            r'over (\d+ (?:months?|weeks?|years?))'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1)
        
        return None
    
    def _identify_target_audience(self, query: str) -> Dict[str, Any]:
        """Identify target audience from query"""
        audience_indicators = {
            "entrepreneurs": ["entrepreneurs", "founders", "business owners", "startups"],
            "fitness_enthusiasts": ["gym-goers", "athletes", "fitness enthusiasts", "bodybuilders"],
            "professionals": ["professionals", "executives", "managers", "corporate"],
            "students": ["students", "learners", "graduates", "university"],
            "parents": ["parents", "moms", "dads", "families"],
            "millennials": ["millennials", "young adults", "25-40"],
            "gen_z": ["gen z", "teens", "young people", "18-25"]
        }
        
        query_lower = query.lower()
        identified_audiences = []
        
        for audience, keywords in audience_indicators.items():
            if any(keyword in query_lower for keyword in keywords):
                identified_audiences.append(audience)
        
        return {
            "primary_audience": identified_audiences[0] if identified_audiences else "general",
            "secondary_audiences": identified_audiences[1:3] if len(identified_audiences) > 1 else []
        }
