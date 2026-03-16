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
  - `POST /api/animations/render`
  - `GET /api/jobs/{job_id}`
- Web demo pages for search/detail + trace player controls
- Docker Compose stack with `api`, `web`, `worker`, `postgres`, `redis`, `qdrant`
- SQL bootstrap and content-quality migration scripts
- Retrieval evaluation + content quality scripts

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

- Generate 50 sample entries: `python scripts/generate_seed50.py`
- Check content quality: `python scripts/check_content_quality.py`
- Ingest sample payload: `powershell -File scripts/ingest-sample.ps1`
- Evaluate retrieval quality: `python scripts/eval_retrieval.py --api http://localhost:8000 --k 10`

## Next step

Move from M0 to MVP:

- Add BM25 + vector hybrid retrieval and rerank
- Add async worker for ingest/render jobs
- Add theorem citation review workflow and status tags
