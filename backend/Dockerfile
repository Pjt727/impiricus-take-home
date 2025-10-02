FROM python:3.12-slim-bookworm 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# copy everyting for simplicity
# for production images my consider multi stage builds and removing sample data / other unused filies
COPY . .

# set up the database
# to persist the sqlite db you would need a docker volume, but the
# db in production is likely running on a separate server
RUN /bin/uv run -m db.manage migrate
RUN /bin/uv run -m db.manage load

EXPOSE 8000
CMD ["/bin/uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

