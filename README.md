# math-sys

Math knowledge system for theorem/formula search with proofs and algorithm animation demos.

## Milestone (M0)

Current repository includes:

- Monorepo skeleton (`apps`, `infra`, `scripts`, `docs`)
- FastAPI service with core endpoints:
  - `GET /health`
  - `GET /api/search`
  - `GET /api/theorems/{id}`
  - `GET /api/formulas/{id}`
  - `POST /api/ingest/doc`
  - `POST /api/animations/trace`
- Web demo pages for search/detail + trace player controls
- PostgreSQL + Redis + Qdrant via Docker Compose
- SQL bootstrap and seed data
- Retrieval evaluation script (`scripts/eval_retrieval.py`)

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

## Utility scripts

- Generate 50 sample entries: `python scripts/generate_seed_50.py`
- Ingest sample payload: `powershell -File scripts/ingest-sample.ps1`
- Evaluate retrieval quality: `python scripts/eval_retrieval.py --api-base http://localhost:8000 --top-k 10`

## Next step

Move from M0 to MVP:

- Add BM25 + vector hybrid retrieval and rerank
- Add async worker for ingest/render jobs
- Add theorem citation review workflow and status tags
