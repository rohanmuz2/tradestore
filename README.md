# Trade Store API

A Python REST API that retains the latest version of each trade in a SQL database.

## Business rules

- A lower incoming version is rejected with HTTP `409`; the same or a higher version replaces the record.
- A trade whose maturity date is earlier than today is rejected with HTTP `422`.
- A background worker marks stored trades expired after their maturity date is surpassed.
- Version comparison and replacement happen in one database transaction. For a high-volume production deployment, configure `DATABASE_URL` for a database with row-level locking such as PostgreSQL.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive OpenAPI documentation. SQLite is used by default. Configuration:

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./trades.db` | SQLAlchemy database URL |
| `EXPIRY_SCAN_SECONDS` | `60` | Background expiry interval |

Example:

```bash
curl -X POST http://localhost:8000/trades -H "Content-Type: application/json" -d '{
  "trade_id": "T1",
  "version": 1,
  "counterparty_id": "CP-1",
  "portfolio_id": "B1",
  "maturity_date": "2099-05-20"
}'
```

## Test and package

```bash
pytest
ruff check .
docker build -t trade-store .
```

The tests express each acceptance rule and enforce at least 90% coverage. The GitHub Actions pipeline runs linting and regression tests, scans open-source dependencies with Trivy, fails on critical vulnerabilities, then publishes the container to GitHub Container Registry on successful pushes to `main`.

The PlantUML sequence/design diagram is in [`docs/design.puml`](docs/design.puml).
