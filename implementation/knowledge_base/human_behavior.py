"""Human Behavior Patterns for Instagram - Anti-Detection & Natural Usage Simulation"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
import random
import time
from enum import Enum


class UserType(Enum):
    """Types of Instagram users with different behavior patterns."""

    CASUAL_USER = "casual_user"
    PROFESSIONAL_MANAGER = "professional_manager"
    INFLUENCER = "influencer"
    BUSINESS_OWNER = "business_owner"


class ActivityLevel(Enum):
    """Activity levels for mood-based behavior variation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


# === NATURAL DAILY USAGE PATTERNS ===
DAILY_USAGE_PATTERNS: Dict[str, Any] = {
    "morning_patterns": {
        "wake_up_check": {
            "time_range": (7, 8.5),  # 7:00-8:30 AM
            "duration_minutes": (2, 5),
            "behavior": "Quick scroll, notifications check",
            "engagement_rate": 0.1,  # 10% of viewed content engaged with
        },
        "commute_usage": {
            "time_range": (8.5, 9.5),  # 8:30-9:30 AM
            "duration_minutes": (5, 15),
            "behavior": "Stories consumption, light engagement",
            "engagement_rate": 0.15,
        },
        "work_break": {
            "time_range": (10, 10.5),  # 10:00-10:30 AM
            "duration_minutes": (3, 8),
            "behavior": "Check notifications, respond to DMs",
            "engagement_rate": 0.25,
        },
    },
    "midday_patterns": {
        "lunch_scroll": {
            "time_range": (12, 12.5),  # 12:00-12:30 PM
            "duration_minutes": (10, 20),
            "behavior": "Active browsing, Reels consumption",
            "engagement_rate": 0.4,
        },
        "afternoon_check": {
            "time_range": (13, 14),  # 1:00-2:00 PM
            "duration_minutes": (5, 15),
            "behavior": "Respond to comments, check Stories",
            "engagement_rate": 0.35,
        },
    },
    "evening_patterns": {
        "peak_usage": {
            "time_range": (19, 21),  # 7:00-9:00 PM
            "duration_minutes": (15, 45),
            "behavior": "Prime consumption and posting window",
            "engagement_rate": 0.6,
        },
        "leisure_scroll": {
            "time_range": (20, 22),  # 8:00-10:00 PM
            "duration_minutes": (10, 30),
            "behavior": "Longer sessions, deeper engagement",
            "engagement_rate": 0.5,
        },
    },
    "weekend_adjustments": {
        "later_start": "Start 1-2 hours later than weekdays",
        "longer_sessions": "Sessions 1.5x longer duration",
        "more_leisure": "Higher entertainment content consumption",
    },
}


# === PROFESSIONAL SOCIAL MEDIA MANAGER PATTERNS ===
SOCIAL_MANAGER_SCHEDULE: Dict[str, Any] = {
    "morning_ritual": {
        "9:00-9:30": {
            "activity": "Platform audit and notification check",
            "actions": ["check_mentions", "review_comments", "scan_DMs"],
            "urgency": "high",
        },
        "9:30-10:00": {
            "activity": "Community engagement response",
            "actions": ["respond_comments", "reply_DMs", "acknowledge_mentions"],
            "target_response_time": "within_15_minutes",
        },
        "10:00-10:30": {
            "activity": "Daily content planning review",
            "actions": ["review_calendar", "adjust_schedule", "trend_research"],
            "strategic_focus": True,
        },
    },
    "content_creation_blocks": {
        "11:00-12:00": {
            "activity": "Content creation and editing",
            "actions": ["create_graphics", "write_captions", "edit_videos"],
            "batch_mode": True,
        },
        "14:00-15:00": {
            "activity": "Analytics and performance review",
            "actions": ["analyze_metrics", "identify_trends", "adjust_strategy"],
            "data_driven": True,
        },
    },
    "engagement_windows": {
        "12:30-13:30": "Lunch hour engagement boost",
        "17:00-18:00": "End of workday community management",
        "19:00-21:00": "Prime time monitoring and response",
    },
}


# === HUMAN PSYCHOLOGY PATTERNS ===
PSYCHOLOGICAL_USAGE_PATTERNS: Dict[str, Any] = {
    "urge_and_craving": {
        "description": "Compulsive checking behavior",
        "frequency_minutes": (30, 90),  # Check every 30-90 minutes
        "duration_seconds": (30, 180),  # 30 seconds to 3 minutes
        "trigger_events": ["notification", "boredom", "waiting"],
        "satisfaction_threshold": 0.3,
    },
    "passive_consumption": {
        "description": "Scrolling without active engagement",
        "frequency_daily": (3, 6),  # 3-6 sessions per day
        "duration_minutes": (5, 20),
        "engagement_rate": 0.05,  # Very low engagement
        "content_preference": ["videos", "images", "stories"],
    },
    "social_validation_seeking": {
        "description": "Seeking approval through likes/comments",
        "post_check_frequency": (5, 15),  # Check 5-15 times after posting
        "response_urgency": "immediate",  # Respond to comments quickly
        "validation_metrics": ["likes", "comments", "shares", "saves"],
    },
    "social_comparison": {
        "description": "Comparing to others' content",
        "session_duration_minutes": (10, 30),
        "behaviors": ["screenshot", "save", "share", "stalk_profile"],
        "emotional_impact": "varies",
    },
}


# === SAFETY & ANTI-DETECTION LIMITS ===
SAFETY_LIMITS: Dict[str, Any] = {
    "hourly_limits": {
        "likes": 60,  # Maximum 1 per minute
        "follows": 30,  # Maximum 0.5 per minute
        "unfollows": 30,  # Maximum 0.5 per minute
        "comments": 15,  # Maximum 0.25 per minute
        "story_views": 100,  # Maximum 1.67 per minute
        "dm_sends": 10,  # Maximum 0.17 per minute
    },
    "daily_limits": {
        "total_actions": 500,
        "likes": 1000,
        "follows": 200,
        "unfollows": 200,
        "comments": 100,
        "posts": 5,
        "stories": 10,
    },
    "weekly_limits": {
        "total_actions": 3000,
        "new_follows": 1000,
        "posts_created": 21,
        "stories_created": 49,
    },
    "mandatory_breaks": {
        "between_actions": (2, 10),  # 2-10 seconds between actions
        "session_breaks": (15, 45),  # 15-45 minute breaks between sessions
        "meal_breaks": [(12, 13), (19, 20)],  # Lunch and dinner breaks
        "sleep_period": (23, 7),  # 11 PM to 7 AM sleep
        "weekend_reduction": 0.7,  # 30% less activity on weekends
    },
}


# === BOT DETECTION EVASION PATTERNS ===
ANTI_DETECTION_STRATEGIES: Dict[str, Any] = {
    "timing_randomization": {
        "posting_variance": (900, 1800),  # ±15-30 minutes from scheduled
        "action_delays": (30, 180),  # 30-180 seconds between actions
        "session_jitter": (300, 900),  # 5-15 minutes session variance
        "daily_start_variance": (1800, 3600),  # ±30-60 minutes daily start
    },
    "behavior_inconsistency": {
        "mood_variations": {
            "high_activity": 0.2,  # 20% of days high activity
            "normal_activity": 0.6,  # 60% of days normal activity
            "low_activity": 0.2,  # 20% of days low activity
        },
        "engagement_patterns": {
            "like_only_sessions": 0.4,  # 40% sessions just liking
            "comment_heavy_sessions": 0.15,  # 15% sessions heavy commenting
            "mixed_sessions": 0.45,  # 45% mixed activity sessions
        },
    },
    "natural_imperfections": {
        "typos_in_comments": 0.02,  # 2% of comments have typos
        "delayed_responses": 0.1,  # 10% of responses delayed
        "missed_opportunities": 0.05,  # 5% of engagement opportunities missed
        "inconsistent_timing": 0.15,  # 15% of actions off-schedule
    },
}


class HumanBehaviorEngine:
    """Main engine for simulating natural human Instagram behavior."""

    def __init__(self, user_type: UserType = UserType.PROFESSIONAL_MANAGER):
        self.user_type = user_type
        self.current_session_start = None
        self.daily_action_counts: Dict[str, Dict[str, int]] = {}
        self.hourly_action_counts: Dict[str, Dict[str, int]] = {}
        self.last_action_time: Optional[datetime] = None

    def get_current_activity_level(self) -> ActivityLevel:
        """Determine current activity level based on time and day."""

        now = datetime.now()
        hour = now.hour
        is_weekend = now.weekday() >= 5

        # Peak hours: 12-14, 19-21
        if hour in [12, 13, 19, 20, 21]:
            return ActivityLevel.HIGH if not is_weekend else ActivityLevel.VERY_HIGH

        # Moderate hours: 9-11, 15-18
        if hour in [9, 10, 11, 15, 16, 17, 18]:
            return ActivityLevel.MEDIUM

        # Low activity hours: early morning, late night
        if hour in [7, 8, 22, 23] or (0 <= hour <= 6):
            return ActivityLevel.LOW

        return ActivityLevel.MEDIUM

    def should_take_break(self) -> bool:
        """Determine if a break should be taken based on natural patterns."""

        if not self.current_session_start:
            return False

        session_duration = (datetime.now() - self.current_session_start).seconds / 60
        activity_level = self.get_current_activity_level()

        # Break thresholds based on activity level
        break_thresholds = {
            ActivityLevel.LOW: 5,  # 5 minutes max
            ActivityLevel.MEDIUM: 15,  # 15 minutes max
            ActivityLevel.HIGH: 30,  # 30 minutes max
            ActivityLevel.VERY_HIGH: 45,  # 45 minutes max
        }

        return session_duration > break_thresholds[activity_level]

    def get_action_delay(self, action_type: str) -> float:
        """Get realistic delay between actions."""

        base_delays: Dict[str, Tuple[float, float]] = {
            "like": (2, 8),
            "comment": (10, 45),
            "follow": (5, 15),
            "unfollow": (3, 12),
            "post": (60, 300),  # 1-5 minutes
            "story": (30, 120),  # 30 seconds - 2 minutes
        }

        min_delay, max_delay = base_delays.get(action_type, (2, 10))

        # Add randomization based on activity level
        activity_level = self.get_current_activity_level()
        if activity_level == ActivityLevel.HIGH:
            min_delay *= 0.7  # Faster when highly active
            max_delay *= 0.8
        elif activity_level == ActivityLevel.LOW:
            min_delay *= 1.5  # Slower when less active
            max_delay *= 1.8

        return random.uniform(min_delay, max_delay)

    def is_within_safety_limits(self, action_type: str) -> bool:
        """Check if action is within safety limits."""

        now = datetime.now()
        hour_key = now.strftime("%Y-%m-%d-%H")
        day_key = now.strftime("%Y-%m-%d")

        # Initialize counters if needed
        if hour_key not in self.hourly_action_counts:
            self.hourly_action_counts[hour_key] = {}
        if day_key not in self.daily_action_counts:
            self.daily_action_counts[day_key] = {}

        # Check hourly limits
        hourly_count = self.hourly_action_counts[hour_key].get(action_type, 0)
        if hourly_count >= SAFETY_LIMITS["hourly_limits"].get(action_type, 999):
            return False

        # Check daily limits
        daily_count = self.daily_action_counts[day_key].get(action_type, 0)
        if daily_count >= SAFETY_LIMITS["daily_limits"].get(action_type, 9999):
            return False

        return True

    def record_action(self, action_type: str) -> None:
        """Record an action for safety limit tracking."""

        now = datetime.now()
        hour_key = now.strftime("%Y-%m-%d-%H")
        day_key = now.strftime("%Y-%m-%d")

        # Update counters
        if hour_key not in self.hourly_action_counts:
            self.hourly_action_counts[hour_key] = {}
        if day_key not in self.daily_action_counts:
            self.daily_action_counts[day_key] = {}

        self.hourly_action_counts[hour_key][action_type] = (
            self.hourly_action_counts[hour_key].get(action_type, 0) + 1
        )
        self.daily_action_counts[day_key][action_type] = (
            self.daily_action_counts[day_key].get(action_type, 0) + 1
        )

        self.last_action_time = now

    def get_optimal_posting_time(self, audience_type: str = "b2c") -> datetime:
        """Get next optimal posting time with human-like variance."""

        now = datetime.now()

        # Base optimal times
        optimal_hours = {
            "b2c": [11, 12, 13, 14, 19, 20, 21],
            "b2b": [10, 11, 12, 13, 14, 15],
            "mixed": [11, 12, 13, 14, 19, 20],
        }.get(audience_type, [12, 13, 19, 20])

        # Find next optimal hour
        current_hour = now.hour
        next_optimal: Optional[int] = None

        for hour in optimal_hours:
            if hour > current_hour:
                next_optimal = hour
                break

        # If no optimal time today, use tomorrow's first optimal time
        if next_optimal is None:
            next_optimal = min(optimal_hours)
            target_date = now + timedelta(days=1)
        else:
            target_date = now

        # Create target datetime
        target_time = target_date.replace(
            hour=next_optimal,
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
            microsecond=0,
        )

        # Add human-like variance (±15-30 minutes)
        variance_minutes = random.randint(-30, 30)
        target_time += timedelta(minutes=variance_minutes)

        return target_time

    def simulate_typing_delay(self, text_length: int) -> float:
        """Simulate realistic typing delay for comments/captions."""

        # Base typing speed: 40-80 WPM
        words = text_length / 5  # Approximate words
        wpm = random.uniform(40, 80)
        base_time = (words / wpm) * 60  # Convert to seconds

        # Add thinking/editing time
        thinking_time = random.uniform(5, 30)  # 5-30 seconds thinking

        return base_time + thinking_time

    def should_add_typo(self) -> bool:
        """Determine if a typo should be added for naturalness."""

        return (
            random.random()
            < ANTI_DETECTION_STRATEGIES["natural_imperfections"]["typos_in_comments"]
        )

    def get_session_duration(self) -> int:
        """Get realistic session duration in minutes."""

        activity_level = self.get_current_activity_level()

        duration_ranges: Dict[ActivityLevel, Tuple[int, int]] = {
            ActivityLevel.LOW: (2, 8),
            ActivityLevel.MEDIUM: (5, 20),
            ActivityLevel.HIGH: (10, 35),
            ActivityLevel.VERY_HIGH: (15, 45),
        }

        min_duration, max_duration = duration_ranges[activity_level]
        return random.randint(min_duration, max_duration)


def get_behavior_pattern(user_type: UserType) -> Dict[str, Any]:
    """Get behavior pattern for specific user type."""

    if user_type == UserType.PROFESSIONAL_MANAGER:
        return SOCIAL_MANAGER_SCHEDULE
    if user_type == UserType.CASUAL_USER:
        return DAILY_USAGE_PATTERNS
    return DAILY_USAGE_PATTERNS  # Default to casual patterns


def is_peak_engagement_time() -> bool:
    """Check if current time is peak engagement time."""

    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # Peak times: 12:00-14:00 and 19:00-21:00
    peak_windows = [
        (12, 0, 14, 0),  # Lunch time
        (19, 0, 21, 0),  # Evening time
    ]

    for start_hour, start_min, end_hour, end_min in peak_windows:
        if (start_hour < hour < end_hour) or (
            hour == start_hour and minute >= start_min
        ) or (hour == end_hour and minute <= end_min):
            return True

    return False


def get_natural_break_duration() -> int:
    """Get natural break duration in minutes."""

    break_type = random.choice(["short", "medium", "long"])

    durations: Dict[str, Tuple[int, int]] = {
        "short": (15, 30),  # 15-30 minutes
        "medium": (45, 90),  # 45-90 minutes
        "long": (2 * 60, 4 * 60),  # 2-4 hours
    }

    min_duration, max_duration = durations[break_type]
    return random.randint(min_duration, max_duration)


__all__ = [
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
