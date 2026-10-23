from datetime import date


class LowerVersionError(Exception):
    def __init__(self, trade_id: str, received: int, current: int):
        self.trade_id = trade_id
        self.received = received
        self.current = current
        super().__init__(f"Trade {trade_id} version {received} is below current version {current}")


class MaturedTradeError(Exception):
    def __init__(self, maturity_date: date, today: date):
        self.maturity_date = maturity_date
        self.today = today
        super().__init__(f"Maturity date {maturity_date} is earlier than today {today}")

