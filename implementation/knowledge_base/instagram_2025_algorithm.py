"""Instagram 2025 Algorithm Intelligence - Complete Research Implementation"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple

# === INSTAGRAM 2025 ALGORITHM CORE SIGNALS ===
INSTAGRAM_2025_ALGORITHM: Dict[str, Any] = {
    "ranking_types": {
        "connected_reach": "Content shown to followers",
        "unconnected_reach": "Content shown via recommendations to non-followers",
    },
    "multi_algorithm_system": {
        "feed_algorithm": "Relationship + Interest + Timeliness + Frequency",
        "reels_algorithm": "Entertainment value + completion rate + shares",
        "stories_algorithm": "Recency + interaction history + frequency",
        "explore_algorithm": "Interest signals + past behavior patterns"
    },
    "critical_timing_windows": {
        "golden_window_minutes": 20,
        "first_15_minutes": "Algorithm favors posts with immediate engagement",
        "initial_spike_importance": "Determines broader distribution",
        "real_time_response": "Crucial for visibility"
    },
    "critical_first_hour_strategy": {
        "within_1_hour": "7x more likely to qualify engagement",
        "within_24_hours": "60x more likely vs 48+ hour delay", 
        "immediate_response": "Significantly higher conversion rates"
    }
}

# === OPTIMAL POSTING TIMES RESEARCH ===
POSTING_OPTIMIZATION: Dict[str, Any] = {
    "optimal_posting_times": {
        "b2b": {
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
            "times": ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
        },
        "b2c": {
            "days": ["Tuesday", "Wednesday", "Thursday"], 
            "times": ["11:00", "12:00", "13:00", "14:00", "19:00", "20:00", "21:00"]
        },
        "weekend": {
            "description": "Lower activity but less competition",
            "times": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
        },
        "stories_peaks": ["08:00", "09:00", "10:00", "19:00", "20:00", "21:00"]
    },
    "viral_posting_windows": {
        "not_9am": "Common belief debunked",
        "actual_optimal": "11am-2pm and 7-9pm",
        "golden_rule": "15-20 minute immediate engagement window"
    }
}


def get_optimal_posting_time(audience_type: str, day_type: str = "weekday") -> List[str]:
    """Get optimal posting times for specific audience type."""

    if day_type == "weekend":
        return POSTING_OPTIMIZATION["optimal_posting_times"]["weekend"]["times"]

    return POSTING_OPTIMIZATION["optimal_posting_times"].get(audience_type, [])


def get_algorithm_factor(factor: str) -> Dict[str, Any]:
    """Get specific algorithm factor details."""

    return INSTAGRAM_2025_ALGORITHM.get(factor, {})
