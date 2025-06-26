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

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application - CORRECTED PATH
CMD ["sh", "-c", "uvicorn src.server.main:app --host 0.0.0.0 --port ${PORT:-8000}"]