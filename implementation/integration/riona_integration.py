"""Bridges Luna's strategies to human-like, safest Instagram automation via Riona."""

from __future__ import annotations

import asyncio
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

from implementation.knowledge_base.instagram_2025_algorithm import INSTAGRAM_2025_ALGORITHM


class RionaHumanBehaviorEngine:
    """Simulates authentic Instagram user behavior and ensures compliance with 2025 algorithm."""

    def __init__(self) -> None:
        # 1. Natural usage patterns (peak times + intensity)
        self.usage_patterns: Dict[str, Dict[str, Any]] = {
            "morning_peak": {"start": "07:00", "end": "09:00", "intensity": 0.8},
            "lunch_peak": {"start": "12:00", "end": "14:00", "intensity": 0.6},
            "evening_peak": {"start": "19:00", "end": "22:00", "intensity": 1.0},
            "weekend_pattern": {"start": "09:00", "end": "15:00", "intensity": 0.7},
        }
        # 2. Habitual user behavior scores
        self.behavioral_scores: Dict[str, float] = {
            "lurking": 3.98,
            "connection": 3.84,
            "play": 4.99,
            "browsing": 5.62,
        }
        # 3. Bot detection avoidance parameters
        self.bot_detection_thresholds: Dict[str, Any] = {
            "max_actions_per_minute": 1,
            "repeat_action_variance": 0.4,
            "max_sequence_repetition": 2,
        }
        # 4. Safety controls & rate limits
        self.safety_limits: Dict[str, int] = {
            "likes_per_hour": 60,
            "follows_per_hour": 30,
            "comments_per_hour": 15,
            "daily_action_limit": 500,
        }
        # 5. Randomization for natural sequences
        self.randomization_params: Dict[str, float] = {
            "delay_mean": 30.0,
            "delay_stddev": 10.0,
        }
        # 6. Algorithm compliance rules
        self.algorithm_rules: Dict[str, Any] = {
            "no_watermarks": True,
            "audio_required": True,
            "video_length_max": 180,
            "original_content_only": True,
        }

        self.algorithm_spec = INSTAGRAM_2025_ALGORITHM

    async def execute_engagement_strategy(
        self,
        action_plan: List[Dict[str, Any]],
        account_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute engagement actions with human-like pacing and compliance safeguards."""

        working_plan = list(action_plan)
        if not self._avoid_bot_detection(working_plan):
            random.shuffle(working_plan)

        timezone = account_config.get("timezone", "UTC")
        weekend_mode = account_config.get("weekend_mode", False)

        daily_count = 0
        hour_counters = {"like": 0, "follow": 0, "comment": 0}
        hour_window_start = datetime.utcnow()
        last_action_time: datetime | None = None
        executed: List[Dict[str, Any]] = []
        compliance_failures: List[Dict[str, Any]] = []

        for action in working_plan:
            if daily_count >= self.safety_limits["daily_action_limit"]:
                break

            now = datetime.utcnow()
            if (now - hour_window_start) >= timedelta(hours=1):
                hour_counters = {key: 0 for key in hour_counters}
                hour_window_start = now

            action_type = action.get("type", "like")
            hourly_limit = self.safety_limits.get(f"{action_type}s_per_hour")
            if hourly_limit is not None and hour_counters.get(action_type, 0) >= hourly_limit:
                continue

            if last_action_time is not None:
                min_interval = 60 / max(0.1, self.bot_detection_thresholds["max_actions_per_minute"])
                elapsed = (now - last_action_time).total_seconds()
                if elapsed < min_interval:
                    await asyncio.sleep(min_interval - elapsed)

            if not self._check_algorithm_compliance(action):
                compliance_failures.append(action)
                continue

            current_pattern = self._generate_human_pattern(now, timezone, weekend_mode)

            base_delay = max(
                1.0,
                random.gauss(
                    self.randomization_params["delay_mean"],
                    self.randomization_params["delay_stddev"],
                ),
            )
            delay_seconds = base_delay / max(0.2, current_pattern["intensity"])
            await asyncio.sleep(delay_seconds)

            # Placeholder for actual Riona client execution
            # await self.riona_client.perform_action(action)

            daily_count += 1
            hour_counters[action_type] = hour_counters.get(action_type, 0) + 1
            last_action_time = datetime.utcnow()

            executed.append(
                {
                    "action": action,
                    "executed_at": last_action_time.isoformat(),
                    "pattern": current_pattern,
                    "delay_seconds": round(delay_seconds, 2),
                }
            )

            if random.random() < self.bot_detection_thresholds["repeat_action_variance"]:
                extra_delay = random.uniform(5.0, 15.0)
                await asyncio.sleep(extra_delay)

        safety_snapshot = self._compose_safety_snapshot(executed, hour_counters, daily_count)
        compliance_snapshot = {
            "checked_rules": list(self.algorithm_rules.keys()),
            "failures": compliance_failures,
        }

        return {
            "executed_at": datetime.utcnow().isoformat(),
            "timezone": timezone,
            "weekend_mode": weekend_mode,
            "executed_actions": executed,
            "safety_snapshot": safety_snapshot,
            "algorithm_compliance": compliance_snapshot,
        }

    def _compose_safety_snapshot(
        self,
        executed: List[Dict[str, Any]],
        hour_counters: Dict[str, int],
        daily_count: int,
    ) -> Dict[str, Any]:
        bot_risk = 0.0
        if executed:
            ratio = daily_count / max(1, self.safety_limits["daily_action_limit"])
            bot_risk = round(ratio * self.bot_detection_thresholds["repeat_action_variance"], 3)

        return {
            "daily_actions": daily_count,
            "hour_counters": hour_counters,
            "bot_detection_risk": bot_risk,
        }

    def _check_algorithm_compliance(self, action: Dict[str, Any]) -> bool:
        """Ensure action plan meets 2025 algorithm rules before execution."""

        content = action.get("content", {})
        if self.algorithm_rules["no_watermarks"] and content.get("watermark_detected", False):
            return False
        if self.algorithm_rules["audio_required"] and not content.get("has_audio", False):
            return False
        if content.get("type") == "video" and content.get("length", 0) > self.algorithm_rules["video_length_max"]:
            return False
        if self.algorithm_rules["original_content_only"] and content.get("is_repost", False):
            return False
        return True

    def _generate_human_pattern(
        self,
        current_time: datetime,
        timezone: str,
        weekend_mode: bool,
    ) -> Dict[str, Any]:
        """Return intensity and behavior emphasis based on current time and usage patterns."""

        weekday = current_time.weekday()
        use_weekend = weekend_mode and weekday >= 5
        for name, cfg in self.usage_patterns.items():
            if name == "weekend_pattern" and not use_weekend:
                continue
            start_time = datetime.strptime(cfg["start"], "%H:%M").time()
            end_time = datetime.strptime(cfg["end"], "%H:%M").time()
            start = datetime.combine(current_time.date(), start_time)
            end = datetime.combine(current_time.date(), end_time)
            if start <= current_time <= end:
                return {
                    "pattern": name,
                    "intensity": cfg["intensity"],
                    "timezone": timezone,
                }

        return {
            "pattern": "off_peak",
            "intensity": 0.3,
            "timezone": timezone,
        }

    def _avoid_bot_detection(self, action_sequence: List[Dict[str, Any]]) -> bool:
        """Validate action sequence randomness and variance against bot detection thresholds."""

        if not action_sequence:
            return True

        seq_types = [action.get("type", "unknown") for action in action_sequence]
        highest_repetition = max(seq_types.count(t) for t in set(seq_types))
        if highest_repetition > self.bot_detection_thresholds["max_sequence_repetition"]:
            return False

        return True


# Backwards compatible facade for orchestrator expectations
class RionaImplementationBridge:
    """Translates implementation deliverables into Riona-compatible tasks."""

    def __init__(self) -> None:
        self.behavior_engine = RionaHumanBehaviorEngine()

    async def queue_tasks(
        self,
        execution_plan: Dict[str, Any],
        account_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run humanized automation sequences derived from execution plan."""

        actions = execution_plan.get("automation_scope", {}).get("actions", [])
        return await self.behavior_engine.execute_engagement_strategy(actions, account_config)
