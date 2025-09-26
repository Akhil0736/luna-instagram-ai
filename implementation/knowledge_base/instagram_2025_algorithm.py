"""Instagram 2025 algorithm insights and supporting research for Luna implementation agents."""

from typing import Any, Dict, List

INSTAGRAM_2025_ALGORITHM: Dict[str, Any] = {
    "ranking_types": {
        "connected_reach": "Content shown to followers",
        "unconnected_reach": "Content shown via recommendations to non-followers",
    },
    "top_3_ranking_factors": {
        "watch_time": {
            "priority": 1,
            "description": "How long people watch videos - #1 signal for both reach types",
            "optimization": "Hook viewers early, maintain engagement throughout",
        },
        "likes_per_reach": {
            "priority": 2,
            "description": "Percentage of viewers who like your post",
            "connected_importance": "Higher for follower reach",
            "unconnected_importance": "Lower for discovery reach",
        },
        "sends_per_reach": {
            "priority": 3,
            "description": "How often people send content to others",
            "connected_importance": "Lower for follower reach",
            "unconnected_importance": "Higher for discovery reach - KEY for growth",
        },
    },
    "recommendation_rules": {
        "no_watermarks": {
            "rule": "Avoid TikTok, CapCut, or other platform watermarks",
            "reason": "Instagram deprioritizes recycled-looking content",
        },
        "use_audio": {
            "rule": "Add music/voiceover even to photos and carousels",
            "reason": "Boosts engagement ranking significantly",
        },
        "video_length": {
            "rule": "Keep videos under 3 minutes",
            "reason": "Instagram prioritizes short-form content (upgraded from 90 seconds)",
        },
        "original_content": {
            "rule": "Post original content or significantly transform reposts",
            "reason": "Simple reposts won't get recommended",
        },
        "account_status": {
            "rule": "Maintain good account standing",
            "check": "Profile → Settings → Account Status must show good standing",
        },
    },
    "trials_feature": {
        "description": "Test content with non-followers without spamming followers",
        "benefit": "Bypasses connected ranking, goes straight to recommendations",
        "use_case": "Perfect for testing viral potential",
    },
}

ALEX_HORMOZI_HOOKS: Dict[str, Dict[str, List[str]]] = {
    "labels": [
        "Local business owners, I have a gift for you",
        "If you're working all the time and your business isn't growing...",
        "Small business owners, listen up",
        "Entrepreneurs, this is for you",
        "Content creators, pay attention",
        "Instagram users, I need to tell you something",
        # Add all 121 proven hooks categorized
    ],
    "questions": [
        "Would you pay $1,000 to have the business of your dreams in 30 days?",
        "Which would you rather be?",
        "What if I told you there was a way to...",
        "Have you ever wondered why some accounts grow faster?",
        # Add all question hooks from research
    ],
    "commands": [
        "Read this if you're tired of being broke",
        "Watch this if you want to get ahead of 99% of people",
        "Stop doing this immediately",
        "Start doing this today",
        # Add all command hooks from research
    ],
    # Continue with all categories from research
}

VIRAL_CONTENT_PATTERNS: Dict[str, Any] = {
    "content_pillars": {
        "educational": 0.30,
        "entertainment": 0.25,
        "social_proof": 0.20,
        "behind_scenes": 0.15,
        "promotional": 0.10,
    },
    "posting_schedule": {
        "optimal_times_b2b": ["10:00", "11:00", "13:00", "14:00", "15:00"],
        "optimal_times_b2c": ["11:00", "12:00", "13:00", "14:00", "19:00", "20:00", "21:00"],
        "story_peaks": ["08:00", "09:00", "10:00", "19:00", "20:00", "21:00"],
        "golden_window_minutes": 20,
    },
}

ALGORITHM_KNOWLEDGE_BASE: Dict[str, Any] = {
    "sources": [
        "Adam Mosseri (Head of Instagram) 2025 algorithm update",
        "Internal Luna research, Q1-Q3 2025",
    ],
    "insights": {
        "algorithm": INSTAGRAM_2025_ALGORITHM,
        "hook_library": ALEX_HORMOZI_HOOKS,
        "viral_patterns": VIRAL_CONTENT_PATTERNS,
    },
    "usage_notes": [
        "Use watch-time optimization guidance to prioritize creative testing",
        "Blend hook libraries with niche-specific relevance for authenticity",
        "Maintain healthy account status metrics before pushing viral experiments",
    ],
}

__all__ = [
    "INSTAGRAM_2025_ALGORITHM",
    "ALEX_HORMOZI_HOOKS",
    "VIRAL_CONTENT_PATTERNS",
    "ALGORITHM_KNOWLEDGE_BASE",
]


def get_instagram_algorithm_insights() -> Dict[str, Any]:
    """Return a consolidated view of Instagram 2025 research insights."""

    return ALGORITHM_KNOWLEDGE_BASE
