"""CTA Effectiveness Framework - Conversion Optimization Research"""
from __future__ import annotations
from typing import Dict, Any, List

# === HIGH-CONVERTING CTA RESEARCH ===
CTA_EFFECTIVENESS_FRAMEWORK: Dict[str, Any] = {
    "essential_cta_components": {
        "clarity": "Clear, immediate understanding of action",
        "action_verbs": ["Discover", "Get", "Join", "Unlock", "Grab", "Start", "Learn"],
        "urgency": ["Limited time", "Today only", "Don't miss out"],
        "personalization": ["For you", "Your perfect", "direct addressing"]
    },
    "cta_placement_strategy": {
        "posts": "End of caption (highest conversion)",
        "stories": "Interactive stickers + swipe-up",
        "reels": "Text overlay + voice CTA",
        "carousels": "Final slide with strong CTA"
    },
    "ab_testing_framework": {
        "language_testing": ["Shop now", "Buy today", "Get yours"],
        "urgency_levels": ["High", "medium", "low pressure"],
        "visual_integration": ["Button", "text", "overlay"],
        "color_psychology": ["High contrast", "brand colors"]
    },
    "conversion_improvements": {
        "button_ctas": "30% higher click-through than text-only",
        "urgent_language": "25% increase in immediate actions",
        "personalized_ctas": "43% higher engagement rates"
    }
}

def get_action_verbs() -> List[str]:
    """Get list of high-converting action verbs."""

    return CTA_EFFECTIVENESS_FRAMEWORK["essential_cta_components"]["action_verbs"]


def get_urgency_phrases() -> List[str]:
    """Get list of urgency phrases for CTAs."""

    return CTA_EFFECTIVENESS_FRAMEWORK["essential_cta_components"]["urgency"]


def get_optimal_cta_placement(content_type: str) -> str:
    """Get optimal CTA placement for content type."""

    return CTA_EFFECTIVENESS_FRAMEWORK["cta_placement_strategy"].get(content_type, "End of caption")


def create_cta(action_verb: str, urgency: str = "", personalization: str = "") -> str:
    """Create optimized CTA using framework components."""

    cta_parts: List[str] = []

    if personalization:
        cta_parts.append(personalization)

    cta_parts.append(action_verb)

    if urgency:
        cta_parts.append(f"({urgency})")

    return " ".join(cta_parts)


def get_conversion_stats() -> Dict[str, str]:
    """Get CTA conversion improvement statistics."""

    return CTA_EFFECTIVENESS_FRAMEWORK["conversion_improvements"]
