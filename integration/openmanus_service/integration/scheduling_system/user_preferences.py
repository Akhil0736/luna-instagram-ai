from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import time, datetime
import json

class WorkingHours(BaseModel):
    start_time: str = Field(default="09:00")
    end_time: str = Field(default="17:00") 
    timezone: str = Field(default="UTC")

class BreakPreferences(BaseModel):
    coffee_breaks: bool = Field(default=True)
    coffee_break_probability: float = Field(default=0.05)
    coffee_break_duration: Dict[str, int] = Field(default={"min": 5, "max": 15})
    lunch_break: bool = Field(default=True)
    lunch_break_start: str = Field(default="12:00")
    lunch_break_end: str = Field(default="13:00")
    lunch_break_duration: Dict[str, int] = Field(default={"min": 30, "max": 60})

class ActivitySettings(BaseModel):
    daily_likes: int = Field(default=50, ge=10, le=200)
    daily_follows: int = Field(default=20, ge=5, le=100)
    daily_comments: int = Field(default=8, ge=2, le=50)
    activity_intensity: str = Field(default="moderate")
    randomize_timing: bool = Field(default=True)
    min_delay_seconds: int = Field(default=10)
    max_delay_seconds: int = Field(default=120)

class WeeklySchedule(BaseModel):
    active_days: List[str] = Field(default=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"])
    weekend_mode: bool = Field(default=False)
    weekend_intensity: float = Field(default=0.5)

class UserSchedulingPreferences(BaseModel):
    user_id: str
    working_hours: WorkingHours = Field(default_factory=WorkingHours)
    break_preferences: BreakPreferences = Field(default_factory=BreakPreferences)
    activity_settings: ActivitySettings = Field(default_factory=ActivitySettings)
    weekly_schedule: WeeklySchedule = Field(default_factory=WeeklySchedule)
    stealth_mode: bool = Field(default=True)
    adaptive_scheduling: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)
