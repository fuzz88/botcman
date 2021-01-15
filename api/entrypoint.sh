#!/bin/sh

echo "Starting app.py with $(python -V)..."

if [ "$DEBUG" = "1" ]

then

gunicorn --chdir /opt/app -b 0.0.0.0:8081 -k  uvicorn.workers.UvicornWorker --reload app:app

else

    if [ "$TEST" = "1"]

    then

    ./run_tests

    fi 

gunicorn --chdir /opt/app -b 0.0.0.0:8081 -k  uvicorn.workers.UvicornWorker -log-level warning app:app

fi
