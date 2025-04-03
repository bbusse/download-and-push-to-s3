# Stage 1: Build stage with full Python image to install dependencies
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies into a virtual environment
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root

# Copy the application code
COPY download-and-push-to-s3.py /app/

# Stage 2: Runtime stage with distroless Python image
FROM gcr.io/distroless/python3-debian11

# Set working directory
WORKDIR /app

# Copy virtual environment and application from builder
COPY --from=builder /app /app

# Set environment variables (can be overridden at runtime)
ENV FILE_URL=""
ENV S3_BUCKET=""
ENV S3_FILE_PATH=""

# Run the script
# Note: Distroless images use the venv's Python directly
CMD ["/app/.venv/bin/python", "/app/download-and-push-to-s3.py"]
