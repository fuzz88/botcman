#!/bin/sh

echo "Starting app.py with $(python -V)..."
# uvicorn --app-dir /opt/app --env-file /opt/app/.env app:app --workers 2 --host 0.0.0.0 --port 8081 --log-level=warning --no-access-log $RELOAD
if [ "$DEBUG" = "1" ]

then

gunicorn --chdir /opt/app -b 0.0.0.0:8081 -k  uvicorn.workers.UvicornWorker --reload app:app

else

gunicorn --chdir /opt/app -w 4 -b 0.0.0.0:8081 -k  uvicorn.workers.UvicornWorker -log-level warning app:app

fi