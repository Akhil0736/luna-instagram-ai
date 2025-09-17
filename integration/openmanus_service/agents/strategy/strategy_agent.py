import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.llm_clients.openrouter_client import OpenRouterClient

class StrategyAgent:
    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.specialist_agents = {
            "content_strategist": self._content_specialist,
            "engagement_expert": self._engagement_specialist,
            "funnel_architect": self._funnel_specialist,
            "growth_hacker": self._growth_specialist
        }
    
    async def synthesize_comprehensive_strategy(self, context: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-agent strategy synthesis with specialist collaboration"""
        
        # Phase 1: Individual specialist analysis
        specialist_strategies = await asyncio.gather(
            self.specialist_agents["content_strategist"](context, research_data),
            self.specialist_agents["engagement_expert"](context, research_data), 
            self.specialist_agents["funnel_architect"](context, research_data),
            self.specialist_agents["growth_hacker"](context, research_data)
        )
        
        # Phase 2: Multi-agent debate and refinement
        refined_strategies = await self._conduct_agent_debate(context, specialist_strategies)
        
        # Phase 3: Final strategy synthesis and validation
        final_strategy = await self._synthesize_final_strategy(context, research_data, refined_strategies)
        
        # Phase 4: Risk assessment and mitigation
        risk_assessment = await self._assess_strategy_risks(final_strategy, context)
        
        return {
            "comprehensive_strategy": final_strategy,
            "risk_assessment": risk_assessment,
            "specialist_insights": specialist_strategies,
            "strategy_confidence": self._calculate_confidence_score(final_strategy, research_data),
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def _content_specialist(self, context: Dict[str, Any], research: Dict[str, Any]) -> str:
        """Content strategy specialist"""
        
        specialist_prompt = f"""
        As a Content Strategy Expert, analyze this situation and create a comprehensive content strategy:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        RESEARCH INSIGHTS: {json.dumps(research.get('research_synthesis', {}), indent=2)}
        
        Create a detailed content strategy covering:
        
        1. CONTENT PILLARS (4-6 pillars with specific themes)
        2. CONTENT MIX & FREQUENCY
        3. VIRAL HOOKS & TEMPLATES
        4. CONTENT CALENDAR STRUCTURE
        5. VISUAL BRAND GUIDELINES
        6. CONTENT CREATION WORKFLOW
        
        Base recommendations on research insights about successful competitors and trending formats.
        Provide specific, actionable guidance tailored to their niche and goals.
        """
        
        return await self.openrouter.call_openrouter_api(
            specialist_prompt,
            model="moonshotai/kimi-k2-0905", 
            task_type="strategy"
        )
    
    async def _engagement_specialist(self, context: Dict[str, Any], research: Dict[str, Any]) -> str:
        """Engagement and community specialist"""
        
        engagement_prompt = f"""
        As an Instagram Engagement Expert, design comprehensive engagement strategies:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        RESEARCH DATA: {json.dumps(research.get('raw_research_data', []), indent=1)}
        
        Design engagement tactics covering:
        
        1. HASHTAG STRATEGY
        2. CAPTION FRAMEWORKS
        3. COMMUNITY BUILDING
        4. STORY ENGAGEMENT
        5. ALGORITHM OPTIMIZATION
        
        Base all recommendations on competitor analysis and successful patterns in their niche.
        """
        
        return await self.openrouter.call_openrouter_api(
            engagement_prompt,
            model="deepseek/deepseek-chat-v3.1:free",
            task_type="strategy"
        )
    
    async def _funnel_specialist(self, context: Dict[str, Any], research: Dict[str, Any]) -> str:
        """Lead generation and funnel specialist"""
        
        funnel_prompt = f"""
        As a Funnel Architecture Expert, design a complete lead generation system:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        RESEARCH DATA: {json.dumps(research.get('research_synthesis', {}), indent=2)}
        
        Design a comprehensive funnel covering:
        
        1. LEAD MAGNET STRATEGY
        2. LANDING PAGE OPTIMIZATION
        3. EMAIL SEQUENCE DESIGN
        4. INSTAGRAM-TO-EMAIL FUNNEL
        5. CONVERSION OPTIMIZATION
        6. METRICS AND TRACKING
        
        Base on successful funnel strategies identified in research.
        """
        
        return await self.openrouter.call_openrouter_api(
            funnel_prompt,
            model="moonshotai/kimi-k2-0905",
            task_type="strategy"
        )
    
    async def _growth_specialist(self, context: Dict[str, Any], research: Dict[str, Any]) -> str:
        """Growth hacking and scaling specialist"""  
        
        growth_prompt = f"""
        As a Growth Hacking Expert, design accelerated growth strategies:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        RESEARCH DATA: {json.dumps(research.get('research_synthesis', {}), indent=2)}
        
        Create growth acceleration strategies covering:
        
        1. VIRAL GROWTH TACTICS
        2. COLLABORATION STRATEGIES
        3. COMPETITIVE ADVANTAGE
        4. AUTOMATION AND SCALING
        
        Focus on scalable, sustainable growth that aligns with their resources and goals.
        """
        
        return await self.openrouter.call_openrouter_api(
            growth_prompt,
            model="deepseek/deepseek-chat-v3.1:free",
            task_type="strategy"
        )
    
    async def _conduct_agent_debate(self, context: Dict[str, Any], specialist_strategies: List[str]) -> str:
        """Simulate multi-agent debate to refine and optimize strategies"""
        
        debate_prompt = f"""
        Conduct a multi-expert debate to refine these Instagram growth strategies:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        SPECIALIST STRATEGIES:
        CONTENT EXPERT: {specialist_strategies[0]}
        ENGAGEMENT EXPERT: {specialist_strategies[1]}  
        FUNNEL EXPERT: {specialist_strategies[2]}
        GROWTH EXPERT: {specialist_strategies[3]}
        
        Simulate a collaborative debate where experts:
        1. Identify overlaps and synergies between strategies
        2. Resolve conflicts and contradictions
        3. Prioritize recommendations based on user's resources and goals
        4. Refine tactics for maximum effectiveness
        5. Create integrated approaches that leverage multiple specialties
        
        Output the refined, consensus strategy that incorporates the best insights from all experts
        while remaining realistic and actionable for the user's situation.
        """
        
        refined_strategy = await self.openrouter.call_openrouter_api(
            debate_prompt,
            model="moonshotai/kimi-k2-0905",
            task_type="synthesis"
        )
        
        return refined_strategy
    
    async def _synthesize_final_strategy(self, context: Dict[str, Any], research: Dict[str, Any], refined_strategies: str) -> Dict[str, Any]:
        """Create the final, comprehensive strategy document"""
        
        synthesis_prompt = f"""
        Create the final, comprehensive Instagram growth strategy:
        
        USER CONTEXT: {json.dumps(context, indent=2)}
        RESEARCH INSIGHTS: {json.dumps(research.get('research_synthesis', {}), indent=2)}
        REFINED EXPERT STRATEGIES: {refined_strategies}
        
        Synthesize into a master strategy document with:
        
        1. EXECUTIVE SUMMARY
        2. CONTENT STRATEGY
        3. ENGAGEMENT TACTICS
        4. LEAD GENERATION SYSTEM
        5. GROWTH ACCELERATION
        6. IMPLEMENTATION ROADMAP
        7. SUCCESS METRICS
        
        Ensure all recommendations are specific, actionable, and tailored to the user's niche, goals, and resources.
        """
        
        try:
            final_strategy = await self.openrouter.call_openrouter_api(
                synthesis_prompt,
                model="moonshotai/kimi-k2-0905", 
                task_type="synthesis"
            )
            
            return json.loads(final_strategy)
            
        except json.JSONDecodeError:
            # Return structured fallback if JSON parsing fails
            return {
                "strategy_text": final_strategy,
                "parsing_error": True,
                "requires_manual_structuring": True
            }
    
    async def _assess_strategy_risks(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Assess potential risks and challenges with the strategy"""
        
        risk_prompt = f"""
        Assess potential risks and challenges with this Instagram growth strategy:
        
        STRATEGY: {json.dumps(strategy, indent=2)}
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        Identify and analyze:
        
        1. EXECUTION RISKS
        2. MARKET RISKS  
        3. BRAND RISKS
        4. FINANCIAL RISKS
        5. MITIGATION STRATEGIES
        
        Provide specific, actionable risk mitigation recommendations.
        """
        
        risk_assessment = await self.openrouter.call_openrouter_api(
            risk_prompt,
            model="deepseek/deepseek-chat-v3.1:free",
            task_type="analysis"
        )
        
        return risk_assessment
    
    def _calculate_confidence_score(self, strategy: Dict[str, Any], research: Dict[str, Any]) -> float:
        """Calculate confidence score for the strategy"""
        
        # Factors affecting confidence
        factors = {
            "research_depth": min(research.get('total_data_points', 0) / 10000, 1.0),
            "strategy_completeness": 1.0 if isinstance(strategy, dict) and len(strategy) > 5 else 0.5,
            "niche_specificity": 0.9 if research.get('research_synthesis', {}).get('market_intelligence') else 0.6,
            "competitor_data": 0.8 if research.get('raw_research_data') else 0.4
        }
        
        # Weighted average
        weights = [0.3, 0.3, 0.2, 0.2]
        confidence = sum(score * weight for score, weight in zip(factors.values(), weights))
        
        return round(confidence, 2)
