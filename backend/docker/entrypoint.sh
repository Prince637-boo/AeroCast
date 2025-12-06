#!/usr/bin/env bash

set -e

echo "Starting container for service: $SERVICE_NAME"

# Apply database migrations
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
fi

# Start UVICORN
echo "Launching Uvicorn server..."
exec uvicorn "$SERVICE_NAME.main:app" \
    --host 0.0.0.0 \
    --port 8000 \
    --proxy-headers \
    --forwarded-allow-ips="*"
