import asyncio
from contextlib import asynccontextmanager, suppress
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, SessionLocal, engine, get_session
from app.exceptions import LowerVersionError, MaturedTradeError
from app.schemas import TradeIn, TradeOut, TradeWriteResult
from app.service import TradeService


async def expiry_worker() -> None:
    while True:
        await asyncio.sleep(settings.expiry_scan_seconds)
        with SessionLocal() as session:
            TradeService(session).expire_matured()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    worker = asyncio.create_task(expiry_worker())
    yield
    worker.cancel()
    with suppress(asyncio.CancelledError):
        await worker


app = FastAPI(
    title="Trade Store API",
    version="1.0.0",
    description="Stores only the latest version of each trade and expires matured trades.",
    lifespan=lifespan,
)


@app.exception_handler(LowerVersionError)
async def lower_version_handler(_, exc: LowerVersionError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc), "current_version": exc.current},
    )


@app.exception_handler(MaturedTradeError)
async def matured_trade_handler(_, exc: MaturedTradeError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok"}


@app.post("/trades", response_model=TradeWriteResult, status_code=status.HTTP_201_CREATED)
def store_trade(
    payload: TradeIn,
    response: Response,
    session: Annotated[Session, Depends(get_session)],
):
    trade, operation = TradeService(session).store(payload)
    if operation == "replaced":
        response.status_code = status.HTTP_200_OK
    return {"operation": operation, "trade": trade}


@app.get("/trades", response_model=list[TradeOut])
def list_trades(
    session: Annotated[Session, Depends(get_session)],
    include_expired: bool = Query(default=True),
):
    return TradeService(session).list(include_expired)


@app.get("/trades/{trade_id}", response_model=TradeOut)
def get_trade(trade_id: str, session: Annotated[Session, Depends(get_session)]):
    trade = TradeService(session).get(trade_id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@app.delete("/trades/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trade(trade_id: str, session: Annotated[Session, Depends(get_session)]):
    if not TradeService(session).delete(trade_id):
        raise HTTPException(status_code=404, detail="Trade not found")

