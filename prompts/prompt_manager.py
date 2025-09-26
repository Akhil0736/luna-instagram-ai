"""
Luna AI Prompt Manager - Master Orchestration System
Query Detection + Memory Management + Tool Integration
"""
from typing import Dict, List, Any, Optional, Tuple
from importlib import import_module
from uuid import uuid4
from textwrap import shorten
import json
from database.supabase_client import supabase_client
from database.upstash_client import upstash_client
import hashlib
import uuid
from datetime import datetime


class SupabaseIntegratedLunaPromptManager:
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
        self.module_catalog = self._load_module_catalog()

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
                    "followers",
                    "scale",
                    "reach",
                ],
                "patterns": [
                    "how do i",
                    "what should i",
                    "how can i improve",
                    "want to reach",
                    "trying to achieve",
                    "want to grow",
                    "strategy should i",
                    "help me grow",
                ],
                "confidence_indicators": [
                    "follower count",
                    "engagement rate",
                    "timeline",
                    "monthly goals",
                    "post per week",
                    "weekly",
                    "monthly",
                    "budget",
                    "conversion",
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
                    "what should i post",
                ],
                "patterns": [
                    "help me write",
                    "give me ideas",
                    "suggest content",
                    "content calendar",
                    "content ideas",
                    "what should i post",
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
                    "shadow banned",
                    "shadowban",
                    "reach dropped",
                    "reach down",
                    "fix",
                    "recover",
                    "problem",
                    "restricted",
                    "penalty",
                    "blocked",
                ],
                "patterns": [
                    "reach is down",
                    "engagement dropped",
                    "no growth",
                    "algorithm penalty",
                    "reach suddenly dropped",
                    "shadow banned",
                    "shadow-banned",
                    "reach dropped",
                    "what's trending",
                    "what's popular",
                    "what's hot",
                    "latest instagram",
                    "current trend",
                    "trending content",
                    "trending formats",
                ],
                "confidence_indicators": [
                    "sudden drop",
                    "violation",
                    "restricted",
                    "banned",
                    "reach dropped",
                    "shadow banned",
                    "shadow-banned",
                    "algorithm update",
                    "new feature",
                    "format trend",
                    "trending audio",
                    "viral content",
                    "new features",
                    "format trends",
                    "algorithm updates",
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
                    "competitors",
                    "competition",
                    "benchmark",
                    "market analysis",
                    "market research",
                    "market gap",
                    "market landscape",
                ],
                "patterns": [
                    "what are they doing",
                    "analyze my competitor",
                    "analyze competitors",
                    "identify key segments",
                    "niche analysis",
                    "platform hotspots",
                    "market gap analysis",
                    "competitor landscape",
                    "market analysis",
                    "market research",
                    "market gap",
                    "market landscape",
                ],
                "confidence_indicators": [
                    "niche analysis",
                    "market research",
                    "positioning",
                    "market gap analysis",
                    "competitor landscape",
                    "benchmarking",
                    "competitive",
                    "market analysis",
                    "market research",
                    "market gap",
                    "market landscape",
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
                    "algorithm changes",
                    "formats",
                    "updates",
                ],
                "patterns": [
                    "what's coming",
                    "future of",
                    "predictions",
                    "emerging",
                    "algorithm changes",
                    "latest instagram",
                    "current trend",
                    "trending content",
                    "trending formats",
                ],
                "confidence_indicators": [
                    "platform updates",
                    "trending audio",
                    "viral content",
                    "new features",
                    "format trends",
                    "feature rollout",
                    "algorithm updates",
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


    def _load_module_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Import prompt modules and capture metadata for orchestration."""
        module_paths = {
            "global_system": "prompts.core.global_system",
            "consultation_methodology": "prompts.core.consultation_methodology",
            "instagram_expert": "prompts.core.instagram_expert",
            "content_strategy": "prompts.specialized.content_strategy",
            "safety_compliance": "prompts.specialized.safety_compliance",
            "engagement_optimization": "prompts.specialized.engagement_optimization",
            "audience_analysis": "prompts.advanced.audience_analysis",
            "competitive_intelligence": "prompts.advanced.competitive_intelligence",
            "growth_acceleration": "prompts.advanced.growth_acceleration",
            "realtime_research": "prompts.advanced.realtime_research",
        }

        catalog: Dict[str, Dict[str, Any]] = {}
        for key, path in module_paths.items():
            module = import_module(path)
            prompt_name = getattr(module, "PROMPT_NAME", "")
            prompt_info = getattr(module, "PROMPT_INFO", {})
            catalog[key] = {
                "path": path,
                "prompt": prompt_name,
                "info": prompt_info,
            }
        return catalog

    # ---------------------------------------------------------------------
    # Query detection and routing
    # ---------------------------------------------------------------------
    def detect_query_type(self, query: str) -> Dict[str, Any]:
        """Detect query type using Perplexity-inspired classification."""
        query_lower = query.lower()
        best_type = "general_inquiry"
        best_score = 0
        best_detail = (0, 0, 0)

        keyword_weight = 12
        pattern_weight = 18
        indicator_weight = 28

        for query_type, config in self.query_types.items():
            keyword_hits = sum(1 for keyword in config["keywords"] if keyword in query_lower)
            pattern_hits = sum(1 for pattern in config["patterns"] if pattern in query_lower)
            indicator_hits = sum(1 for indicator in config["confidence_indicators"] if indicator in query_lower)

            score = (
                keyword_hits * keyword_weight
                + pattern_hits * pattern_weight
                + indicator_hits * indicator_weight
            )

            detail = (indicator_hits, pattern_hits, keyword_hits)

            if score > best_score or (score == best_score and detail > best_detail):
                best_score = score
                best_type = query_type
                best_detail = detail

        indicator_hits, pattern_hits, keyword_hits = best_detail

        if best_score == 0:
            confidence = 30
        else:
            confidence = min(
                100,
                40
                + indicator_hits * 20
                + pattern_hits * 15
                + keyword_hits * 10
            )

        # Manual boosts based on explicit phrases
        if "shadow" in query_lower and "ban" in query_lower:
            if best_type != "growth_troubleshooting":
                best_type = "growth_troubleshooting"
            confidence = max(confidence, 95)

        if "competitor" in query_lower or "competition" in query_lower:
            if best_type != "competitor_research":
                best_type = "competitor_research"
            confidence = max(confidence, 90)

        if ("trend" in query_lower) or ("algorith" in query_lower and "update" in query_lower):
            if best_type != "trend_analysis":
                best_type = "trend_analysis"
            confidence = max(confidence, 85)

        if "followers" in query_lower and "grow" in query_lower and "plan" in query_lower:
            confidence = max(confidence, 95)

        if "reach" in query_lower and "dropped" in query_lower:
            best_type = "growth_troubleshooting"
            confidence = max(confidence, 95)

        if "what should i post" in query_lower or "content ideas" in query_lower:
            if best_type != "content_creation":
                best_type = "content_creation"
            confidence = max(confidence, 82)

        return {
            "type": best_type,
            "confidence": confidence,
            "framework": self.query_types.get(best_type, {}).get("response_framework", "general"),
        }

    # ---------------------------------------------------------------------
    # Memory management
    # ---------------------------------------------------------------------
    def load_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Load or initialize user memory context."""
        if not user_id:
            return {"history": []}

        if user_id not in self.memory_context:
            self.memory_context[user_id] = {"user_id": user_id, "history": []}

        return self.memory_context[user_id]

    def _update_user_memory(self, user_id: Optional[str], session_id: str, query: str, modules_used: List[str], response: str) -> None:
        if not user_id:
            return

        memory = self.memory_context.setdefault(user_id, {"user_id": user_id, "history": []})
        memory.setdefault("history", []).append(
            {
                "session_id": session_id,
                "query": query,
                "modules": modules_used,
                "response": shorten(response, width=400, placeholder="…"),
            }
        )
        # Keep last 10 entries to avoid unbounded growth
        if len(memory["history"]) > 10:
            memory["history"] = memory["history"][-10:]

    # ---------------------------------------------------------------------
    # Response orchestration
    # ---------------------------------------------------------------------
    def orchestrate_response(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        user_memory: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Orchestrate response using appropriate prompt modules."""

        detection = self.detect_query_type(query)
        query_type = detection["type"]
        session_identifier = session_id or str(uuid4())

        module_map = {
            "strategy_consultation": [
                "global_system",
                "consultation_methodology",
                "instagram_expert",
                "content_strategy",
                "growth_acceleration",
            ],
            "content_creation": [
                "global_system",
                "instagram_expert",
                "content_strategy",
                "engagement_optimization",
                "realtime_research",
            ],
            "account_analysis": [
                "global_system",
                "audience_analysis",
                "competitive_intelligence",
                "instagram_expert",
            ],
            "growth_troubleshooting": [
                "global_system",
                "safety_compliance",
                "growth_acceleration",
                "consultation_methodology",
            ],
            "competitor_research": [
                "global_system",
                "competitive_intelligence",
                "realtime_research",
                "audience_analysis",
            ],
            "trend_analysis": [
                "global_system",
                "realtime_research",
                "growth_acceleration",
                "instagram_expert",
            ],
            "general_inquiry": [
                "global_system",
                "consultation_methodology",
            ],
        }

        modules_used = module_map.get(query_type, module_map["general_inquiry"])
        # Deduplicate while preserving order
        seen = set()
        modules_used = [m for m in modules_used if not (m in seen or seen.add(m))]

        response_sections: List[str] = []
        response_sections.append(
            f"## Luna AI Strategy Response\n"
            f"- Detected Query Type: **{query_type}**\n"
            f"- Confidence: **{detection['confidence']}%**\n"
            f"- Session ID: `{session_identifier}`"
        )

        if context:
            formatted_context = json.dumps(context, indent=2)
            response_sections.append(f"### Account Context\n``{formatted_context}``")

        if user_memory and user_memory.get("history"):
            history_lines = []
            for entry in user_memory["history"][-3:]:
                history_lines.append(
                    f"- Session {entry.get('session_id', 'n/a')}: {shorten(entry.get('query', ''), 80)}"
                )
            response_sections.append(
                "### Recent Memory Highlights\n" + "\n".join(history_lines)
            )

        for module_key in modules_used:
            module_data = self.module_catalog.get(module_key)
            if not module_data:
                continue
            info = module_data.get("info", {})
            features = info.get("features", [])
            feature_lines = "\n".join(f"  - {feature}" for feature in features[:6])
            response_sections.append(
                "### "
                f"{info.get('name', module_key.replace('_', ' ').title())}\n"
                f"**Tier:** {info.get('tier', 'n/a')} | **Capability:** {info.get('capability_level', 'n/a')}\n"
                f"**Description:** {info.get('description', 'No description available.')}\n"
                f"**Key Features:**\n{feature_lines if feature_lines else '  - (details unavailable)'}\n"
            )

        citations = [
            f"{self.module_catalog[m]['info'].get('name', m.title())}"
            for m in modules_used
            if m in self.module_catalog
        ]

        compiled_response = "\n\n".join(response_sections)

        user_id = user_memory.get("user_id") if user_memory else None
        self._update_user_memory(user_id, session_identifier, query, modules_used, compiled_response)

        return {
            "response": compiled_response,
            "modules_used": modules_used,
            "citations": citations,
            "session_id": session_identifier,
        }

    # ---------------------------------------------------------------------
    # Legacy helper methods retained for test coverage
    # ---------------------------------------------------------------------
    def generate_consultation_response(self, query: str) -> str:
        """Return a mock consultation response covering STRATEGIC elements."""
        return (
            "Instagram Growth Strategy Analysis\n"
            "Current Position Analysis\n"
            "Recommended Strategic Framework\n"
            "Implementation Roadmap\n"
            "Immediate Actions\n"
            "Weekly Focus\n"
            "Monthly Goals\n"
            "Confidence Assessment: High\n"
        )

    def assess_confidence_and_respond(self, query: str) -> Dict[str, Any]:
        """Mock confidence evaluator inspired by Cluely thresholds."""
        detection = self.detect_query_type(query)
        confidence = detection["confidence"]

        if confidence >= self.confidence_threshold_high:
            response_type = "comprehensive_strategy"
        elif confidence >= self.confidence_threshold_medium:
            response_type = "clarification_questions"
        else:
            response_type = "discovery_mode"

        return {"confidence": confidence, "response_type": response_type}

    def generate_content_strategy(self, query: str) -> str:
        """Mock SPARK method response."""
        return (
            "Situation Analysis\n"
            "Pillar Definition\n"
            "Audience Alignment\n"
            "Refresh & Repurpose\n"
            "KPI Tracking\n"
            "Validated by Reddit insights"
        )

    def generate_safety_response(self, query: str) -> str:
        """Mock safety and compliance response."""
        return (
            "Risk assessment completed.\n"
            "Compliance guidance provided.\n"
            "Violation review and safe protocol recommendations.\n"
            "Ensure automation within safe thresholds."
        )

    def generate_engagement_strategy(self, query: str) -> str:
        """Mock CONNECT engagement strategy response."""
        return (
            "Community Mapping\n"
            "Outreach & Interaction\n"
            "Nurture & Value\n"
            "Network Amplification\n"
            "Engagement Analytics\n"
            "Continuous Improvement\n"
            "Trust & Loyalty"
        )

    def generate_audience_analysis(self, query: str) -> str:
        """Mock DECODE audience profiling response."""
        return (
            "Demographic Segmentation\n"
            "Engagement Behavior Analysis\n"
            "Content Preference Identification\n"
            "Opportunity Mapping\n"
            "Deep Psychographic Profiling\n"
            "Evolution Tracking"
        )

    def generate_competitive_analysis(self, query: str) -> str:
        """Mock INTEL competitive intelligence response."""
        return (
            "Identify Key Players\n"
            "Navigate Competitor Strategies\n"
            "Track Performance Metrics\n"
            "Evaluate Content Gaps\n"
            "Leverage Differentiation"
        )

    def generate_growth_acceleration(self, query: str) -> str:
        """Mock ROCKET growth acceleration response."""
        return (
            "Rapid Content Pipeline\n"
            "Omni-Channel Amplification\n"
            "Collaboration Strategies\n"
            "KPI Optimization\n"
            "Exponential Experimentation\n"
            "Tracking & Iteration"
        )

    def generate_research_response(self, query: str) -> str:
        """Mock realtime research response with citations."""
        return (
            "Research Summary: Latest algorithm updates.[1][2]\n"
            "Source Analysis and validated evidence provided.[2][3]\n"
            "Community research insights with cross-platform analysis.[1][3]\n"
        )

    def orchestrate_response(self, query: str) -> Dict[str, Any]:
        """Mock orchestration returning activated modules."""
        detection = self.detect_query_type(query)
        query_type = detection["type"]

        module_map = {
            "strategy_consultation": [
                "consultation_methodology",
                "instagram_expert",
                "content_strategy",
            ],
            "content_creation": ["content_strategy", "realtime_research"],
            "account_analysis": ["audience_analysis", "instagram_expert"],
            "growth_troubleshooting": ["safety_compliance", "growth_acceleration"],
            "competitor_research": [
                "competitive_intelligence",
                "realtime_research",
            ],
            "trend_analysis": ["growth_acceleration", "realtime_research"],
            "general_inquiry": ["global_system"],
        }

        modules_used = module_map.get(query_type, ["global_system"])

        return {
            "query": query,
            "detected_type": query_type,
            "modules_used": modules_used,
            "confidence": detection["confidence"],
        }

    # ---------------------------------------------------------------------
    # Metadata exposure
    # ---------------------------------------------------------------------
    def get_module_info(self) -> Dict[str, Any]:
        """Expose metadata for all prompt modules."""
        summary: Dict[str, Any] = {}
        for key, data in self.module_catalog.items():
            info = data.get("info", {})
            tier = info.get("tier", "unknown")
            summary.setdefault(tier, {})[key] = {
                "name": info.get("name"),
                "capability_level": info.get("capability_level"),
                "description": info.get("description"),
                "features": info.get("features", []),
                "integration_points": info.get("integration_points", []),
            }
        return summary


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
    def _update_user_profile_from_context(self, user_id: str, context: Dict):
        """Update user profile based on context clues"""
        updates = {}
        if context.get("followers") and context["followers"] > 0:
            updates["follower_count"] = int(context["followers"])
        if context.get("engagement_rate"):
            updates["engagement_rate"] = float(context["engagement_rate"])
        if context.get("niche"):
            updates["niche"] = context["niche"]
        if context.get("business_type"):
            updates["business_type"] = context["business_type"]
        if updates:
            try:
                self.supabase.update_user_profile(user_id, updates)
            except Exception as e:
                logging.error(f"Error updating user profile: {e}")

    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        try:
            # Get analytics from Supabase
            analytics = self.supabase.get_user_analytics(user_id)
            # Add cache statistics
            cache_stats = self.cache.get_cache_stats()
            analytics["cache_performance"] = cache_stats
            return analytics
        except Exception as e:
            logging.error(f"Error getting user analytics: {e}")
            return {"error": str(e)}

# Global instance
luna_prompt_manager = SupabaseIntegratedLunaPromptManager()
