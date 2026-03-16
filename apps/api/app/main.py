from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine, get_db
from .models import Formula, Theorem
from .schemas import FormulaOut, SearchResponse, TheoremOut, TraceRequest, TraceResponse
from .search import search_knowledge
from .seed import seed_if_needed
from .trace import binary_search_trace, bubble_sort_trace
from .config import settings

app = FastAPI(title="math-sys api", version="0.1.0")


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


@app.post("/api/animations/trace", response_model=TraceResponse)
def create_trace(payload: TraceRequest) -> TraceResponse:
    if payload.algorithm == "binary_search":
        if payload.target is None:
            raise HTTPException(status_code=400, detail="target is required for binary_search")
        steps = binary_search_trace(payload.array, payload.target)
    else:
        steps = bubble_sort_trace(payload.array)

    return TraceResponse(algorithm=payload.algorithm, steps=steps)
