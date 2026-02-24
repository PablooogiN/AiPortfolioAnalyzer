from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from database import Base, engine, get_db
from models import Holding
from schemas import AnalyzeRequest, HoldingCreate, HoldingResponse, HoldingUpdate
from services.ai_service import stream_analysis
from services.stock_service import enrich_holdings, get_prices

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Holdings CRUD ──────────────────────────────────────────────


@app.get("/api/holdings", response_model=list[HoldingResponse])
def list_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).order_by(Holding.ticker).all()


@app.post("/api/holdings", response_model=HoldingResponse, status_code=201)
def create_holding(body: HoldingCreate, db: Session = Depends(get_db)):
    holding = Holding(**body.model_dump())
    holding.ticker = holding.ticker.upper().strip()
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


@app.put("/api/holdings/{holding_id}", response_model=HoldingResponse)
def update_holding(
    holding_id: int, body: HoldingUpdate, db: Session = Depends(get_db)
):
    holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        if key == "ticker" and value:
            value = value.upper().strip()
        setattr(holding, key, value)
    db.commit()
    db.refresh(holding)
    return holding


@app.delete("/api/holdings/{holding_id}", status_code=204)
def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(holding)
    db.commit()


# ── Portfolio Summary ──────────────────────────────────────────


@app.get("/api/portfolio")
def portfolio_summary(db: Session = Depends(get_db)):
    holdings = db.query(Holding).all()
    if not holdings:
        return {"holdings": [], "total_value": 0, "total_cost": 0}
    priced = get_prices(holdings)
    total_value = sum(h["current_value"] for h in priced)
    total_cost = sum(h["shares"] * h["avg_cost"] for h in priced)
    for h in priced:
        h["weight"] = round(h["current_value"] / total_value * 100, 2) if total_value else 0
    return {
        "holdings": priced,
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_gain_loss": round(total_value - total_cost, 2),
        "total_gain_loss_pct": round((total_value - total_cost) / total_cost * 100, 2)
        if total_cost
        else 0,
    }


# ── AI Analysis (SSE streaming) ───────────────────────────────


@app.post("/api/analyze")
async def analyze_portfolio(body: AnalyzeRequest, db: Session = Depends(get_db)):
    holdings = db.query(Holding).all()
    if not holdings:
        raise HTTPException(status_code=400, detail="No holdings to analyze")
    enriched = enrich_holdings(holdings)
    total_value = sum(h["current_value"] for h in enriched)
    for h in enriched:
        h["weight"] = round(h["current_value"] / total_value * 100, 2) if total_value else 0
    return EventSourceResponse(stream_analysis(enriched, body.strategy))
