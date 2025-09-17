import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.llm_clients.openrouter_client import OpenRouterClient

class ExecutionAgent:
    def __init__(self):
        self.openrouter = OpenRouterClient()
    
    async def create_implementation_plan(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed implementation plan with timelines and automation scope"""
        
        # Phase 1: Implementation timeline
        timeline = await self._create_implementation_timeline(strategy, context)
        
        # Phase 2: Content calendar
        content_calendar = await self._generate_content_calendar(strategy, context)
        
        # Phase 3: Automation scope definition
        automation_scope = await self._define_automation_scope(strategy, context)
        
        # Phase 4: Resource requirements
        resource_requirements = await self._calculate_resource_requirements(strategy, context)
        
        return {
            "implementation_timeline": timeline,
            "content_calendar": content_calendar,  
            "automation_scope": automation_scope,
            "resource_requirements": resource_requirements,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def _create_implementation_timeline(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create detailed implementation timeline"""
        
        timeline_prompt = f"""
        Create a detailed 90-day implementation timeline for this Instagram growth strategy:
        
        STRATEGY: {json.dumps(strategy, indent=2)}
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        Create a implementation plan with:
        
        WEEK 1-2: FOUNDATION SETUP
        WEEK 3-6: CONTENT & ENGAGEMENT LAUNCH  
        WEEK 7-10: OPTIMIZATION & SCALING
        WEEK 11-12: ACCELERATION & AUTOMATION
        
        For each phase, specify:
        - Specific tasks and deliverables
        - Time estimates and deadlines
        - Success criteria and checkpoints
        
        Make timeline realistic based on user's available time and resources.
        """
        
        timeline = await self.openrouter.call_openrouter_api(
            timeline_prompt,
            model="moonshotai/kimi-k2-0905",
            task_type="planning"
        )
        
        return timeline
    
    async def _generate_content_calendar(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate detailed content calendar"""
        
        calendar_prompt = f"""
        Generate a detailed 30-day content calendar based on this strategy:
        
        CONTENT STRATEGY: {json.dumps(strategy.get('content_strategy', {}), indent=2)}
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        Create a day-by-day content calendar including:
        
        FOR EACH DAY:
        1. POST TYPE (Reel/Carousel/Single Image)
        2. CONTENT PILLAR theme
        3. SPECIFIC TOPIC/HOOK suggestion  
        4. CAPTION FRAMEWORK to use
        5. HASHTAG CATEGORY 
        6. STORY CONTENT suggestions
        7. ENGAGEMENT TACTICS for that post
        
        Include specific content ideas, hook suggestions, and optimal posting times.
        """
        
        calendar = await self.openrouter.call_openrouter_api(
            calendar_prompt,
            model="deepseek/deepseek-chat-v3.1:free", 
            task_type="planning"
        )
        
        return calendar
    
    async def _define_automation_scope(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Define what Luna AI will automate vs what user handles"""
        
        automation_prompt = f"""
        Define the automation scope for Luna AI based on this strategy and user context:
        
        STRATEGY: {json.dumps(strategy, indent=2)}
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        Define what LUNA AI WILL AUTOMATE:
        
        1. RESEARCH & INTELLIGENCE
        2. CONTENT PLANNING
        3. ENGAGEMENT OPTIMIZATION  
        4. FUNNEL MANAGEMENT
        5. STRATEGY REFINEMENT
        
        Define what USER WILL HANDLE:
        
        1. CONTENT CREATION
        2. AUTHENTIC ENGAGEMENT
        3. PROGRAM DELIVERY
        
        Create clear boundaries and explain the collaborative approach.
        """
        
        automation_scope = await self.openrouter.call_openrouter_api(
            automation_prompt,
            model="moonshotai/kimi-k2-0905",
            task_type="planning"
        )
        
        return automation_scope
    
    async def _calculate_resource_requirements(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Calculate time, budget, and tool requirements"""
        
        resource_prompt = f"""
        Calculate resource requirements for implementing this strategy:
        
        STRATEGY: {json.dumps(strategy, indent=2)}
        USER CONTEXT: {json.dumps(context, indent=2)}
        
        Calculate requirements for:
        
        1. TIME INVESTMENT
        2. BUDGET REQUIREMENTS
        3. SKILL DEVELOPMENT
        4. TECHNICAL SETUP
        5. CONTENT CREATION RESOURCES
        
        Provide realistic estimates and budget ranges. Include free/low-cost alternatives where possible.
        """
        
        resources = await self.openrouter.call_openrouter_api(
            resource_prompt,
            model="deepseek/deepseek-chat-v3.1:free",
            task_type="planning"
        )
        
        return resources
