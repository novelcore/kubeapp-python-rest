# syntax=docker/dockerfile:1

# --- Build stage ---
FROM python:3.12-alpine AS builder

WORKDIR /app

# Build deps needed for packages that may compile from source (fallback)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Install Poetry
RUN pip install --no-cache-dir poetry==2.1.3

# Prefer pre-built binary wheels (grpcio, cryptography ship musllinux wheels)
ENV PIP_PREFER_BINARY=1

# Copy dependency manifests
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install deps into an in-project virtualenv
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install --no-interaction --no-cache --only main --no-root

# --- Runtime stage ---
FROM python:3.12-alpine

WORKDIR /app

# Non-root user
RUN adduser -D -u 1000 appuser

# Copy the virtualenv from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY app/ /app/app/

RUN chown -R appuser:appuser /app

USER appuser

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["python", "-m", "app.main"]
