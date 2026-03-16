# M0 Tasks (Autonomous Progress)

## Goal
Build a runnable baseline for theorem/formula search with proof display and basic algorithm trace animation.

## Delivered

- Repository skeleton created
- Docker Compose stack with `api`, `web`, `worker`, `postgres`, `redis`, `qdrant`
- FastAPI baseline endpoints
- Seed content for sample theorems and formulas
- Initial SQL schema
- Ingest endpoint (`POST /api/ingest/doc`) with duplicate-skip counters
- Async render enqueue + job status endpoints (`POST /api/animations/render`, `GET /api/jobs/{job_id}`)
- Basic web demo page for search/detail and trace playback controls
- API smoke tests and CI workflow
- 50-sample seed generator (`scripts/generate_seed50.py`)
- Retrieval benchmark script (`scripts/eval_retrieval.py`)
- Content quality checker (`scripts/check_content_quality.py`)
- Content metadata fields (review status, source URL, source license)

## Remaining for M0 completion

1. Curate and review 50 entries with exact citation page-level refs
2. Add real render pipeline (manim/ffmpeg) to replace placeholder trace artifact
3. Run full E2E verification once Docker engine is available
