from typing import Literal

from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    id: int
    type: Literal["theorem", "formula"]
    title: str
    snippet: str
    score: float


class SearchResponse(BaseModel):
    query: str
    items: list[SearchItem]


ReviewStatus = Literal["draft", "reviewed", "verified"]


class TheoremOut(BaseModel):
    id: int
    name: str
    aliases: str | None = None
    statement_latex: str
    proof_md: str
    conditions: str | None = None
    tags: str | None = None
    refs: str
    source_url: str | None = None
    source_license: str | None = None
    review_status: ReviewStatus = "draft"

    class Config:
        from_attributes = True


class FormulaOut(BaseModel):
    id: int
    name: str
    latex: str
    meaning: str
    constraints: str | None = None
    examples: str | None = None
    refs: str
    source_url: str | None = None
    source_license: str | None = None
    review_status: ReviewStatus = "draft"

    class Config:
        from_attributes = True


class TraceRequest(BaseModel):
    algorithm: Literal["binary_search", "bubble_sort"]
    array: list[int]
    target: int | None = None


class TraceStep(BaseModel):
    step: int
    state: list[int]
    highlight: list[int]
    code_line: int
    caption: str


class TraceResponse(BaseModel):
    algorithm: str
    steps: list[TraceStep]


class IngestTheoremIn(BaseModel):
    name: str
    aliases: str | None = None
    statement_latex: str
    proof_md: str
    conditions: str | None = None
    tags: str | None = None
    refs: str = Field(..., min_length=3)
    source_url: str | None = None
    source_license: str | None = None
    review_status: ReviewStatus = "draft"


class IngestFormulaIn(BaseModel):
    name: str
    latex: str
    meaning: str
    constraints: str | None = None
    examples: str | None = None
    refs: str = Field(..., min_length=3)
    source_url: str | None = None
    source_license: str | None = None
    review_status: ReviewStatus = "draft"


class IngestRequest(BaseModel):
    theorems: list[IngestTheoremIn] = Field(default_factory=list)
    formulas: list[IngestFormulaIn] = Field(default_factory=list)


class IngestResponse(BaseModel):
    inserted_theorems: int
    inserted_formulas: int
    skipped_theorems: int
    skipped_formulas: int


class RenderRequest(BaseModel):
    trace: dict


class RenderResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    enqueued_at: str | None = None
    ended_at: str | None = None
    result: dict | None = None
    error: str | None = None
