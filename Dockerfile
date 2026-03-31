# Default simple OpenEnv API Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy the core environment files
COPY pyproject.toml .
COPY README.md .
COPY openenv.yaml .

# Copy source code directories
COPY server/ ./server/
COPY models.py .
COPY client.py .
COPY __init__.py .
COPY data/ ./data/

# Install the package itself (reads pyproject.toml)
RUN pip install --no-cache-dir -e .

# Expose the standard OpenEnv port
EXPOSE 8000

# Run the FastAPI server via Uvicorn
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
