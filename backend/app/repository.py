"""Simple in-memory repository for MVP prototyping.

The repository abstractions allow future replacement with a database layer
without forcing changes to the API handlers. Data is stored in dictionaries
keyed by identifiers to keep lookups efficient.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Dict, Iterable, List, Optional

from .models import Athlete, ComplianceSummary, InsightRequest, TrainingLog, TrainingPlan


class InMemoryRepository:
    """Minimal repository used during early product discovery."""

    def __init__(self) -> None:
        self._athletes: Dict[str, Athlete] = {}
        self._plans: Dict[str, TrainingPlan] = {}
        self._logs: List[TrainingLog] = []

    # Athlete operations -------------------------------------------------
    def list_athletes(self) -> Iterable[Athlete]:
        return self._athletes.values()

    def upsert_athlete(self, athlete: Athlete) -> Athlete:
        self._athletes[athlete.id] = athlete
        return athlete

    # Plan operations ----------------------------------------------------
    def list_plans(self) -> Iterable[TrainingPlan]:
        return self._plans.values()

    def get_plan(self, plan_id: str) -> Optional[TrainingPlan]:
        return self._plans.get(plan_id)

    def upsert_plan(self, plan: TrainingPlan) -> TrainingPlan:
        self._plans[plan.id] = plan
        return plan

    # Logging operations -------------------------------------------------
    def add_log(self, log: TrainingLog) -> TrainingLog:
        self._logs.append(log)
        return log

    def list_logs_for_plan(self, plan_id: str) -> List[TrainingLog]:
        plan = self._plans.get(plan_id)
        if not plan:
            return []
        session_ids = {session.id for session in plan.sessions}
        return [log for log in self._logs if log.session_id in session_ids]

    def list_logs_for_athlete(self, athlete_id: str) -> List[TrainingLog]:
        return [log for log in self._logs if log.athlete_id == athlete_id]

    # Analytics ----------------------------------------------------------
    def summarize_compliance(self, request: InsightRequest) -> List[ComplianceSummary]:
        summaries: List[ComplianceSummary] = []
        plan = self._plans.get(request.plan_id)
        if not plan:
            return summaries

        logs_by_athlete: Dict[str, List[TrainingLog]] = defaultdict(list)
        for log in self._logs:
            if log.session_id in {session.id for session in plan.sessions}:
                logs_by_athlete[log.athlete_id].append(log)

        athletes = request.athlete_id and [request.athlete_id] or plan.athlete_ids
        for athlete_id in athletes:
            planned_sessions = len(plan.sessions)
            athlete_logs = logs_by_athlete.get(athlete_id, [])
            sessions_logged = len(athlete_logs)
            compliance = (sessions_logged / planned_sessions * 100.0) if planned_sessions else 0.0
            flagged = [
                log.session_id
                for log in athlete_logs
                if log.rpe and log.rpe >= 8
            ]
            summaries.append(
                ComplianceSummary(
                    plan_id=plan.id,
                    athlete_id=athlete_id,
                    sessions_planned=planned_sessions,
                    sessions_logged=sessions_logged,
                    compliance_rate=round(compliance, 2),
                    flagged_sessions=flagged,
                )
            )

        return summaries

    def recent_logs(self, lookback_days: int) -> List[TrainingLog]:
        cutoff = datetime.now(UTC) - timedelta(days=lookback_days)
        return [log for log in self._logs if log.completed_at >= cutoff]
