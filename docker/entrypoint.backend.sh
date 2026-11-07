#!/bin/sh
set -e

echo "=== Bahavar Music Backend Startup ==="

# Wait for PostgreSQL if not using SQLite fallback
if [ "$USE_SQLITE" != "True" ] && [ "$USE_SQLITE" != "true" ] && [ "$USE_SQLITE" != "1" ]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
  while ! nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"; do
    sleep 1
  done
  echo "PostgreSQL is available and accepting connections."
fi

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static assets..."
python manage.py collectstatic --noinput || true

# Seed initial Bahavar data
echo "Seeding initial platform fixtures (seed_bahavar_data)..."
python manage.py seed_bahavar_data || true

echo "Starting Django server..."
exec "$@"
