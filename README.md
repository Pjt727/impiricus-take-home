# Overview
Minimal fullstack app providing an interface to physician messages.
## Data
![db-diagram](assets/db-diagram.png)
## Running
- Frontend/ Backend each have their own own DockerFile
### Docker compose
- Run the `docker-compose.yml` which will orchestrate both the frontend and backend ports 3000 and 8000 need to be open
    - `docker-compose up`
### Docker
- Running Backend example (CWD backend):
    - `docker build -t impiricus-backend .`
    - `docker run -p 8000:8000 impiricus-backend:latest`
- Running Frontend example (CWD frontend):
    - `docker build -t impiricus-frontend .`
    - `docker run -p 3000:3000 impiricus-frontend:latest`

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



