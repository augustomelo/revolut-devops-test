FROM python:3.13-slim

RUN addgroup --system --gid 1000 revolut && \
    adduser --system --no-create-home --uid 1000 --gid 1000 app;

USER app:revolut

WORKDIR /src
ENV PATH="/src/.venv/bin:$PATH"

COPY --chown=app:revolut --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --chown=app:revolut ./uv.lock ./pyproject.toml /src
RUN uv sync --frozen --no-cache --no-dev;

COPY --chown=app:revolut ./app ./app

CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0", "--log-config", "/src/app/log_config.yaml"]
