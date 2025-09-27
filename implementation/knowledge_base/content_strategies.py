"""Content Strategy Frameworks - Funnel-Based Architecture & Viral Patterns"""
from __future__ import annotations
from typing import Dict, Any, List

# === FUNNEL-BASED CONTENT STRATEGY ===
CONTENT_STRATEGY_FRAMEWORK: Dict[str, Any] = {
    "funnel_based_architecture": {
        "top_of_funnel_discovery": {
            "reels": {
                "frequency": "2-3 times per week",
                "purpose": "Primary growth driver through Explore tab",
                "reach_boost": 0.67  # 67% higher reach than static posts
            },
            "carousels": {
                "purpose": "High engagement, encourage saves/shares, boost algorithm visibility",
                "engagement_boost": 1.4  # 1.4x more engagement than single images
            }
        },
        "middle_of_funnel_engagement": {
            "photos": "Maintain visual consistency and brand presence",
            "stories": {
                "frequency": "Daily engagement",
                "content": "polls, Q&As, behind-the-scenes content",
                "daily_users": "500M",
                "urgency": "24-hour"
            }
        },
        "bottom_of_funnel_loyalty": {
            "lives": "Real-time Q&A, product launches, trust-building",
            "channels": "VIP updates for super fans, exclusive content"
        }
    },
    "content_format_performance": {
        "reels": {"reach_boost": 0.67, "description": "67% higher reach than static posts"},
        "carousels": {"engagement_boost": 1.4, "description": "1.4x more engagement than single images"},
        "stories": {"daily_users": "500M", "urgency": "24-hour"},
        "igtv": {"completion_rate": 0.95, "optimal_length": "<60s"}
    }
}

# === PROVEN CONTENT PILLAR FRAMEWORK ===
VIRAL_CONTENT_PATTERNS: Dict[str, Any] = {
    "proven_pillar_strategy": {
        "educational": {
            "percentage": 0.30,
            "goal": "Trust Building",
            "content_examples": ["Facts", "How-tos", "Tutorials"],
            "frequency": "30%"
        },
        "social_proof": {
            "percentage": 0.20,
            "goal": "Conversion", 
            "content_examples": ["Testimonials", "UGC", "Reviews"],
            "frequency": "20%"
        },
        "entertainment": {
            "percentage": 0.25,
            "goal": "Engagement",
            "content_examples": ["Memes", "Challenges", "Stories"],
            "frequency": "25%"
        },
        "behind_scenes": {
            "percentage": 0.15,
            "goal": "Connection",
            "content_examples": ["Process", "Team", "Personal"],
            "frequency": "15%"
        },
        "promotional": {
            "percentage": 0.10,
            "goal": "Sales",
            "content_examples": ["Products", "Services", "CTAs"],
            "frequency": "10%"
        }
    },
    "viral_content_analysis": {
        "optimal_character_count": "78% of viral posts use 150-300 characters",
        "hook_patterns": ["Questions", "controversies", "you won't believe formats"],
        "weekly_strategy": "3-2-1: 3 value posts, 2 engagement posts, 1 promotional"
    },
    "viral_content_formula": {
        "hook": "0-3 seconds: Attention-grabbing opening",
        "value_delivery": "3-15 seconds: Clear benefit/entertainment", 
        "engagement_trigger": "15+ seconds: Question/CTA for interaction",
        "shareability_factor": "Memorable/quotable element"
    }
}


def get_content_pillar_mix() -> Dict[str, float]:
    """Get the proven content pillar percentages."""

    return {k: v["percentage"] for k, v in VIRAL_CONTENT_PATTERNS["proven_pillar_strategy"].items()}


def get_viral_formula() -> Dict[str, str]:
    """Get the viral content formula components."""

    return VIRAL_CONTENT_PATTERNS["viral_content_formula"]
