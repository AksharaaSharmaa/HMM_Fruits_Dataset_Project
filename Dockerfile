FROM python:3.11-slim

# Install eSpeak NG and required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    espeak-ng \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY index.html .

# Expose port (Render will use PORT env variable)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/api/health')"

# Run the application
# Use $PORT environment variable for Render compatibility
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8001}
