from collections.abc import Callable
from datetime import date

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.exceptions import LowerVersionError, MaturedTradeError
from app.models import Trade
from app.schemas import TradeIn


class TradeService:
    def __init__(self, session: Session, today: Callable[[], date] = date.today):
        self.session = session
        self.today = today

    def store(self, payload: TradeIn) -> tuple[Trade, str]:
        today = self.today()
        if payload.maturity_date < today:
            raise MaturedTradeError(payload.maturity_date, today)

        # SELECT FOR UPDATE serializes competing updates on databases that support it.
        current = self.session.scalar(
            select(Trade).where(Trade.trade_id == payload.trade_id).with_for_update()
        )
        if current and payload.version < current.version:
            raise LowerVersionError(payload.trade_id, payload.version, current.version)

        values = payload.model_dump(exclude={"created_date"})
        values["created_date"] = payload.created_date or today
        values["expired"] = False

        if current:
            for name, value in values.items():
                setattr(current, name, value)
            trade, operation = current, "replaced"
        else:
            trade, operation = Trade(**values), "created"
            self.session.add(trade)

        self.session.commit()
        self.session.refresh(trade)
        return trade, operation

    def get(self, trade_id: str) -> Trade | None:
        return self.session.get(Trade, trade_id)

    def list(self, include_expired: bool = True) -> list[Trade]:
        statement = select(Trade).order_by(Trade.trade_id)
        if not include_expired:
            statement = statement.where(Trade.expired.is_(False))
        return list(self.session.scalars(statement))

    def delete(self, trade_id: str) -> bool:
        trade = self.get(trade_id)
        if trade is None:
            return False
        self.session.delete(trade)
        self.session.commit()
        return True

    def expire_matured(self) -> int:
        result = self.session.execute(
            update(Trade)
            .where(Trade.maturity_date < self.today(), Trade.expired.is_(False))
            .values(expired=True)
        )
        self.session.commit()
        return result.rowcount

