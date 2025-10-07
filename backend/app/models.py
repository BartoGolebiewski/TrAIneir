from __future__ import annotations

from datetime import UTC, date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Athlete(BaseModel):
    """Representation of an athlete within a coaching roster."""

    id: str = Field(..., description="Unique identifier for the athlete")
    name: str = Field(..., description="Full name of the athlete")
    date_of_birth: Optional[date] = Field(
        None, description="Date of birth used for age-based workload insights"
    )
    sport: Optional[str] = Field(None, description="Primary sport or discipline")
    notes: Optional[str] = Field(
        None, description="Optional background notes shared across the coaching staff"
    )


class TrainingSession(BaseModel):
    """Single training session that belongs to a training plan."""

    id: str = Field(..., description="Unique identifier for the session")
    title: str = Field(..., description="Name of the session")
    scheduled_for: date = Field(..., description="Date the session is scheduled for")
    focus_area: Optional[str] = Field(
        None, description="Key focus (e.g. endurance, strength, recovery)"
    )
    duration_minutes: Optional[int] = Field(
        None, description="Planned duration of the session in minutes"
    )
    details: Optional[str] = Field(
        None, description="Detailed session plan or instructions for athletes"
    )


class TrainingLog(BaseModel):
    """Log entry submitted after a session is completed."""

    session_id: str = Field(..., description="Identifier of the session that was logged")
    athlete_id: str = Field(..., description="Identifier of the athlete logging the session")
    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the session was completed",
    )
    rpe: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Rate of perceived exertion on a 1-10 scale",
    )
    notes: Optional[str] = Field(None, description="Free-form feedback from the athlete")


class TrainingPlan(BaseModel):
    """Training plan containing multiple sessions for an athlete or group."""

    id: str = Field(..., description="Unique identifier for the plan")
    title: str = Field(..., description="Name of the training plan")
    owner_id: str = Field(..., description="Coach responsible for the plan")
    athlete_ids: List[str] = Field(
        default_factory=list,
        description="List of athletes assigned to the plan",
    )
    sessions: List[TrainingSession] = Field(
        default_factory=list, description="Sessions scheduled as part of this plan"
    )
    tags: List[str] = Field(default_factory=list, description="Searchable tags")


class ComplianceSummary(BaseModel):
    """Simple analytics payload describing plan adherence."""

    plan_id: str
    athlete_id: str
    sessions_planned: int
    sessions_logged: int
    compliance_rate: float = Field(
        ..., description="Percentage of logged sessions vs planned sessions"
    )
    flagged_sessions: List[str] = Field(
        default_factory=list,
        description="Sessions that need coach attention (e.g. missed, high RPE)",
    )


class InsightRequest(BaseModel):
    """Parameters controlling insight generation for a plan."""

    plan_id: str
    athlete_id: Optional[str] = None
    lookback_days: int = Field(30, ge=7, le=180)
