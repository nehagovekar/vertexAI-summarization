# Use Python 3.11 slim image (lightweight version of Python)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Environment variables for Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies (gcc needed for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ ./src/
COPY .env ./

# Create secrets directory (we'll mount the real secrets here)
RUN mkdir -p secrets

# Tell Docker this container uses port 8000
EXPOSE 8000

# Health check - Docker will ping this to see if container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# The command to run when container starts
CMD ["python", "-m", "uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8000"]

