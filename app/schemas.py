from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TradeIn(BaseModel):
    trade_id: str = Field(min_length=1, max_length=64)
    version: int = Field(ge=1)
    counterparty_id: str = Field(min_length=1, max_length=64)
    portfolio_id: str = Field(min_length=1, max_length=64)
    maturity_date: date
    created_date: date | None = None


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_id: str
    version: int
    counterparty_id: str
    portfolio_id: str
    maturity_date: date
    created_date: date
    expired: bool


class TradeWriteResult(BaseModel):
    operation: str
    trade: TradeOut

