# M0 Tasks (Autonomous Progress)

## Goal
Build a runnable baseline for theorem/formula search with proof display and basic algorithm trace animation.

## Delivered

- Repository skeleton created
- Docker Compose stack with `api`, `web`, `postgres`, `redis`, `qdrant`
- FastAPI baseline endpoints
- Seed content for sample theorems and formulas
- Initial SQL schema
- Ingest endpoint (`POST /api/ingest/doc`)
- Basic web demo page for search/detail and trace playback controls
- API smoke tests and CI workflow
- 50-sample seed generator (`scripts/generate_seed_50.py`)
- Retrieval benchmark script (`scripts/eval_retrieval.py`)

## Remaining for M0 completion

1. Curate and review 50 entries with exact citation page-level refs
2. Add content quality checks (source citation + review status)
3. Add worker process for async ingest and render jobs
4. Run full E2E verification once Docker engine is available
