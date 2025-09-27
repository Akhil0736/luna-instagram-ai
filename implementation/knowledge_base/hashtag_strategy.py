"""Hashtag Strategy 2025 - Algorithm Evolution & Optimization Framework"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple

# === 2024-2025 HASHTAG ALGORITHM CHANGES ===
HASHTAG_STRATEGY_2025: Dict[str, Any] = {
    "algorithm_evolution": {
        "computer_vision": "Instagram now uses advanced computer vision to understand content",
        "context_role": "Hashtags provide additional context, not primary categorization",
        "quality_over_quantity": "Fewer, more targeted hashtags perform better"
    },
    "proven_hashtag_framework": {
        "optimal_count": "10-15 hashtags",
        "mix_strategy": {
            "broad_popular": {
                "count_range": [1, 2],
                "reach": "1M+ posts",
                "purpose": "Maximum exposure"
            },
            "mid_tier": {
                "count_range": [3, 5],
                "reach": "100K-1M posts",
                "purpose": "Balanced competition"
            },
            "niche_specific": {
                "count_range": [4, 6],
                "reach": "10K-100K posts",
                "purpose": "Targeted audience"
            },
            "brand_custom": {
                "count_range": [1, 2],
                "reach": "<10K posts",
                "purpose": "Community building"
            }
        }
    },
    "performance_metrics": {
        "hashtag_reach_percentage": "Percentage of reach from hashtags",
        "save_rate_by_hashtag": "Which tags drive content saves",
        "follower_growth_rate": "Hashtag-driven new followers",
        "engagement_quality": "Comments vs. likes ratio per hashtag"
    }
}

def get_hashtag_mix_counts() -> Dict[str, Tuple[int, int]]:
    """Get recommended hashtag counts by category."""

    mix_strategy = HASHTAG_STRATEGY_2025["proven_hashtag_framework"]["mix_strategy"]
    return {
        category: tuple(data["count_range"])
        for category, data in mix_strategy.items()
    }


def get_optimal_hashtag_count() -> str:
    """Get optimal hashtag count recommendation."""

    return HASHTAG_STRATEGY_2025["proven_hashtag_framework"]["optimal_count"]


def validate_hashtag_strategy(hashtags: Dict[str, List[str]]) -> Dict[str, Any]:
    """Validate hashtag mix against proven framework."""

    mix_strategy = HASHTAG_STRATEGY_2025["proven_hashtag_framework"]["mix_strategy"]
    results = {"valid": True, "recommendations": []}

    total_count = sum(len(tags) for tags in hashtags.values())

    if total_count > 15:
        results["valid"] = False
        results["recommendations"].append("Reduce total hashtags to 10-15 maximum")

    for category, expected_range in get_hashtag_mix_counts().items():
        actual_count = len(hashtags.get(category, []))
        if actual_count < expected_range[0] or actual_count > expected_range[1]:
            results["recommendations"].append(
                f"{category}: Use {expected_range[0]}-{expected_range[1]} hashtags, currently using {actual_count}"
            )

    return results
