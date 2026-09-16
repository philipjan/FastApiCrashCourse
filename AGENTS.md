# AGENTS.md

## Overview
FastAPI + Postgres learning project. The app and all routes live in the repo-root `main.py`. Pydantic I/O model: `src/FastApiCrashCourse/product/models.py` (`Product`). SQLAlchemy ORM model: `src/FastApiCrashCourse/product/database_models.py` (`Product`, imported into `main.py` as `OrmProduct`). DB wiring: `src/FastApiCrashCourse/database.py`. Env loading: `env_loader.py`.

## Commands
- Install deps: `uv sync`
- Run dev server (autoreload): `uv run fastapi dev main.py`
- Run uvicorn directly: `uv run uvicorn main:app --reload`

Always run from the repo root. There is no test, lint, or typecheck setup yet.

## Conventions / gotchas
- Package manager is `uv` (`uv.lock`); use `uv run ...`, not bare `python`/`pip`. Requires Python >= 3.12.
- Importing `main` instantiates `DBManager()`, which connects to Postgres and runs `create_all`, so a reachable database must exist before the app can start. `compose.yaml` is empty; no DB service is defined for you.
- `EnvLoader.initializeEnvs()` calls `load_dotenv()` and runs in `main.py` before `DBManager()`; `.env` builds `POSTGRES_BASE_URL` with `${VAR}` expansion.
- Schema is auto-created (`Base.metadata.create_all`) — there are no migrations. ORM models must be imported before `DBManager()` is instantiated or their tables are skipped, which is why `main.py` imports `database_models` before line 12.
- Never import from `main` inside `src/...` modules: `app`/`db_manager` are defined after `main.py`'s imports, so it causes circular imports. The SQLAlchemy `Base` lives in `database.py` for this reason; subclass it there.
- Two `Product` classes exist: the pydantic one (`models.py`) for request/response, and the ORM one (`database_models.py`, aliased `OrmProduct`) for queries. Keep them straight.
- Inject sessions with `Depends(db_manager.get_db_session)` — pass the function without `()` (it is a generator).
- `src/FastApiCrashCourse/product/endpoints.py` is an imported-nowhere stub; all working routes are in `main.py`. To add routes there, import the module from `main.py` only after `app` is defined.
- Imports mix repo-root names (`env_loader`, `main`) and `src.`-prefixed paths (`src.FastApiCrashCourse...`), so `main.py` must stay at the repo root.
- `.env` is tracked in git and contains real Postgres credentials; there is no `.gitignore`. Do not add secrets or commit `.env` changes.
