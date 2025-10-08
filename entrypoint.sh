#!/bin/bash
set -e

# Default DB host
#DB_HOST=${DOCKER_DB_HOST:-postgres_db}
DB_HOST=${DOCKER_DB_HOST:-172.19.0.2}

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL at $DB_HOST..."
while ! pg_isready -h "$DB_HOST" -U "$DOCKER_DB_USER" > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is up!"

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn server
exec gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8020
