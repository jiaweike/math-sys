# math-sys

Math knowledge system for theorem/formula search with proofs and algorithm animation demos.

## Milestone (M0)

Current repository includes:

- Monorepo skeleton (`apps`, `infra`, `scripts`, `docs`)
- FastAPI service with minimal endpoints:
  - `GET /health`
  - `GET /api/search`
  - `GET /api/theorems/{id}`
  - `GET /api/formulas/{id}`
  - `POST /api/animations/trace`
- PostgreSQL + Redis + Qdrant via Docker Compose
- SQL bootstrap and seed data

## Quick start

1. Copy env file:

```bash
cp .env.example .env
```

2. Start services:

```bash
docker compose up --build
```

3. Open API docs:

- API docs: http://localhost:8000/docs
- Web demo: http://localhost:3000

## Project layout

```text
apps/
  api/
  web/
  worker/
infra/
  sql/
scripts/
docs/
```

## Next step

Move from M0 to MVP:

- Add ingest pipeline (`POST /api/ingest/doc`)
- Add BM25 + vector hybrid retrieval
- Add web search/detail UI and playback controls for animation traces
