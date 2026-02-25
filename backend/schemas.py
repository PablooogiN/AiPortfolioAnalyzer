from datetime import datetime

from pydantic import BaseModel, Field


class HoldingCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    shares: float = Field(..., gt=0)
    avg_cost: float = Field(..., gt=0)
    date_added: str


class HoldingUpdate(BaseModel):
    ticker: str | None = Field(None, min_length=1, max_length=10)
    shares: float | None = Field(None, gt=0)
    avg_cost: float | None = Field(None, gt=0)
    date_added: str | None = None


class HoldingResponse(BaseModel):
    id: int
    ticker: str
    shares: float
    avg_cost: float
    date_added: str
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class AnalyzeRequest(BaseModel):
    strategy: str = Field(..., min_length=1)


class Recommendation(BaseModel):
    action: str
    ticker: str
    rationale: str


class AnalysisResponse(BaseModel):
    summary: str
    key_findings: list[str]
    recommendations: list[Recommendation]
    risk_warnings: list[str]
