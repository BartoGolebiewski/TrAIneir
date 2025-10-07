# TrAIneir

Apps for coaches to manage and monitor training sessions and training plans
for their athletes, using AI to analyze previous training plans, results, and
training logs.

## Repository Layout

- `backend/` – FastAPI MVP API with in-memory persistence. Provides endpoints
  for managing athletes, training plans, training logs, and basic compliance
  analytics.

## Next Steps

- Scaffold web/mobile clients that consume the API.
- Introduce persistent storage (PostgreSQL) and background jobs for analytics.
- Expand AI insights beyond compliance scoring.

## Publishing to GitHub

If you do not see the files in your GitHub repository, the local commits still
need to be pushed to the remote. From the project root run:

```bash
git remote -v          # verify the remote URL
git push origin work   # push the current branch
```

Replace `origin` with the name of your remote and `work` with the branch you
want to publish (for example, `main`). Once the push succeeds, the files and
commit history will appear in GitHub.
