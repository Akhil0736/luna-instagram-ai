from __future__ import annotations

from typing import List, Iterable


class QueryOptimizer:
    """
    Research Query Optimizer
    - Expands base intents into multiple platform-specific queries
    - Adds synonyms/semantic variants to widen coverage
    - Keeps total under a practical ceiling to allow parallel requests
    """

    def __init__(self, max_queries: int = 25) -> None:
        self.max_queries = max_queries

    def expand(self, base_queries: List[str], niche: str) -> List[str]:
        seeds = list(base_queries)
        # Platform-specific variants
        platforms = [
            "reddit", "youtube", "quora", "medium", "blog", "case study",
            "instagram forum", "growth hacking", "2024", "2025",
        ]
        platform_variants = [f"{q} {p}" for q in seeds for p in platforms]

        # Semantic variants / synonyms focusing on IG growth
        synonyms = [
            "increase followers", "boost engagement", "reach growth",
            "content strategy", "hashtag strategy", "posting times",
            "real examples", "success stories", "step-by-step",
        ]
        synonym_variants = [f"{niche} {s}" for s in synonyms]

        # Combine and deduplicate while preserving order
        combined: List[str] = []
        seen = set()
        for q in seeds + platform_variants + synonym_variants:
            if q not in seen:
                combined.append(q)
                seen.add(q)
            if len(combined) >= self.max_queries:
                break
        return combined
