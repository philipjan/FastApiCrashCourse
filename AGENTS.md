# AGENTS.md

## Overview
A small FastAPI learning project. The FastAPI `app` and all routes live in the repo-root `main.py`; the `Product` pydantic model is in `src/FastApiCrashCourse/product/models.py`.

## Commands
- Install deps: `uv sync`
- Run dev server (autoreload): `uv run fastapi dev main.py`
- Run uvicorn directly: `uv run uvicorn main:app --reload`

Always run from the repo root. There is no test, lint, or typecheck setup yet.

## Conventions / gotchas
- Package manager is `uv` (`uv.lock`); use `uv run ...`, not bare `python`/`pip`.
- Requires Python >= 3.12.
- Routes are defined in `main.py` but the pattern is to import the app and decorate at module import time (`from main import app`), so a new endpoint module only takes effect once it is imported (e.g. from `main.py`). `src/FastApiCrashCourse/product/endpoints.py` currently contains only imports and is imported nowhere, so it registers nothing.
- Imports mix a repo-root import (`from main import app`) and a `src.`-prefixed import (`from src.FastApiCrashCourse...`), so `main.py` must stay at the repo root.
- State is an in-memory module-level `CURRENT_PRODUCTS` list seeded at import time; it is not persisted and resets on every restart.
- Known bug in `add_product` (`main.py`): the "update existing" branch does `CURRENT_PRODUCTS[product.id] = product`, indexing the list by product id instead of `.append`/index lookup, so it can raise and return 500.
- `price`/`quantity` in the `Product` model are required; `.env` exists but is empty and nothing loads it beyond `python-dotenv` being installed.
