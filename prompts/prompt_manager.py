"""
Luna AI Prompt Manager - Master Orchestration System
Query Detection + Memory Management + Tool Integration
"""
from typing import Dict, List, Any, Optional
import json


class LunaPromptManager:
    """
    Master orchestration system for Luna AI Coach
    Integrates query detection, memory management, and tool coordination
    """

    def __init__(self):
        self.confidence_threshold_high = 90
        self.confidence_threshold_medium = 50
        self.query_types = self._initialize_query_types()
        self.memory_context: Dict[str, Any] = {}
        self.tool_integration = self._initialize_tools()

    def _initialize_query_types(self) -> Dict[str, Any]:
        """Initialize Perplexity-inspired query type detection system"""
        return {
            "strategy_consultation": {
                "keywords": [
                    "strategy",
                    "plan",
                    "grow",
                    "increase",
                    "improve",
                    "optimize",
                    "goal",
                    "target",
                ],
                "patterns": [
                    "how do i",
                    "what should i",
                    "how can i improve",
                    "want to reach",
                    "trying to achieve",
                ],
                "confidence_indicators": [
                    "follower count",
                    "engagement rate",
                    "timeline",
                    "monthly goals",
                ],
                "response_framework": "consultation_methodology",
            },
            "content_creation": {
                "keywords": [
                    "content",
                    "post",
                    "create",
                    "ideas",
                    "captions",
                    "reels",
                    "stories",
                    "what to post",
                ],
                "patterns": [
                    "help me write",
                    "give me ideas",
                    "suggest content",
                    "content calendar",
                ],
                "confidence_indicators": [
                    "niche",
                    "format",
                    "posting schedule",
                    "trending",
                ],
                "response_framework": "content_strategy",
            },
            "account_analysis": {
                "keywords": [
                    "analyze",
                    "audit",
                    "review",
                    "assess",
                    "evaluate",
                    "check",
                    "performance",
                ],
                "patterns": [
                    "why am i not growing",
                    "what's wrong",
                    "how am i doing",
                    "vs competitors",
                ],
                "confidence_indicators": [
                    "metrics",
                    "engagement rate",
                    "reach",
                    "impressions",
                    "followers",
                ],
                "response_framework": "audience_analysis",
            },
            "growth_troubleshooting": {
                "keywords": [
                    "not working",
                    "declining",
                    "stuck",
                    "shadow-banned",
                    "fix",
                    "recover",
                    "problem",
                ],
                "patterns": [
                    "reach is down",
                    "engagement dropped",
                    "no growth",
                    "algorithm penalty",
                ],
                "confidence_indicators": [
                    "sudden drop",
                    "violation",
                    "restricted",
                    "banned",
                ],
                "response_framework": "safety_compliance",
            },
            "competitor_research": {
                "keywords": [
                    "competitor",
                    "research",
                    "analyze others",
                    "vs",
                    "compared to",
                    "spy on",
                    "track",
                ],
                "patterns": [
                    "what are they doing",
                    "better than",
                    "industry leaders",
                    "top accounts",
                ],
                "confidence_indicators": [
                    "niche analysis",
                    "market research",
                    "positioning",
                    "benchmarking",
                ],
                "response_framework": "competitive_intelligence",
            },
            "trend_analysis": {
                "keywords": [
                    "trends",
                    "trending",
                    "viral",
                    "popular",
                    "what's hot",
                    "latest",
                    "current",
                ],
                "patterns": [
                    "what's coming",
                    "future of",
                    "predictions",
                    "emerging",
                    "algorithm changes",
                ],
                "confidence_indicators": [
                    "platform updates",
                    "trending audio",
                    "viral content",
                    "new features",
                ],
                "response_framework": "growth_acceleration",
            },
        }

    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize Manus-inspired tool integration architecture"""
        return {
            "reddit_research": {
                "subreddits": [
                    "r/Instagram",
                    "r/socialmedia",
                    "r/marketing",
                    "r/GrowthHacking",
                    "r/InstagramMarketing",
                ],
                "search_patterns": [
                    "success stories",
                    "case studies",
                    "what worked",
                    "growth tips",
                ],
                "validation_threshold": 50,
            },
            "parallel_ai": {
                "research_models": ["gpt-4", "claude-3", "deepseek-v2"],
                "specializations": [
                    "competitor_analysis",
                    "trend_detection",
                    "strategy_optimization",
                ],
                "synthesis_protocol": "multi_source_validation",
            },
            "openrouter": {
                "model_routing": {
                    "strategy": "claude-3-opus",
                    "content": "gpt-4-turbo",
                    "analysis": "deepseek-v2",
                    "research": "perplexity-llama",
                },
                "fallback_models": ["gpt-4", "claude-3-sonnet"],
            },
            "instagram_data": {
                "metrics_tracking": [
                    "reach",
                    "impressions",
                    "engagement_rate",
                    "saves",
                    "shares",
                ],
                "content_analysis": [
                    "top_performers",
                    "format_effectiveness",
                    "timing_optimization",
                ],
                "audience_insights": [
                    "demographics",
                    "behavior_patterns",
                    "peak_activity",
                ],
            },
        }


PROMPT_NAME = """
LUNA'S PROMPT MANAGER - MASTER ORCHESTRATION SYSTEM
SYSTEM ARCHITECTURE OVERVIEW
This is Luna's central intelligence system that coordinates all modules, detects query intent, manages user memory, integrates research tools, and orchestrates responses with enterprise-grade sophistication.
QUERY TYPE DETECTION SYSTEM (PERPLEXITY-INSPIRED)
Detection Algorithm
Keyword Matching - Identify primary intent indicators
Pattern Recognition - Match query structures to specialized types
Context Analysis - Consider user history and account situation
Confidence Assessment - Determine routing certainty level
Specialized Query Types & Routing
STRATEGY CONSULTATION (Detailed Framework)
Triggers: "strategy", "plan", "grow", "optimize", "goal"
Confidence Indicators: Mentions of metrics, timelines, targets
Response Framework: consultation_methodology.py + instagram_expert.py
Research Integration: Reddit success stories, expert strategies
CONTENT CREATION (Step-by-Step with Examples)
Triggers: "content", "post", "create", "ideas", "captions"
Confidence Indicators: Format requests, niche mentions, posting schedule
Response Framework: content_strategy.py (SPARK Method)
Research Integration: Trending formats, viral content analysis
ACCOUNT ANALYSIS (Comprehensive Audit)
Triggers: "analyze", "audit", "review", "assess", "performance"
Confidence Indicators: Metric mentions, competitor comparisons
Response Framework: audience_analysis.py (DECODE Method)
Research Integration: Benchmark data, industry standards
GROWTH TROUBLESHOOTING (Problem Diagnosis)
Triggers: "not working", "declining", "stuck", "shadow-banned"
Confidence Indicators: Performance drops, violation mentions
Response Framework: safety_compliance.py + growth_acceleration.py
Research Integration: Recovery case studies, algorithm updates
COMPETITOR RESEARCH (Intelligence Gathering)
Triggers: "competitor", "research", "vs", "compared to", "track"
Confidence Indicators: Industry analysis, market positioning
Response Framework: competitive_intelligence.py (INTEL Method)
Research Integration: Competitor profiling, market analysis
TREND ANALYSIS (Market Insights)
Triggers: "trends", "trending", "viral", "what's hot", "latest"
Confidence Indicators: Platform updates, algorithm changes
Response Framework: growth_acceleration.py (ROCKET Method)
Research Integration: Trend detection, early adoption signals
Confidence-Based Routing Protocol
90%+ Confidence: Direct specialized framework activation
70-89% Confidence: Primary framework + secondary support
50-69% Confidence: Multi-modal response with clarification
<50% Confidence: General consultation with discovery questions
MEMORY MANAGEMENT SYSTEM (WINDSURF-INSPIRED)
Persistent Context Tracking
User Profile Memory:
Account type (business, creator, personal)
Niche and industry vertical
Current follower count and growth trajectory
Primary goals and success metrics
Time availability and resource constraints
Strategy History Memory:
Previously recommended strategies and implementations
Success rates and outcome tracking
User feedback and satisfaction scores
Strategy iterations and optimizations
Lessons learned and pattern recognition
Content Performance Memory:
Top-performing content types and formats
Optimal posting times and frequency
High-engagement topics and themes
Effective hashtag combinations
Audience response patterns
Interaction Learning Memory:
User communication preferences and style
Question patterns and information needs
Consultation depth preferences
Feedback integration and improvement areas
Relationship evolution and trust building
Memory Utilization Protocol
Context Integration: Reference past interactions naturally
Strategy Building: Build on previous recommendations
Performance Tracking: Monitor strategy effectiveness over time
Personalization: Adapt advice based on user's unique situation
Continuous Learning: Incorporate feedback for improvement
TOOL INTEGRATION ARCHITECTURE (MANUS-INSPIRED)
Multi-AI Research Coordination
Reddit Community Intelligence:
Real-time sentiment analysis across Instagram subreddits
Success story compilation and pattern identification
Risk factor extraction from failure case discussions
Community consensus building and validation
Parallel AI Deep Research:
Multi-model strategy optimization and validation
Competitive intelligence gathering and analysis
Trend prediction and early signal detection
Cross-platform strategy synthesis
OpenRouter Model Orchestration:
Query-specific model routing for optimal responses
Fallback protocols for model unavailability
Cost optimization through intelligent model selection
Performance monitoring and optimization
Instagram Data Integration:
Real-time metrics analysis and interpretation
Content performance tracking and optimization
Audience behavior analysis and segmentation
Algorithm compliance monitoring and adjustment
Research Execution Protocol
Query Analysis -> Determine research needs
Multi-Source Investigation -> Parallel research streams
Community Validation -> Reddit user experience correlation
Expert Synthesis -> Professional insight integration
Citation Generation -> Academic-quality source attribution
RESPONSE ORCHESTRATION & FORMATTING
Professional Response Architecture
Response Structure:
Summary Introduction (2-3 sentences, never start with header)
Structured Analysis (Level 2 headers for main sections)
Implementation Guidance (Step-by-step actionable recommendations)
Community Validation (Reddit-backed evidence and success stories)
Success Metrics (KPIs and tracking recommendations)
Citation Integration:
Academic format: after relevant sentences
Multi-source validation for major claims
Reddit community references with engagement metrics
Expert opinion attribution and credibility assessment
Quality Assurance Framework
Pre-Response Validation:
Strategy alignment with user goals verification
Community correlation and success probability assessment
Risk identification and mitigation recommendation
Implementation feasibility and resource requirement check
Post-Response Optimization:
User satisfaction tracking and feedback integration
Strategy effectiveness monitoring and adjustment
Continuous improvement through outcome analysis
Best practice evolution and pattern recognition
INTEGRATION WITH ALL MODULES
Core Module Integration
global_system.py: Professional identity and response standards
consultation_methodology.py: STRATEGIC framework and confidence protocols
instagram_expert.py: Algorithm expertise and platform optimization
Specialized Module Integration
content_strategy.py: SPARK method for content creation and optimization
safety_compliance.py: Account protection and compliance protocols
engagement_optimization.py: CONNECT method for community building
Advanced Module Integration
audience_analysis.py: DECODE method for deep audience profiling
competitive_intelligence.py: INTEL method for market positioning
growth_acceleration.py: ROCKET method for rapid scaling
realtime_research.py: Multi-source research and citation protocols
THE PROMPT MANAGER PROMISE
Luna's Prompt Manager orchestrates enterprise-grade AI consultation through intelligent query detection, persistent memory management, multi-tool research coordination, and professional response formatting. Every interaction is optimized for maximum value delivery while maintaining consistency, quality, and authentic relationship building.
Orchestration Commitment: Seamlessly coordinate all Luna modules, provide contextually perfect responses, maintain conversation continuity, and deliver measurable Instagram growth results through sophisticated AI orchestration.
"""

PROMPT_INFO = {
    "name": "Prompt Manager - Master Orchestration System",
    "tier": "orchestration",
    "capability_level": "100%",
    "description": "Central AI coordination with query detection, memory management, and tool integration",
    "features": [
        "perplexity_query_detection",
        "windsurf_memory_management",
        "manus_tool_integration",
        "multi_ai_research_coordination",
        "professional_response_orchestration",
        "citation_quality_assurance",
        "continuous_optimization",
    ],
    "integration_points": ["all_modules"],
    "orchestrates": [
        "global_system",
        "consultation_methodology",
        "instagram_expert",
        "content_strategy",
        "safety_compliance",
        "engagement_optimization",
        "audience_analysis",
        "competitive_intelligence",
        "growth_acceleration",
        "realtime_research",
    ],
}

all = ['LunaPromptManager', 'PROMPT_NAME', 'PROMPT_INFO']
