from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status

from .models import (
    Athlete,
    ComplianceSummary,
    InsightRequest,
    TrainingLog,
    TrainingPlan,
)
from .repository import InMemoryRepository

app = FastAPI(
    title="TrAIneir API",
    version="0.1.0",
    description="MVP API for managing athletes, training plans, and insights.",
)


def get_repository() -> InMemoryRepository:
    """Provide a repository instance.

    For early MVP work we use a singleton in-memory repository. When replacing
    with a persistent store, this function can be refactored to provide a
    database session or another dependency-injected resource.
    """

    if not hasattr(get_repository, "_repo"):
        get_repository._repo = InMemoryRepository()  # type: ignore[attr-defined]
    return get_repository._repo  # type: ignore[attr-defined]


@app.get("/health", summary="API health check")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/athletes", response_model=list[Athlete])
def list_athletes(repo: InMemoryRepository = Depends(get_repository)) -> list[Athlete]:
    return list(repo.list_athletes())


@app.post(
    "/athletes",
    response_model=Athlete,
    status_code=status.HTTP_201_CREATED,
)
def upsert_athlete(
    athlete: Athlete, repo: InMemoryRepository = Depends(get_repository)
) -> Athlete:
    return repo.upsert_athlete(athlete)


@app.get("/plans", response_model=list[TrainingPlan])
def list_plans(repo: InMemoryRepository = Depends(get_repository)) -> list[TrainingPlan]:
    return list(repo.list_plans())


@app.get("/plans/{plan_id}", response_model=TrainingPlan)
def get_plan(
    plan_id: str, repo: InMemoryRepository = Depends(get_repository)
) -> TrainingPlan:
    plan = repo.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan


@app.post(
    "/plans",
    response_model=TrainingPlan,
    status_code=status.HTTP_201_CREATED,
)
def upsert_plan(
    plan: TrainingPlan, repo: InMemoryRepository = Depends(get_repository)
) -> TrainingPlan:
    return repo.upsert_plan(plan)


@app.post(
    "/logs",
    response_model=TrainingLog,
    status_code=status.HTTP_201_CREATED,
)
def add_log(log: TrainingLog, repo: InMemoryRepository = Depends(get_repository)) -> TrainingLog:
    return repo.add_log(log)


@app.post(
    "/analytics/compliance",
    response_model=list[ComplianceSummary],
)
def summarize_compliance(
    request: InsightRequest, repo: InMemoryRepository = Depends(get_repository)
) -> list[ComplianceSummary]:
    return repo.summarize_compliance(request)
