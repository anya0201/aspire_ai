# ---- Build stage ----
FROM python:3.11-slim AS builder

WORKDIR /build

ARG PYTHON_REQUIREMENTS=requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt requirements-core.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Runtime stage ----
FROM python:3.11-slim

WORKDIR /app

# Runtime-only system deps (curl for healthcheck, docker CLI for sandbox)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN groupadd -r aspire && useradd -r -g aspire -d /app -s /sbin/nologin aspire \
    && mkdir -p /app/uploads && chown -R aspire:aspire /app

COPY --chown=aspire:aspire . .

USER aspire

EXPOSE 8000



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
