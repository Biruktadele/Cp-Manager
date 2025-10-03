#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Run gunicorn
python apscheduler_runner.py
# uvicorn ChatApi.asgi:application --host 0.0.0.0 --port 8001 --reload
python manage.py runserver