import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./trades.db")
    expiry_scan_seconds: float = float(os.getenv("EXPIRY_SCAN_SECONDS", "60"))


settings = Settings()

