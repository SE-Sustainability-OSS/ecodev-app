###########
# BUILDER #
###########
FROM python:3.13-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies (if any wheels need compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install packages
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN python3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########
FROM python:3.13-slim

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Switch to non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Copy application code as non-root
WORKDIR /app
COPY --chown=appuser:appuser app/ /app/app
ENV PYTHONPATH=/app

# Opened ports
EXPOSE 80

CMD ["uvicorn", "app.dash_app:server", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "300", "--ws-ping-timeout", "300" ]
