# Multi-stage Dockerfile for E-commerce Backend
# Python 3.11 with optimizations, security, and health checks

# =============================================================================
# Stage 1: Base Image with Dependencies
# =============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# =============================================================================
# Stage 2: Development Dependencies
# =============================================================================
FROM base as development

# Install development dependencies
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /tmp/requirements.txt
COPY requirements-test.txt /tmp/requirements-test.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/requirements-test.txt

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Development command
CMD ["uvicorn", "main_clean.py:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =============================================================================
# Stage 3: Production Dependencies
# =============================================================================
FROM base as production-deps

# Copy requirements
COPY requirements.txt /tmp/requirements.txt

# Install only production dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# =============================================================================
# Stage 4: Production Image
# =============================================================================
FROM python:3.11-alpine as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install runtime dependencies
RUN apk add --no-cache \
    libpq \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G appuser appuser

# Copy Python dependencies from production-deps stage
COPY --from=production-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=production-deps /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["uvicorn", "main_clean.py:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# =============================================================================
# Stage 5: Testing Image
# =============================================================================
FROM development as testing

# Install additional testing dependencies
RUN pip install pytest-cov pytest-xdist

# Set working directory
WORKDIR /app

# Copy test files
COPY tests/ /app/tests/
COPY examples/ /app/examples/

# Run tests
CMD ["python", "-m", "pytest", "tests/", "-v", "--cov=src", "--cov-report=html"]
