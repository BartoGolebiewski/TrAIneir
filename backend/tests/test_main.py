from datetime import date, datetime, timezone

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
for candidate in (ROOT, PROJECT_ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_plan_lifecycle() -> None:
    athlete_payload = {"id": "athlete-1", "name": "Alex Runner"}
    response = client.post("/athletes", json=athlete_payload)
    assert response.status_code == 201

    plan_payload = {
        "id": "plan-1",
        "title": "Base Phase",
        "owner_id": "coach-1",
        "athlete_ids": ["athlete-1"],
        "sessions": [
            {
                "id": "session-1",
                "title": "Interval Run",
                "scheduled_for": date.today().isoformat(),
            }
        ],
    }
    response = client.post("/plans", json=plan_payload)
    assert response.status_code == 201

    response = client.get("/plans/plan-1")
    assert response.status_code == 200
    assert response.json()["title"] == "Base Phase"

    log_payload = {
        "session_id": "session-1",
        "athlete_id": "athlete-1",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "rpe": 7,
    }
    response = client.post("/logs", json=log_payload)
    assert response.status_code == 201

    analytics_payload = {"plan_id": "plan-1"}
    response = client.post("/analytics/compliance", json=analytics_payload)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["sessions_logged"] == 1
    assert data[0]["compliance_rate"] == 100.0
