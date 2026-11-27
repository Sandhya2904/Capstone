# Capstone

# NetPulse

A layered FastAPI device-monitoring API with an in-memory repository and optional MySQL/Alembic persistence.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/openapi.json`.

## Tests

```bash
python -m pytest -q
```

## In-memory baseline

The default `NETPULSE_STORAGE=memory` repository is shared across requests and resets on server restart.

1. POST `/devices` with a device payload.
2. PATCH `/devices/{device_id}/status` to `offline` twice.
3. GET `/alerts`; the first transition creates one alert and the second creates none.

## MySQL and Alembic

Copy `.env.example` to `.env`, create the MySQL database and user, set `NETPULSE_STORAGE=mysql`, then run:

```bash
alembic upgrade head
alembic current
alembic downgrade -1
alembic upgrade head
```

Restart uvicorn after setting MySQL mode. The service and routes are unchanged by repository selection.

## Architecture

- Routes translate domain exceptions to HTTP responses.
- The service owns registration and online-to-offline business rules.
- The in-memory or MySQL repository owns persistence.
- The event module creates offline alerts.
- Alembic owns database schema evolution.
