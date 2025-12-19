FROM python:3.11-slim

# Prevent python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Don't buffer stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for some packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Default envs (override at runtime or via docker-compose)
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

EXPOSE 5000

# Run with gunicorn for production-like environment
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
