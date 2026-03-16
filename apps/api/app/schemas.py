from typing import Literal

from pydantic import BaseModel


class SearchItem(BaseModel):
    id: int
    type: Literal["theorem", "formula"]
    title: str
    snippet: str
    score: float


class SearchResponse(BaseModel):
    query: str
    items: list[SearchItem]


class TheoremOut(BaseModel):
    id: int
    name: str
    aliases: str | None = None
    statement_latex: str
    proof_md: str
    conditions: str | None = None
    tags: str | None = None
    refs: str | None = None

    class Config:
        from_attributes = True


class FormulaOut(BaseModel):
    id: int
    name: str
    latex: str
    meaning: str
    constraints: str | None = None
    examples: str | None = None
    refs: str | None = None

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
