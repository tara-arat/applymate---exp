# Dockerfile - Modern multi-stage build for ApplyMate
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/database data/profiles data/uploads data/logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "ui/app.py", "--server.address", "0.0.0.0"]


# Development stage with additional tools
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest>=8.0.0 \
    pytest-asyncio>=0.23.0 \
    pytest-cov>=4.1.0 \
    ruff>=0.2.0 \
    mypy>=1.8.0 \
    ipython>=8.20.0

# Enable hot-reload for Streamlit
CMD ["streamlit", "run", "ui/app.py", "--server.address", "0.0.0.0", "--server.runOnSave", "true"]
