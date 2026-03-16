from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base


class Theorem(Base):
    __tablename__ = "theorem"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    aliases = Column(String(255), nullable=True)
    statement_latex = Column(Text, nullable=False)
    proof_md = Column(Text, nullable=False)
    conditions = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)
    refs = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    source_license = Column(String(100), nullable=True)
    review_status = Column(String(32), nullable=False, default="draft")


class Formula(Base):
    __tablename__ = "formula"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    latex = Column(Text, nullable=False)
    meaning = Column(Text, nullable=False)
    constraints = Column(Text, nullable=True)
    examples = Column(Text, nullable=True)
    refs = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    source_license = Column(String(100), nullable=True)
    review_status = Column(String(32), nullable=False, default="draft")


class Algorithm(Base):
    __tablename__ = "algo"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    complexity = Column(String(100), nullable=True)
    pseudocode = Column(Text, nullable=True)


class TheoremDependency(Base):
    __tablename__ = "theorem_dependency"

    id = Column(Integer, primary_key=True)
    theorem_id = Column(Integer, ForeignKey("theorem.id"), nullable=False)
    depends_on_theorem_id = Column(Integer, ForeignKey("theorem.id"), nullable=False)

    theorem = relationship("Theorem", foreign_keys=[theorem_id])
    depends_on = relationship("Theorem", foreign_keys=[depends_on_theorem_id])
