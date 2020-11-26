#!/bin/sh

echo "Starting app.py with $(python -V)..."
uvicorn --app-dir app/ app:app --workers 2 --log-level=warning --no-access-log
