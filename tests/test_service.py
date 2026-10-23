from datetime import date

from app.models import Trade
from app.schemas import TradeIn
from app.service import TradeService


def test_expiry_job_marks_only_surpassed_trades(session_factory):
    with session_factory() as session:
        session.add_all(
            [
                Trade(
                    trade_id="OLD",
                    version=1,
                    counterparty_id="CP-1",
                    portfolio_id="B1",
                    maturity_date=date(2024, 1, 1),
                    created_date=date(2023, 1, 1),
                    expired=False,
                ),
                Trade(
                    trade_id="TODAY",
                    version=1,
                    counterparty_id="CP-2",
                    portfolio_id="B1",
                    maturity_date=date(2025, 1, 1),
                    created_date=date(2024, 1, 1),
                    expired=False,
                ),
            ]
        )
        session.commit()
        service = TradeService(session, today=lambda: date(2025, 1, 1))

        assert service.expire_matured() == 1
        assert service.get("OLD").expired is True
        assert service.get("TODAY").expired is False
        assert [trade.trade_id for trade in service.list(include_expired=False)] == ["TODAY"]


def test_created_date_defaults_to_today(session_factory):
    with session_factory() as session:
        service = TradeService(session, today=lambda: date(2025, 1, 1))
        trade, operation = service.store(
            TradeIn(
                trade_id="T1",
                version=1,
                counterparty_id="CP-1",
                portfolio_id="B1",
                maturity_date=date(2025, 1, 1),
            )
        )
        assert operation == "created"
        assert trade.created_date == date(2025, 1, 1)

