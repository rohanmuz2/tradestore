# Product Requirements Document: Trade Store API

**Version:** 1.0  
**Status:** Implemented  
**Audience:** Engineering interviewers, developers, QA engineers, and DevOps reviewers

## 1. Executive summary

The Trade Store API receives trades from one or more transmission channels and keeps the latest accepted version of every trade. It protects the store from stale updates, rejects trades that are already matured, and automatically marks stored trades as expired after maturity.

The implementation is a Python REST service built with FastAPI and SQLAlchemy. SQLite provides a zero-configuration local database; the database URL is configurable so a production deployment can use PostgreSQL or another supported SQL database. Automated tests, code-quality checks, vulnerability scanning, container packaging, and GitHub Actions provide a repeatable delivery process.

## 2. Problem statement

A trade platform may receive thousands of trade messages in an unpredictable order. Messages for the same trade can carry different versions, including duplicate or stale versions. Without validation, an older message could overwrite a newer trade and corrupt the current state.

The system must provide one authoritative current record per trade while applying the following rules:

1. Reject an incoming version lower than the stored version.
2. Replace the stored record when the incoming version is the same or higher.
3. Reject a new message when its maturity date is earlier than the processing date.
4. Mark stored trades expired after their maturity date has passed.

## 3. Goals and non-goals

### Goals

- Expose a clear REST interface for creating, replacing, reading, listing, and deleting trades.
- Enforce the trade rules in a reusable service layer rather than only at the HTTP boundary.
- Persist data in a relational database.
- Provide deterministic error responses for invalid business operations.
- Automatically update the expiry flag without requiring a client request.
- Demonstrate TDD through acceptance-focused unit and API tests.
- Automate regression tests, linting, vulnerability scanning, and container publication.
- Remain easy to run locally and straightforward to migrate to a production database.

### Non-goals for this version

- Maintaining the complete historical record of every trade version.
- Authenticating clients or implementing role-based access control.
- Consuming directly from Kafka, RabbitMQ, or another message broker.
- Multi-region replication or disaster recovery.
- Providing a user interface.
- Deploying the container to a specific cloud runtime. The current pipeline publishes a deployable image to GitHub Container Registry.

## 4. Users and use cases

| User or system | Need |
|---|---|
| Upstream trade producer | Submit new trades and version updates safely |
| Operations service | Query the current state of a trade |
| Portfolio service | List active or all trades |
| Operations engineer | Check service health and inspect API documentation |
| Developer or reviewer | Run regression tests and reproduce the build locally |

Primary flow:

1. An upstream producer sends a trade to `POST /trades`.
2. The API validates the payload shape.
3. The service compares the maturity date and stored version in a database transaction.
4. The trade is inserted, replaced, or rejected.
5. A background worker periodically marks surpassed trades expired.

## 5. Functional requirements

| ID | Requirement | Expected result |
|---|---|---|
| FR-01 | Store a previously unseen trade | HTTP `201`, operation `created` |
| FR-02 | Receive the same version again | Existing record replaced; HTTP `200` |
| FR-03 | Receive a higher version | Existing record replaced; HTTP `200` |
| FR-04 | Receive a lower version | No mutation; HTTP `409` with current version |
| FR-05 | Receive a maturity date before today | No mutation; HTTP `422` |
| FR-06 | Receive a maturity date equal to today | Trade accepted and not immediately expired |
| FR-07 | Maturity date becomes earlier than today | Background worker sets `expired=true` |
| FR-08 | Retrieve one trade | HTTP `200`, or `404` if absent |
| FR-09 | List trades | Return records ordered by trade ID |
| FR-10 | Filter out expired trades | `include_expired=false` returns active records only |
| FR-11 | Delete a trade | HTTP `204`, or `404` if absent |
| FR-12 | Check service health | `GET /health` returns `{"status":"ok"}` |

## 6. Trade data model

| Field | Type | Constraints and meaning |
|---|---|---|
| `trade_id` | String | Required, unique identifier, maximum 64 characters |
| `version` | Integer | Required, minimum 1 |
| `counterparty_id` | String | Required, maximum 64 characters |
| `portfolio_id` | String | Required, maximum 64 characters |
| `maturity_date` | Date | Required, must not be before the processing date on ingestion |
| `created_date` | Date | Optional input; defaults to the processing date |
| `expired` | Boolean | System-managed; initially false and later updated by the expiry worker |

`trade_id` is the database primary key because this version stores only the current state of each trade. The version remains a business field used for ordering updates.

## 7. API contract

### Create or replace a trade

`POST /trades`

```json
{
  "trade_id": "T2",
  "version": 2,
  "counterparty_id": "CP-2",
  "portfolio_id": "B1",
  "maturity_date": "2099-05-20"
}
```

Successful response:

```json
{
  "operation": "created",
  "trade": {
    "trade_id": "T2",
    "version": 2,
    "counterparty_id": "CP-2",
    "portfolio_id": "B1",
    "maturity_date": "2099-05-20",
    "created_date": "2026-10-23",
    "expired": false
  }
}
```

The example date illustrates the response structure. At runtime, an omitted `created_date` uses the server's current date.

### Read operations

- `GET /trades/{trade_id}` retrieves one trade.
- `GET /trades` retrieves all current trade records.
- `GET /trades?include_expired=false` retrieves active records only.
- `GET /health` reports process health.

### Delete operation

- `DELETE /trades/{trade_id}` deletes a record and returns HTTP `204`.

### Error semantics

| Status | Meaning |
|---|---|
| `404 Not Found` | Requested trade does not exist |
| `409 Conflict` | Incoming version is lower than the current version |
| `422 Unprocessable Entity` | Invalid request data or maturity date in the past |

FastAPI publishes the full machine-readable OpenAPI contract at `/openapi.json` and interactive documentation at `/docs`.

## 8. Architecture and processing design

The implementation separates responsibilities into four layers:

1. **API layer:** FastAPI routes, dependency injection, status codes, and exception mapping.
2. **Schema layer:** Pydantic request and response validation.
3. **Service layer:** Version, maturity, replacement, deletion, and expiry rules.
4. **Persistence layer:** SQLAlchemy models, sessions, and database engine configuration.

The application startup creates the schema and launches an asynchronous expiry loop. Each interval, the loop opens its own database session and performs one set-based update for all newly matured trades.

The write path uses a transaction and requests a row lock with `SELECT ... FOR UPDATE`. SQLite is suitable for local development and evaluation. A production system handling concurrent writers across multiple application instances should use PostgreSQL with row-level locking and an appropriate isolation strategy. A distributed scheduler or database job should replace the in-process expiry worker when multiple replicas are deployed.

## 9. TDD and verification strategy

The tests encode business behavior before it is treated as complete. They operate at two levels:

- **API tests** verify request validation, HTTP status codes, create/replace behavior, lower-version rejection, maturity rejection, filtering, deletion, not-found behavior, and health checks.
- **Service tests** inject a fixed date to verify the expiry boundary and default created date without depending on the wall clock.

The test database is an isolated in-memory SQLite instance. FastAPI's database dependency is replaced during each test, so test execution cannot modify the development database.

Quality gates:

- All regression tests must pass.
- Application coverage must remain at or above 90%.
- Ruff lint checks must pass.
- Trivy must find no critical (blocker-equivalent) open-source vulnerabilities.
- Container publication runs only after tests and the vulnerability gate pass.

Current verified result: 9 tests pass with approximately 97.6% application coverage.

## 10. CI/CD and security

The GitHub Actions workflow runs for pushes and pull requests targeting `main`:

1. Check out the exact source revision.
2. Install pinned runtime and development dependencies.
3. Run Ruff static checks.
4. Run the complete Pytest regression suite and coverage gate.
5. Scan the filesystem and Python dependency declarations with Trivy.
6. Fail the workflow when a critical vulnerability is detected.
7. On a successful push to `main`, build the Docker image and publish it as `ghcr.io/<owner>/<repository>:latest`.

Publishing an immutable commit-SHA image tag and deploying to a managed runtime would be the next production-hardening step.

## 11. Non-functional requirements

| Area | Requirement or approach |
|---|---|
| Correctness | Business rules isolated in a tested service layer |
| Performance | Set-based expiry update; indexes on maturity and expired fields |
| Consistency | Version validation and update occur in one transaction |
| Scalability | Stateless HTTP layer; external SQL database supported through configuration |
| Maintainability | Typed schemas, small modules, documented endpoints, automated linting |
| Portability | Docker image and environment-driven configuration |
| Security | Input validation, non-root container user, pinned direct dependencies, critical vulnerability gate |
| Observability | Health endpoint; structured logging and metrics are recommended next steps |

## 12. Acceptance criteria traceability

| Acceptance criterion | Implementation | Test evidence |
|---|---|---|
| Lower versions are rejected | `TradeService.store` raises `LowerVersionError` | `test_lower_version_is_rejected` |
| Same versions replace | Service updates the existing entity | `test_same_version_replaces_trade` |
| Higher versions replace | Service updates version and values | `test_higher_version_replaces_trade` |
| Past maturity is rejected | `MaturedTradeError` before database mutation | `test_past_maturity_is_rejected` |
| Surpassed trades expire | Set-based `expire_matured` update | `test_expiry_job_marks_only_surpassed_trades` |
| Regression automation | Pytest job in GitHub Actions | `.github/workflows/ci-cd.yml` |
| Critical OSS findings fail build | Trivy `severity: CRITICAL`, `exit-code: 1` | CI vulnerability-scan job |

## 13. Risks, decisions, and trade-offs

- **Current-state storage:** Keeping only one row per trade makes reads simple and fast, but does not provide an audit trail. A production design may add an immutable `trade_versions` table or publish accepted events.
- **In-process scheduler:** It is simple and sufficient for one instance. Multiple replicas could run the same job; the update is idempotent, but a dedicated scheduler is operationally cleaner.
- **SQLite default:** It removes setup friction for reviewers, but PostgreSQL is recommended for concurrent production workloads.
- **Date rather than timestamp:** The requirements use business dates. If trading cut-offs depend on market timezone or time of day, use timezone-aware timestamps and an explicit business calendar.
- **Delete endpoint:** It completes the REST lifecycle for this exercise. Regulated production systems commonly prefer soft deletion and audit retention.

## 14. Future roadmap

1. Add PostgreSQL and database migrations with Alembic.
2. Add idempotency keys and optimistic concurrency or serializable transaction handling.
3. Consume trade events from Kafka while retaining the REST ingestion option.
4. Store immutable trade-version history and audit metadata.
5. Add authentication, authorization, rate limits, and request-size limits.
6. Add JSON logs, metrics, tracing, readiness checks, and alerting.
7. Publish immutable image tags and deploy to Kubernetes, ECS, Cloud Run, or Azure Container Apps.
8. Add load, concurrency, contract, and integration tests using a real PostgreSQL service.

## 15. Interview walkthrough

A concise demonstration can follow this order:

1. State the core risk: out-of-order messages must not overwrite newer trade state.
2. Show `TradeService.store` and explain why the rule belongs outside the HTTP route.
3. Run the tests and point out the fixed-date expiry boundary test.
4. Open `/docs` and submit a valid trade, a same-version replacement, and a lower version.
5. Walk through the sequence, class, component, ER, and pipeline diagrams.
6. Explain why SQLite was selected for easy review and PostgreSQL is recommended for production concurrency.
7. Show the CI gates and explain that image publication depends on both regression and security success.
8. Close with production improvements: migrations, historical versions, authentication, observability, and load testing.

## 16. Supporting diagrams

- [`design.puml`](design.puml) — ingestion and expiry sequence
- [`architecture.puml`](architecture.puml) — runtime component architecture
- [`class-diagram.puml`](class-diagram.puml) — code-level class relationships
- [`data-model.puml`](data-model.puml) — database entity model
- [`ci-cd.puml`](ci-cd.puml) — delivery and security gates

