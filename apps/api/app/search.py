from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from . import models
from .schemas import SearchItem


def _snippet(text: str, limit: int = 120) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def search_knowledge(db: Session, query: str, kind: str = "all", top_k: int = 20) -> list[SearchItem]:
    query_like = f"%{query}%"
    items: list[SearchItem] = []

    if kind in ("all", "theorem"):
        stmt = (
            select(models.Theorem)
            .where(
                or_(
                    func.lower(models.Theorem.name).like(func.lower(query_like)),
                    func.lower(func.coalesce(models.Theorem.aliases, "")).like(func.lower(query_like)),
                    func.lower(models.Theorem.statement_latex).like(func.lower(query_like)),
                )
            )
            .limit(top_k)
        )
        for row in db.execute(stmt).scalars().all():
            items.append(
                SearchItem(
                    id=row.id,
                    type="theorem",
                    title=row.name,
                    snippet=_snippet(row.statement_latex),
                    score=1.0,
                )
            )

    if kind in ("all", "formula"):
        stmt = (
            select(models.Formula)
            .where(
                or_(
                    func.lower(models.Formula.name).like(func.lower(query_like)),
                    func.lower(models.Formula.latex).like(func.lower(query_like)),
                    func.lower(models.Formula.meaning).like(func.lower(query_like)),
                )
            )
            .limit(top_k)
        )
        for row in db.execute(stmt).scalars().all():
            items.append(
                SearchItem(
                    id=row.id,
                    type="formula",
                    title=row.name,
                    snippet=_snippet(row.meaning),
                    score=1.0,
                )
            )

    return items[:top_k]
