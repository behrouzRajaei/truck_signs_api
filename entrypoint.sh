#!/usr/bin/env bash
set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL to be ready
while ! nc -z $DOCKER_DB_HOST $DOCKER_DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL is ready"

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

echo "Starting Gunicorn..."
# Start Gunicorn server on port 8020
exec gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8020
