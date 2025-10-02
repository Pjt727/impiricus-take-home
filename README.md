# Overview
Minimal fullstack app providing an interface to physician messages.
## Data
![db-diagram](assets/db-diagram.png)
## Running
## Frontend
- TypeScript
- Next.js with react (compiled with bun)
### dev
## Backend
- Python
- FastAPI - backend framework
- SQLite - file based database
- SQLAlchemy (ORM) - interface with database
- pytest - testing framework
### dev
- `uv run -m db.manage migrate && uv run -m db.manage load` create database with initial data
    - uses `DB_URL` env variable which is set to "sqlite:///impiricus.db" by default
- `uv run uvicorn main:app --reload`
    - can navigate to /docs for interactive swagger docs
- autoformatting (default options) done with [ruff](https://docs.astral.sh/ruff/formatter/)



