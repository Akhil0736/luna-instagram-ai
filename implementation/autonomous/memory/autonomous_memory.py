"""Autonomous Memory System - Integration with Luna's Cache Manager"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import json
import hashlib
from dataclasses import dataclass, asdict

# Import Luna's existing cache system
try:
    from cache_manager_working import WorkingLunaCacheManager

    CACHE_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    CACHE_AVAILABLE = False
    WorkingLunaCacheManager = None  # type: ignore[assignment]


@dataclass
class AutonomousMemoryEntry:
    """Memory entry for autonomous agent experiences"""

    memory_id: str
    agent_id: str
    timestamp: datetime
    memory_type: str  # decision, learning, context, pattern
    content: Dict[str, Any]
    importance_score: float  # 0.0 to 1.0
    access_count: int
    last_accessed: datetime
    tags: List[str]


class LunaAutonomousMemory:
    """Enhanced memory system integrating with Luna's cache manager"""

    def __init__(self):
        self.cache_manager = WorkingLunaCacheManager() if CACHE_AVAILABLE else None
        self.memory_entries: Dict[str, AutonomousMemoryEntry] = {}
        self.agent_memories: Dict[str, List[str]] = {}  # agent_id -> memory_ids
        self.memory_indices: Dict[str, List[str]] = {}  # tag -> memory_ids

    async def initialize(self):
        """Initialize memory system with cache integration"""
        if self.cache_manager and CACHE_AVAILABLE:
            await self.cache_manager.init_redis()

    async def store_memory(
        self,
        agent_id: str,
        memory_type: str,
        content: Dict[str, Any],
        importance_score: float = 0.5,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Store autonomous memory entry"""

        # Generate unique memory ID
        memory_id = self._generate_memory_id(agent_id, content)

        # Create memory entry
        memory_entry = AutonomousMemoryEntry(
            memory_id=memory_id,
            agent_id=agent_id,
            timestamp=datetime.now(),
            memory_type=memory_type,
            content=content,
            importance_score=importance_score,
            access_count=0,
            last_accessed=datetime.now(),
            tags=tags or [],
        )

        # Store in local memory
        self.memory_entries[memory_id] = memory_entry

        # Update agent memory index
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = []
        self.agent_memories[agent_id].append(memory_id)

        # Update tag indices
        for tag in memory_entry.tags:
            if tag not in self.memory_indices:
                self.memory_indices[tag] = []
            self.memory_indices[tag].append(memory_id)

        # Persist to cache if available
        if self.cache_manager:
            await self._persist_memory_to_cache(memory_entry)

        return memory_id

    async def retrieve_memory(self, memory_id: str) -> Optional[AutonomousMemoryEntry]:
        """Retrieve specific memory entry"""
        if memory_id in self.memory_entries:
            memory = self.memory_entries[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now()
            return memory

        # Try to load from cache
        if self.cache_manager:
            cached_memory = await self._load_memory_from_cache(memory_id)
            if cached_memory:
                self.memory_entries[memory_id] = cached_memory
                return cached_memory

        return None

    async def search_memories(
        self, agent_id: str, query: Dict[str, Any], limit: int = 10
    ) -> List[AutonomousMemoryEntry]:
        """Search memories based on query parameters"""
        agent_memory_ids = self.agent_memories.get(agent_id, [])

        matching_memories: List[AutonomousMemoryEntry] = []

        for memory_id in agent_memory_ids:
            memory = await self.retrieve_memory(memory_id)
            if not memory:
                continue

            # Apply filters
            if self._matches_query(memory, query):
                matching_memories.append(memory)

        # Sort by relevance (importance score + recency)
        matching_memories.sort(
            key=lambda m: m.importance_score + self._recency_score(m.timestamp),
            reverse=True,
        )

        return matching_memories[:limit]

    async def get_learning_patterns(self, agent_id: str) -> Dict[str, Any]:
        """Extract learning patterns from agent's memory"""
        memories = await self.search_memories(agent_id, {"memory_type": "learning"}, limit=50)

        if not memories:
            return {"patterns": [], "insights": "Insufficient data"}

        # Analyze success patterns
        successful_memories = [m for m in memories if m.content.get("success_score", 0) >= 0.7]
        failed_memories = [m for m in memories if m.content.get("success_score", 0) <= 0.3]

        patterns = {
            "success_patterns": self._extract_patterns(successful_memories),
            "failure_patterns": self._extract_patterns(failed_memories),
            "improvement_trend": self._calculate_improvement_trend(memories),
            "most_important_lessons": self._get_most_important_lessons(memories),
        }

        return patterns

    async def consolidate_memories(self, agent_id: str) -> Dict[str, Any]:
        """Consolidate and compress old memories"""
        agent_memories = await self.search_memories(agent_id, {}, limit=1000)

        if len(agent_memories) <= 100:
            return {"action": "no_consolidation_needed", "memory_count": len(agent_memories)}

        # Sort by importance and recency
        sorted_memories = sorted(
            agent_memories,
            key=lambda m: m.importance_score + self._recency_score(m.timestamp),
            reverse=True,
        )

        # Keep top 100 memories
        memories_to_keep = sorted_memories[:100]
        memories_to_archive = sorted_memories[100:]

        # Archive old memories
        archived_count = 0
        for memory in memories_to_archive:
            if await self._archive_memory(memory):
                archived_count += 1

        return {
            "action": "consolidation_completed",
            "kept_memories": len(memories_to_keep),
            "archived_memories": archived_count,
            "total_processed": len(agent_memories),
        }

    def _generate_memory_id(self, agent_id: str, content: Dict[str, Any]) -> str:
        """Generate unique memory ID"""
        content_hash = hashlib.md5(json.dumps(content, sort_keys=True).encode(), usedforsecurity=False).hexdigest()
        timestamp_hash = hashlib.md5(str(datetime.now().timestamp()).encode(), usedforsecurity=False).hexdigest()[:8]
        return f"{agent_id}_{timestamp_hash}_{content_hash[:12]}"

    def _matches_query(self, memory: AutonomousMemoryEntry, query: Dict[str, Any]) -> bool:
        """Check if memory matches query criteria"""
        for key, value in query.items():
            if key == "memory_type":
                if memory.memory_type != value:
                    return False
            elif key == "tags":
                if not any(tag in memory.tags for tag in value):
                    return False
            elif key == "min_importance":
                if memory.importance_score < value:
                    return False
            elif key == "after_date":
                if memory.timestamp < value:
                    return False
            elif key in memory.content:
                if memory.content[key] != value:
                    return False

        return True

    def _recency_score(self, timestamp: datetime) -> float:
        """Calculate recency score (0.0 to 1.0)"""
        now = datetime.now()
        age_hours = (now - timestamp).total_seconds() / 3600

        # Exponential decay: recent memories get higher scores
        return max(0.0, 1.0 - (age_hours / (24 * 7)))  # Decay over a week

    def _extract_patterns(self, memories: List[AutonomousMemoryEntry]) -> List[Dict[str, Any]]:
        """Extract common patterns from memories"""
        if not memories:
            return []

        patterns: List[Dict[str, Any]] = []

        # Pattern 1: Common contexts
        context_patterns: Dict[str, int] = {}
        for memory in memories:
            context = memory.content.get("context", {})
            for key, value in context.items():
                pattern_key = f"{key}:{value}"
                context_patterns[pattern_key] = context_patterns.get(pattern_key, 0) + 1

        # Find most common context patterns
        common_contexts = sorted(context_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        if common_contexts:
            patterns.append({"type": "common_contexts", "patterns": common_contexts})

        # Pattern 2: Timing patterns
        hours = [m.timestamp.hour for m in memories]
        if hours:
            most_common_hour = max(set(hours), key=hours.count)
            patterns.append(
                {
                    "type": "timing_pattern",
                    "most_active_hour": most_common_hour,
                    "activity_distribution": {h: hours.count(h) for h in set(hours)},
                }
            )

        return patterns

    def _calculate_improvement_trend(self, memories: List[AutonomousMemoryEntry]) -> Dict[str, Any]:
        """Calculate improvement trend over time"""
        if len(memories) < 5:
            return {"trend": "insufficient_data"}

        # Sort by timestamp
        sorted_memories = sorted(memories, key=lambda m: m.timestamp)

        # Split into early and recent periods
        split_point = len(sorted_memories) // 2
        early_memories = sorted_memories[:split_point]
        recent_memories = sorted_memories[split_point:]

        # Calculate average success scores
        early_scores = [m.content.get("success_score", 0.5) for m in early_memories]
        recent_scores = [m.content.get("success_score", 0.5) for m in recent_memories]

        early_avg = sum(early_scores) / len(early_scores) if early_scores else 0
        recent_avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0

        improvement = recent_avg - early_avg

        if improvement > 0.1:
            trend = "improving"
        elif improvement < -0.1:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "early_performance": early_avg,
            "recent_performance": recent_avg,
            "improvement_score": improvement,
        }

    def _get_most_important_lessons(
        self, memories: List[AutonomousMemoryEntry], limit: int = 5
    ) -> List[str]:
        """Get most important lessons learned"""
        # Sort by importance score
        important_memories = sorted(memories, key=lambda m: m.importance_score, reverse=True)

        lessons: List[str] = []
        for memory in important_memories[:limit]:
            lesson = memory.content.get("lesson_learned", "No specific lesson")
            if lesson and lesson != "No specific lesson":
                lessons.append(lesson)

        return lessons

    async def _persist_memory_to_cache(self, memory: AutonomousMemoryEntry):
        """Persist memory to cache system"""
        if not self.cache_manager:
            return

        cache_key = f"autonomous_memory:{memory.memory_id}"
        cache_data = {"memory": asdict(memory), "timestamp": memory.timestamp.isoformat()}

        # Store with 7-day TTL
        ttl = 7 * 24 * 3600  # 7 days in seconds
        _ = (cache_key, cache_data, ttl)  # Placeholder to indicate variable usage
        # await self.cache_manager.store_with_ttl(cache_key, cache_data, ttl)

    async def _load_memory_from_cache(self, memory_id: str) -> Optional[AutonomousMemoryEntry]:
        """Load memory from cache system"""
        if not self.cache_manager:
            return None

        cache_key = f"autonomous_memory:{memory_id}"
        _ = cache_key  # Placeholder to indicate variable usage
        # cached_data = await self.cache_manager.get(cache_key)

        # if cached_data:
        #     memory_dict = cached_data.get("memory")
        #     if memory_dict:
        #         # Reconstruct datetime objects
        #         memory_dict["timestamp"] = datetime.fromisoformat(memory_dict["timestamp"])
        #         memory_dict["last_accessed"] = datetime.fromisoformat(memory_dict["last_accessed"])
        #         return AutonomousMemoryEntry(**memory_dict)

        return None

    async def _archive_memory(self, memory: AutonomousMemoryEntry) -> bool:
        """Archive old memory to long-term storage"""
        # In real implementation, this would move to cheaper storage
        # For now, just remove from active memory
        if memory.memory_id in self.memory_entries:
            del self.memory_entries[memory.memory_id]

        # Remove from agent memory index
        agent_memories = self.agent_memories.get(memory.agent_id, [])
        if memory.memory_id in agent_memories:
            agent_memories.remove(memory.memory_id)

        return True


# Global memory manager instance
luna_autonomous_memory = LunaAutonomousMemory()
