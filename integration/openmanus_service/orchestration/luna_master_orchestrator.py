import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from agents.conversation.conversation_agent import ConversationAgent
from agents.research.research_agent import ResearchAgent  
from agents.strategy.strategy_agent import StrategyAgent
from agents.execution.execution_agent import ExecutionAgent

logger = logging.getLogger("luna_orchestrator")

class LunaMasterOrchestrator:
    def __init__(self):
        self.conversation_agent = ConversationAgent()
        self.research_agent = ResearchAgent()
        self.strategy_agent = StrategyAgent()
        self.execution_agent = ExecutionAgent()
        self.active_conversations = {}
    
    async def initiate_luna_consultation(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Initiate comprehensive Luna AI consultation process"""
        
        logger.info(f"🌙 Initiating Luna consultation for user {user_id}")
        
        try:
            # Phase 1: Intelligent conversation and context extraction
            conversation_result = await self.conversation_agent.process_initial_input(user_input, user_id)
            
            # Store conversation state
            self.active_conversations[user_id] = {
                "stage": "conversation",
                "conversation_data": conversation_result,
                "started_at": datetime.utcnow().isoformat()
            }
            
            if conversation_result["stage"] == "awaiting_responses":
                return {
                    "status": "conversation_active",
                    "message": f"Perfect! I understand you're in the {conversation_result['context']['niche']} space. To create your comprehensive Instagram growth strategy, I need to dive deeper with a few targeted questions:",
                    "questions": conversation_result["follow_up_questions"],
                    "conversation_id": user_id,
                    "next_action": "answer_questions"
                }
            
        except Exception as e:
            logger.error(f"Error in consultation initiation: {str(e)}")
            return {
                "status": "error",
                "message": "I encountered an issue starting your consultation. Let me try again.",
                "error": str(e)
            }
    
    async def process_user_responses(self, user_id: str, responses: Dict[str, str]) -> Dict[str, Any]:
        """Process user responses and potentially initiate research"""
        
        logger.info(f"🌙 Processing responses from user {user_id}")
        
        try:
            conversation_state = self.active_conversations.get(user_id)
            if not conversation_state:
                return {"status": "error", "message": "Conversation session not found"}
            
            # Process responses through conversation agent
            response_result = await self.conversation_agent.process_follow_up_response(user_id, responses)
            
            if response_result["status"] == "ready_for_research":
                
                # Update conversation state
                conversation_state["stage"] = "research"
                conversation_state["enriched_context"] = response_result["enriched_context"]
                conversation_state["research_scope"] = response_result["research_scope"]
                
                return {
                    "status": "initiating_research",
                    "message": "Excellent! I have everything I need. I'm now conducting comprehensive research using my advanced AI agents. This includes analyzing your competitors, researching current trends, and gathering market intelligence. This will take 2-3 minutes...",
                    "research_scope": response_result["research_scope"],
                    "conversation_id": user_id,
                    "next_action": "wait_for_research"
                }
                
            elif response_result["status"] == "need_more_info":
                return {
                    "status": "additional_questions",
                    "message": "I need just a bit more information to ensure your strategy is perfectly tailored:",
                    "additional_questions": response_result["additional_questions"],
                    "missing_info": response_result["missing_info"],
                    "conversation_id": user_id,
                    "next_action": "answer_additional_questions"
                }
            
        except Exception as e:
            logger.error(f"Error processing responses: {str(e)}")
            return {
                "status": "error", 
                "message": "I encountered an issue processing your responses. Let me try again.",
                "error": str(e)
            }
    
    async def conduct_comprehensive_research(self, user_id: str) -> Dict[str, Any]:
        """Execute comprehensive research phase"""
        
        logger.info(f"🔍 Starting comprehensive research for user {user_id}")
        
        try:
            conversation_state = self.active_conversations.get(user_id)
            if not conversation_state:
                return {"status": "error", "message": "Conversation session not found"}
            
            context = conversation_state["enriched_context"]
            research_scope = conversation_state.get("research_scope", {
                "competitor_analysis": True,
                "content_research": True, 
                "market_analysis": True,
                "funnel_research": True
            })
            
            # Execute comprehensive research
            research_results = await self.research_agent.conduct_comprehensive_research(context, research_scope)
            
            # Update conversation state
            conversation_state["stage"] = "strategy"
            conversation_state["research_results"] = research_results
            
            return {
                "status": "research_complete", 
                "message": "Research complete! I've analyzed your competitors, current trends, and market opportunities. Now my strategy experts are collaborating to create your comprehensive Instagram growth plan...",
                "research_summary": {
                    "competitors_analyzed": len(research_results.get("raw_research_data", [])),
                    "data_points_collected": research_results.get("total_data_points", 0),
                    "research_areas": list(research_scope.keys())
                },
                "conversation_id": user_id,
                "next_action": "wait_for_strategy"
            }
            
        except Exception as e:
            logger.error(f"Error in research phase: {str(e)}")
            return {
                "status": "error",
                "message": "I encountered an issue during research. Let me try with a different approach.",
                "error": str(e)
            }
    
    async def generate_comprehensive_strategy(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive strategy using multi-agent collaboration"""
        
        logger.info(f"🎯 Generating strategy for user {user_id}")
        
        try:
            conversation_state = self.active_conversations.get(user_id)
            if not conversation_state:
                return {"status": "error", "message": "Conversation session not found"}
            
            context = conversation_state["enriched_context"]
            research_results = conversation_state["research_results"]
            
            # Multi-agent strategy synthesis
            strategy_results = await self.strategy_agent.synthesize_comprehensive_strategy(context, research_results)
            
            # Generate implementation plan
            implementation_plan = await self.execution_agent.create_implementation_plan(
                strategy_results["comprehensive_strategy"], 
                context
            )
            
            # Update conversation state
            conversation_state["stage"] = "complete"
            conversation_state["final_strategy"] = strategy_results
            conversation_state["implementation_plan"] = implementation_plan
            conversation_state["completed_at"] = datetime.utcnow().isoformat()
            
            return {
                "status": "strategy_complete",
                "comprehensive_strategy": strategy_results,
                "implementation_plan": implementation_plan,
                "conversation_id": user_id,
                "consultation_summary": {
                    "total_time": self._calculate_consultation_time(conversation_state),
                    "confidence_score": strategy_results.get("strategy_confidence", 0.8),
                    "research_depth": research_results.get("total_data_points", 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in strategy generation: {str(e)}")
            return {
                "status": "error",
                "message": "I encountered an issue generating your strategy. Let me try again.",
                "error": str(e)
            }
    
    async def get_consultation_status(self, user_id: str) -> Dict[str, Any]:
        """Get current consultation status"""
        
        conversation_state = self.active_conversations.get(user_id)
        if not conversation_state:
            return {"status": "not_found", "message": "No active consultation found"}
        
        return {
            "status": "active",
            "current_stage": conversation_state["stage"],
            "started_at": conversation_state["started_at"],
            "conversation_id": user_id
        }
    
    def _calculate_consultation_time(self, conversation_state: Dict[str, Any]) -> str:
        """Calculate total consultation time"""
        start_time = datetime.fromisoformat(conversation_state["started_at"].replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(conversation_state["completed_at"].replace("Z", "+00:00")) 
        
        duration = end_time - start_time
        minutes = int(duration.total_seconds() / 60)
        
        return f"{minutes} minutes"
