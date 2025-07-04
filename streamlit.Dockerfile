FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY streamlit-requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r streamlit-requirements.txt

# Copy streamlit app
COPY streamlit_app.py .

# Expose port
EXPOSE 8501

# Run streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]