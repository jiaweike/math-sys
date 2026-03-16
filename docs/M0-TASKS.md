# M0 Tasks (Autonomous Progress)

## Goal
Build a runnable baseline for theorem/formula search with proof display and basic algorithm trace animation.

## Delivered

- Repository skeleton created
- Docker Compose stack with `api`, `postgres`, `redis`, `qdrant`
- FastAPI baseline endpoints
- Seed content for sample theorems and formulas
- Initial SQL schema

## Remaining for M0 completion

1. Add ingest endpoint and pipeline (`POST /api/ingest/doc`)
2. Add first 50 curated entries (theorem/formula/proof)
3. Add basic web page for search and theorem detail
4. Add integration tests for `/api/search` and `/api/theorems/{id}`
5. Add CI workflow (lint/test/build)
