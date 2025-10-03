#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create a Django superuser non-interactively if environment variables are set
# This relies on DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL,
# and DJANGO_SUPERUSER_PASSWORD being set as environment variables on Render.
# The '|| true' ensures the build doesn't fail if the user already exists on subsequent deploys.
# if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
#     python manage.py createsuperuser --noinput || true
# else
#     echo "Warning: DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set. Admin user not created during build."
# fi

# REMOVED:
# - python apscheduler_runner.py (should be a separate worker process)
# - uvicorn ChatApi.asgi:application --host 0.0.0.0 --port 8001 --reload (should be your start command, not in build.sh)
# - python manage.py runserver (NEVER use in production)