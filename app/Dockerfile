# syntax=docker/dockerfile:1

# Development stage for Poetry installation and dependency management
FROM cgr.dev/chainguard/python:latest-dev AS poetry-base

# Switch to root to install required build dependencies
USER root

# Install necessary dependencies for building C extensions
RUN apk add --no-cache \
    build-base \
    libffi \
    libffi-dev \
    pkgconf \
    gcc \
    curl

# Create nonroot user's home directory and set ownership
RUN mkdir -p /home/nonroot && \
    chown -R nonroot:nonroot /home/nonroot

# Switch to nonroot user for Rust installation
USER nonroot
WORKDIR /home/nonroot

# Install Rust for nonroot user
ENV RUSTUP_HOME=/home/nonroot/.rustup
ENV CARGO_HOME=/home/nonroot/.cargo
ENV PATH="/home/nonroot/.cargo/bin:${PATH}"

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    source /home/nonroot/.cargo/env

# Set up Poetry environment
ENV POETRY_VERSION=2.1.3
ENV POETRY_HOME=/home/nonroot/.poetry
ENV POETRY_VENV=/home/nonroot/.poetry-venv
ENV POETRY_CACHE_DIR=/home/nonroot/.cache
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Poetry
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools wheel \
    && $POETRY_VENV/bin/pip install "poetry==${POETRY_VERSION}"

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy Poetry configuration files
COPY --chown=nonroot:nonroot pyproject.toml poetry.lock ./

# Create a dummy README.md if not present
RUN touch README.md

# Create and activate virtual environment
RUN python -m venv .venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Pre-install and build wheels for critical dependencies
RUN mkdir -p /home/nonroot/wheels && \
    pip install --no-cache-dir \
    cffi==1.17.1 \
    wheel \
    setuptools

# Configure poetry
RUN poetry config installer.max-workers 1 && \
    poetry config virtualenvs.create false

# Prefer pre-built binary wheels over source builds.
# pydantic-core and grpcio ship cp314 wheels; without this they fall back to
# source compilation which fails against the bundled PyO3 / GCC 15 in the image.
ENV PIP_PREFER_BINARY=1

# Install project dependencies
RUN poetry install --no-interaction --no-cache --only main --no-root

# Production stage
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

# Copy the virtual environment from poetry-base
COPY --from=poetry-base /app/.venv /app/.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy application code
COPY app/ /app/app

# Set Python runtime environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the application port
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["python"]
CMD ["-m", "app.main"]