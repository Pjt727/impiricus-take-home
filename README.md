# Overview
Minimal fullstack app providing an interface to physician messages.
## Data
![db-diagram](assets/db-diagram.png)
## Running
## Frontend
- TypeScript
- Next.js with react (compiled with bun)
### dev
- `bun dev` 
- autoformatting (default options) done with [TypeScript Language Server](https://github.com/typescript-language-server/typescript-language-server)
## Backend
- Python
- FastAPI - backend framework
- SQLite - file based database
- SQLAlchemy (ORM) - interface with database
- pytest - testing framework
### dev
- `uv run -m db.manage migrate && uv run -m db.manage load` create database with initial data
    - uses `DB_URL` env variable which is set to "sqlite:///impiricus.db" by default
- `uv run uvicorn main:app --reload` run the backend with live watch
    - can navigate to /docs for interactive swagger docs
- `DB_URL="sqlite:///:memory:" uv run pytest` (bash/zsh) run the pytest suite
- autoformatting (default options) done with [ruff](https://docs.astral.sh/ruff/formatter/)



