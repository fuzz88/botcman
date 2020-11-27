#!/bin/sh

echo "Starting app.py with $(python -V)..."
uvicorn --app-dir /opt/app --env-file /opt/app/.env app:app --workers 2 --host 0.0.0.0 --port 8081 --log-level=warning --no-access-log $RELOAD
