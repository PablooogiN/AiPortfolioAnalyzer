from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    account_type = Column(String, nullable=False, default="post-tax")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class PortfolioSettings(Base):
    __tablename__ = "portfolio_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pre_tax_cash = Column(Float, nullable=False, default=0.0)
    post_tax_cash = Column(Float, nullable=False, default=0.0)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
