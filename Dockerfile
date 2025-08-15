FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install only essential packages for build, then remove later
RUN apk add --no-cache --virtual .build-deps \
        build-base \
        linux-headers \
        gcc \
        g++ \
        curl \
    && apk add --no-cache \
        libffi-dev \
        musl-dev \
        bash

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps  # remove build deps to shrink image

# Copy rest of the app (including app.py)
COPY . .

# Expose app port
EXPOSE 8000

# Run the app
CMD ["python", "app.py","--server.address=0.0.0.0","--server.port=8000"]
