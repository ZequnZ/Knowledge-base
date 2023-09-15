# Multi-stage build
FROM python:3.10.6-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry dependency files to container
COPY pyproject.toml poetry.lock /app/

# Install dependency
RUN poetry config virtualenvs.in-project true && \
    poetry install -vvv --no-root --only=main && \
    rm -rf $POETRY_CACHE_DIR

FROM base as final

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:${PATH}" \
    PYTHONPATH="/app/src/"

# Copy your code into container. e.g.:
COPY /src /app

# Copy installed Python dependencies to final container
COPY --from=builder /app/.venv ${VIRTUAL_ENV}

# Keep the container running
# CMD tail -f /dev/null

# Replace your enterpoint here. e.g:
ENTRYPOINT ["python", "-m", "main"]
