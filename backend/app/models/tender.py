from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


TenderStatus = Literal["open", "closing_soon", "closed"]


class Tender(BaseModel):
    id: str
    title: str
    organization: str
    category: str
    location: str
    procurement_method: str
    published_at: date
    deadline: date
    estimated_value_pkr: int | None = None
    summary: str
    requirements: list[str] = Field(default_factory=list)
    source: str = "TenderIQ sample data"
    status: TenderStatus = "open"
    created_at: datetime | None = None


class AnalysisResult(BaseModel):
    score: int = Field(ge=0, le=100)
    recommendation: Literal["strong_match", "review", "low_match"]
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    explanation: str
    analyzed_at: datetime


class TenderWithAnalysis(Tender):
    analysis: AnalysisResult | None = None
