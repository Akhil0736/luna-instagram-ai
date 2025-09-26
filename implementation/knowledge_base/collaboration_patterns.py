"""Shared schemas for multi-agent collaboration workflows."""
from typing import Dict, List

COLLABORATION_PATTERNS: Dict[str, List[str]] = {
    "strategy_alignment": ["content_strategist", "engagement_expert", "funnel_architect"],
}
