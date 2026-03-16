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
- Basic web demo page for search and detail
- API smoke tests and CI workflow

## Remaining for M0 completion

1. Add first 50 curated entries (theorem/formula/proof)
2. Add content quality checks (source citation + review status)
3. Add retrieval benchmark script (Recall@k, MRR, NDCG@10)
4. Add worker process for async ingest and render jobs
