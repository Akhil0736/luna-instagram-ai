"""Growth Hacking Framework - Proven Viral Tactics & Strategies"""
from __future__ import annotations
from typing import Dict, Any, List

# === PROVEN GROWTH HACKING STRATEGIES ===
GROWTH_HACKING_FRAMEWORK: Dict[str, Any] = {
    "core_techniques": {
        "strategic_timing": {
            "post_when_competitors_silent": "Avoid competition",
            "real_time_trend_jacking": "Leverage breaking news moments",
            "competitor_silence_windows": "Find gaps in competitor posting"
        },
        "collaboration_networks": {
            "micro_influencer_range": "1K-100K followers",
            "cross_brand_collaborations": "Complementary audiences",
            "ugc_campaigns": "User-generated content with incentives"
        },
        "hashtag_farming": {
            "target_competitor_hashtags": "During peak hours",
            "engage_trending_content": "First to engage with trending hashtags",
            "branded_hashtag_creation": "With clear incentives"
        },
        "comment_strategy": {
            "first_60_seconds": "3-5 strategic comments",
            "value_adding_responses": "Not generic praise",
            "tag_relevant_accounts": "Expand reach"
        },
        "story_engagement_loops": {
            "interactive_stickers": "Drive profile visits",
            "link_in_bio_funneling": "Traffic direction",
            "cross_platform_sharing": "Story distribution"
        }
    },
    "viral_content_engineering": {
        "hook_timing": "0-3 seconds: Attention-grabbing opening",
        "value_delivery": "3-15 seconds: Clear benefit/entertainment",
        "engagement_trigger": "15+ seconds: Question/CTA for interaction",
        "shareability_factor": "Memorable/quotable element"
    },
    "community_building_tactics": {
        "response_time": "Within 15 minutes to all comments",
        "caption_questions": "Ask questions in every post caption",
        "exclusive_content": "For top engagers",
        "live_sessions": "Weekly for community building"
    }
}

# === COLLABORATION EFFECTIVENESS RESEARCH ===
COLLABORATION_STRATEGIES: Dict[str, Any] = {
    "collaboration_effectiveness": {
        "expanded_reach": "Appear in both audiences' feeds",
        "higher_engagement": "Trusted recommendation effect",
        "follower_growth": "Credibility through association",
        "increased_sales": "Combined conversion power"
    },
    "optimal_collaboration_types": {
        "brand_influencer": "73% higher engagement than solo posts",
        "brand_brand": "45% reach increase for complementary audiences",
        "influencer_influencer": "89% engagement boost in shared niches"
    },
    "high_performing_formats": {
        "behind_scenes": "67% higher engagement",
        "product_tutorials": "54% better conversion rates",
        "ugc_features": "79% more authentic feel",
        "joint_giveaways": "156% participation increase"
    },
    "partnership_selection_criteria": {
        "audience_overlap_analysis": {
            "20_40_overlap": "Optimal for growth",
            "40_60_overlap": "Best for engagement",
            "60_plus_overlap": "Risk of audience fatigue"
        },
        "engagement_quality_metrics": {
            "comments_likes_ratio": "Higher = better audience quality",
            "save_rate": "Indicates valuable content creation",
            "share_rate": "Shows content worth distributing"
        }
    }
}


def get_growth_techniques() -> List[str]:
    """Get list of core growth hacking techniques."""

    return list(GROWTH_HACKING_FRAMEWORK["core_techniques"].keys())


def get_collaboration_stats() -> Dict[str, str]:
    """Get collaboration effectiveness statistics."""

    return COLLABORATION_STRATEGIES["optimal_collaboration_types"]


def get_viral_engineering_steps() -> Dict[str, str]:
    """Get viral content engineering formula."""

    return GROWTH_HACKING_FRAMEWORK["viral_content_engineering"]


def get_community_building_tactics() -> Dict[str, str]:
    """Get community building tactics."""

    return GROWTH_HACKING_FRAMEWORK["community_building_tactics"]


def calculate_optimal_overlap(audience_size_1: int, audience_size_2: int, overlap: int) -> str:
    """Calculate if audience overlap is optimal for collaboration."""

    if min(audience_size_1, audience_size_2) == 0:
        return "insufficient_overlap"

    overlap_percentage = (overlap / min(audience_size_1, audience_size_2)) * 100

    if 20 <= overlap_percentage <= 40:
        return "optimal_for_growth"
    if 40 < overlap_percentage <= 60:
        return "best_for_engagement"
    if overlap_percentage > 60:
        return "risk_of_fatigue"
    return "insufficient_overlap"
