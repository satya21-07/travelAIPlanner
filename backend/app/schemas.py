from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class ItineraryRequest(BaseModel):
    destination: str = Field(..., min_length=2, max_length=120)
    start_location: Optional[str] = Field(default=None, max_length=120)
    days: int = Field(..., ge=1, le=21)
    travelers: int = Field(default=1, ge=1, le=12)
    budget: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=8)
    travel_style: str = Field(default="balanced", max_length=40)
    interests: list[str] = Field(default_factory=list)


class DayPlan(BaseModel):
    day: int
    title: str
    morning: str
    afternoon: str
    evening: str
    food: str
    estimated_cost: float


class ItineraryResponse(BaseModel):
    id: int
    destination: str
    start_location: Optional[str]
    days: int
    travelers: int
    budget: float
    currency: str
    travel_style: str
    interests: list[str]
    summary: str
    total_estimated_cost: float
    daily_plan: list[DayPlan]
    cost_breakdown: dict[str, float]
    tips: list[str]
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Destination(BaseModel):
    name: str
    region: str
    tags: list[str]
    base_daily_cost: int
    best_for: str
    image: str
    video: Optional[str] = None
    highlights: list[str]


class ErrorResponse(BaseModel):
    detail: Union[str, dict[str, Any]]
