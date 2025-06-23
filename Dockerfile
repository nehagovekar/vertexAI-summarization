# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies and upgrade pip
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ ./src/

# Create secrets directory (we'll mount the real secrets here)
RUN mkdir -p /app/secrets

# Expose port
EXPOSE 8000

# Set environment variables (will be overridden by mounted .env)
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]