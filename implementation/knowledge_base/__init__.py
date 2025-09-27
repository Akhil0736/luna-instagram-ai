"""Luna AI Knowledge Base - Complete Research Integration"""

from .hook_database import (
    ALEX_HORMOZI_HOOKS,
    VIRAL_HOOK_TEMPLATES,
    HOOK_TESTING_FRAMEWORK,
    get_hooks_by_category,
    get_random_hook,
    get_hook_categories,
    get_total_hook_count,
    get_viral_hook_template,
    get_random_viral_hooks,
    customize_hook_template,
)
from .instagram_2025_algorithm import (
    INSTAGRAM_2025_ALGORITHM,
    POSTING_OPTIMIZATION,
    get_optimal_posting_time,
    get_algorithm_factor,
)
from .content_strategies import (
    CONTENT_STRATEGY_FRAMEWORK,
    VIRAL_CONTENT_PATTERNS,
    get_content_pillar_mix,
    get_viral_formula,
)
from .hashtag_strategy import (
    HASHTAG_STRATEGY_2025,
    get_hashtag_mix_counts,
    get_optimal_hashtag_count,
    validate_hashtag_strategy,
)
from .cta_framework import (
    CTA_EFFECTIVENESS_FRAMEWORK,
    get_action_verbs,
    get_urgency_phrases,
    get_optimal_cta_placement,
    create_cta,
    get_conversion_stats,
)
from .growth_hacking import (
    GROWTH_HACKING_FRAMEWORK,
    COLLABORATION_STRATEGIES,
    get_growth_techniques,
    get_collaboration_stats,
    get_viral_engineering_steps,
    get_community_building_tactics,
    calculate_optimal_overlap,
)
from .human_behavior import (
    UserType,
    ActivityLevel,
    HumanBehaviorEngine,
    DAILY_USAGE_PATTERNS,
    SOCIAL_MANAGER_SCHEDULE,
    PSYCHOLOGICAL_USAGE_PATTERNS,
    SAFETY_LIMITS,
    ANTI_DETECTION_STRATEGIES,
    get_behavior_pattern,
    is_peak_engagement_time,
    get_natural_break_duration,
)

__all__ = [
    # Hook Database
    "ALEX_HORMOZI_HOOKS",
    "VIRAL_HOOK_TEMPLATES",
    "HOOK_TESTING_FRAMEWORK",
    "get_hooks_by_category",
    "get_random_hook",
    "get_hook_categories",
    "get_total_hook_count",
    "get_viral_hook_template",
    "get_random_viral_hooks",
    "customize_hook_template",

    # Algorithm Intelligence
    "INSTAGRAM_2025_ALGORITHM",
    "POSTING_OPTIMIZATION",
    "get_optimal_posting_time",
    "get_algorithm_factor",

    # Content Strategy
    "CONTENT_STRATEGY_FRAMEWORK",
    "VIRAL_CONTENT_PATTERNS",
    "get_content_pillar_mix",
    "get_viral_formula",

    # Hashtag Strategy
    "HASHTAG_STRATEGY_2025",
    "get_hashtag_mix_counts",
    "get_optimal_hashtag_count",
    "validate_hashtag_strategy",

    # CTA Framework
    "CTA_EFFECTIVENESS_FRAMEWORK",
    "get_action_verbs",
    "get_urgency_phrases",
    "get_optimal_cta_placement",
    "create_cta",
    "get_conversion_stats",

    # Growth Hacking
    "GROWTH_HACKING_FRAMEWORK",
    "COLLABORATION_STRATEGIES",
    "get_growth_techniques",
    "get_collaboration_stats",
    "get_viral_engineering_steps",
    "get_community_building_tactics",
    "calculate_optimal_overlap",

    # Human Behavior Simulation
    "UserType",
    "ActivityLevel",
    "HumanBehaviorEngine",
    "DAILY_USAGE_PATTERNS",
    "SOCIAL_MANAGER_SCHEDULE",
    "PSYCHOLOGICAL_USAGE_PATTERNS",
    "SAFETY_LIMITS",
    "ANTI_DETECTION_STRATEGIES",
    "get_behavior_pattern",
    "is_peak_engagement_time",
    "get_natural_break_duration",
]
