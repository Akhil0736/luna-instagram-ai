"""Knowledge base of proven attention hooks and 2025 Instagram algorithm insights."""
from typing import Dict, List, Any

# Instagram 2025 Algorithm Intelligence (Adam Mosseri)
INSTAGRAM_2025_ALGORITHM = {
    "ranking_types": {
        "connected_reach": "Content shown to followers",
        "unconnected_reach": "Content shown via recommendations to non-followers"
    },
    "top_3_ranking_factors": {
        "watch_time": {
            "priority": 1,
            "description": "How long people watch videos - #1 signal",
            "optimization": "Hook viewers early, maintain engagement"
        },
        "likes_per_reach": {
            "priority": 2,
            "description": "Percentage of viewers who like posts",
            "connected_importance": "Higher for follower reach",
            "unconnected_importance": "Lower for discovery"
        },
        "sends_per_reach": {
            "priority": 3,
            "description": "How often people share content",
            "connected_importance": "Lower for follower reach", 
            "unconnected_importance": "Higher for discovery - KEY for growth"
        }
    },
    "recommendation_rules": {
        "no_watermarks": "Avoid TikTok, CapCut watermarks",
        "use_audio": "Add music/voice even to photos",
        "video_length": "Keep under 3 minutes", 
        "original_content": "Transform, don't just repost",
        "account_status": "Maintain good standing"
    }
}

# Alex Hormozi's 121 Proven Hooks
ALEX_HORMOZI_HOOKS = {
    "labels": [
        "Local business owners, I have a gift for you",
        "If you're working all the time and your business isn't growing...",
        "Small business owners, listen up",
        "Entrepreneurs, this is for you", 
        "Content creators, pay attention",
        "Instagram users making this mistake",
        "Anyone trying to grow online",
        "People who want real results",
        "Fitness enthusiasts, stop doing this",
        "Business owners, this will change everything"
    ],
    "questions": [
        "Would you pay $1,000 to have the business of your dreams in 30 days?",
        "Which would you rather be?",
        "What if I told you there was a way to...",
        "Have you ever wondered why some accounts grow faster?",
        "Do you want to know the secret everyone's hiding?",
        "What would happen if you could automate your growth?",
        "Why do 99% of people fail at Instagram?",
        "What's the difference between those who succeed and those who don't?"
    ],
    "commands": [
        "Read this if you're tired of being broke",
        "Watch this if you want to get ahead of 99% of people",
        "Stop doing this immediately",
        "Start doing this today",
        "Save this post for later",
        "Share this with someone who needs it",
        "Try this hack right now",
        "Comment below if you agree"
    ],
    "statements": [
        "The smartest thing you can do today...",
        "How to get ahead of 99% of people",
        "This will change everything",
        "Nobody talks about this",
        "The algorithm doesn't want you to know",
        "I wish I knew this when I started",
        "This is what successful people do differently",
        "The secret to viral content"
    ],
    "narratives": [
        "One day I was scrolling and this changed everything...",
        "I'll never forget what happened next...",
        "This story will blow your mind...", 
        "My biggest mistake was...",
        "The moment everything clicked was when...",
        "Let me tell you about the time I...",
        "Here's what nobody tells you about..."
    ]
}

# Viral Content Patterns from Research
VIRAL_CONTENT_PATTERNS = {
    "content_pillars": {
        "educational": 0.30,    # Trust building, tutorials
        "entertainment": 0.25,  # Memes, challenges  
        "social_proof": 0.20,   # Testimonials, UGC
        "behind_scenes": 0.15,  # Process, personal
        "promotional": 0.10     # Products, CTAs
    },
    "optimal_times": {
        "b2b": ["10:00", "11:00", "13:00", "14:00", "15:00"],
        "b2c": ["11:00", "12:00", "13:00", "14:00", "19:00", "20:00", "21:00"],
        "stories": ["08:00", "09:00", "19:00", "20:00", "21:00"],
        "golden_window": 20  # Critical first 20 minutes
    },
    "hashtag_strategy": {
        "total_count": 12,
        "broad_popular": {"count": 2, "reach": "1M+"},
        "mid_tier": {"count": 4, "reach": "100K-1M"},
        "niche_specific": {"count": 5, "reach": "10K-100K"}, 
        "brand_custom": {"count": 1, "reach": "<10K"}
    }
}

# Hook Testing Framework (70-20-10 Rule)
HOOK_TESTING_FRAMEWORK = {
    "proven": 0.70,      # Use successful hooks from past
    "adjacent": 0.20,    # Adapt from similar niches  
    "experimental": 0.10 # Test completely new approaches
}

def get_hooks_by_category(category: str) -> List[str]:
    """Retrieve hooks by specific category."""
    return ALEX_HORMOZI_HOOKS.get(category, [])

def get_algorithm_factor(factor: str) -> Dict[str, Any]:
    """Get specific 2025 algorithm ranking factor details."""
    return INSTAGRAM_2025_ALGORITHM["top_3_ranking_factors"].get(factor, {})
