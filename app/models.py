from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Trade(Base):
    __tablename__ = "trades"

    trade_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    counterparty_id: Mapped[str] = mapped_column(String(64), nullable=False)
    portfolio_id: Mapped[str] = mapped_column(String(64), nullable=False)
    maturity_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

