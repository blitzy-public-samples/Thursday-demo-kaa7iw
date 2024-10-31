# Human Tasks:
# 1. Ensure PostgreSQL connection string is configured in environment
# 2. Configure Google Cloud User Store credentials
# 3. Set up Redis connection parameters
# 4. Review and adjust Gunicorn worker configuration if needed
# 5. Configure monitoring and logging settings
# 6. Set up SSL certificates if needed

# Requirement: Technology Stack - Implements Python 3.9+ runtime environment
# Base image with Python 3.9
FROM python:3.9-slim

# Requirement: Production Deployment - Sets production environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Requirement: Containerization - Sets up working directory
WORKDIR /app

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# Requirement: Production Deployment - Installs production-grade dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Gunicorn port
# Requirement: Containerization - Exposes container port
EXPOSE 8000

# Configure health check
# Requirement: Production Deployment - Implements container health monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Start Gunicorn with production configuration
# Requirement: Production Deployment - Configures production-ready Gunicorn WSGI server
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "--capture-output", \
     "--enable-stdio-inheritance", \
     "wsgi:app"]