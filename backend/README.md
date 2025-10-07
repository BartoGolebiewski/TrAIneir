# TrAIneir Backend

FastAPI-based MVP API that powers athlete and training plan management.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs can be
found at `/docs`.

## Available Endpoints

- `GET /health` – Basic readiness probe.
- `GET /athletes` / `POST /athletes` – List and create/update athletes.
- `GET /plans` / `POST /plans` – List and create/update training plans.
- `GET /plans/{plan_id}` – Retrieve a specific training plan.
- `POST /logs` – Submit a training log entry.
- `POST /analytics/compliance` – Returns a simple adherence summary for the
  requested plan.

The in-memory repository is provided for quick iteration. Swap `InMemoryRepository`
with a persistence-backed implementation once the domain stabilizes.
