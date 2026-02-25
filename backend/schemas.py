from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HoldingCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    shares: float = Field(..., gt=0)
    account_type: Literal["pre-tax", "post-tax"] = "post-tax"


class HoldingUpdate(BaseModel):
    ticker: str | None = Field(None, min_length=1, max_length=10)
    shares: float | None = Field(None, gt=0)
    account_type: Literal["pre-tax", "post-tax"] | None = None


class HoldingResponse(BaseModel):
    id: int
    ticker: str
    shares: float
    account_type: str
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class CashPositionsUpdate(BaseModel):
    pre_tax_cash: float = Field(..., ge=0)
    post_tax_cash: float = Field(..., ge=0)


class CashPositionsResponse(BaseModel):
    pre_tax_cash: float
    post_tax_cash: float

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
