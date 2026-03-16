from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine, get_db
from .jobs import enqueue_render, get_job_status
from .models import Formula, Theorem
from .schemas import (
    FormulaOut,
    IngestRequest,
    IngestResponse,
    JobStatusResponse,
    RenderRequest,
    RenderResponse,
    SearchResponse,
    TheoremOut,
    TraceRequest,
    TraceResponse,
)
from .search import search_knowledge
from .seed import seed_if_needed
from .trace import binary_search_trace, bubble_sort_trace
from .config import settings

app = FastAPI(title="math-sys api", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    if settings.seed_on_start:
        db = SessionLocal()
        try:
            seed_if_needed(db)
        finally:
            db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1),
    type: str = Query("all", pattern="^(all|theorem|formula)$"),
    top_k: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
) -> SearchResponse:
    items = search_knowledge(db, query=q, kind=type, top_k=top_k)
    return SearchResponse(query=q, items=items)


@app.get("/api/theorems/{theorem_id}", response_model=TheoremOut)
def get_theorem(theorem_id: int, db: Session = Depends(get_db)) -> TheoremOut:
    row = db.get(Theorem, theorem_id)
    if not row:
        raise HTTPException(status_code=404, detail="theorem not found")
    return row


@app.get("/api/formulas/{formula_id}", response_model=FormulaOut)
def get_formula(formula_id: int, db: Session = Depends(get_db)) -> FormulaOut:
    row = db.get(Formula, formula_id)
    if not row:
        raise HTTPException(status_code=404, detail="formula not found")
    return row


@app.post("/api/ingest/doc", response_model=IngestResponse)
def ingest_doc(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    inserted_theorems = 0
    inserted_formulas = 0
    skipped_theorems = 0
    skipped_formulas = 0

    for item in payload.theorems:
        exists = db.query(Theorem).filter(Theorem.name == item.name).first()
        if exists:
            skipped_theorems += 1
            continue
        db.add(Theorem(**item.model_dump()))
        inserted_theorems += 1

    for item in payload.formulas:
        exists = db.query(Formula).filter(Formula.name == item.name).first()
        if exists:
            skipped_formulas += 1
            continue
        db.add(Formula(**item.model_dump()))
        inserted_formulas += 1

    db.commit()
    return IngestResponse(
        inserted_theorems=inserted_theorems,
        inserted_formulas=inserted_formulas,
        skipped_theorems=skipped_theorems,
        skipped_formulas=skipped_formulas,
    )


@app.post("/api/animations/render", response_model=RenderResponse)
def render_trace(payload: RenderRequest) -> RenderResponse:
    try:
        job_id = enqueue_render(payload.trace)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"render queue unavailable: {exc}") from exc

    return RenderResponse(job_id=job_id, status="queued")


@app.get("/api/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str) -> JobStatusResponse:
    try:
        return JobStatusResponse(**get_job_status(job_id))
    except Exception as exc:
        if exc.__class__.__name__ == "NoSuchJobError":
            raise HTTPException(status_code=404, detail="job not found") from exc
        raise HTTPException(status_code=503, detail=f"job backend unavailable: {exc}") from exc


@app.post("/api/animations/trace", response_model=TraceResponse)
def create_trace(payload: TraceRequest) -> TraceResponse:
    if payload.algorithm == "binary_search":
        if payload.target is None:
            raise HTTPException(status_code=400, detail="target is required for binary_search")
        steps = binary_search_trace(payload.array, payload.target)
    else:
        steps = bubble_sort_trace(payload.array)

    return TraceResponse(algorithm=payload.algorithm, steps=steps)
