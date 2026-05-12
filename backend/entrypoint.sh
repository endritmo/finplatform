#!/bin/sh
set -e

echo "========================================"
echo " FinPlatform Backend — Starting up"
echo "========================================"

echo "[1/3] Running database migrations..."
python manage.py migrate --noinput

echo "[2/3] Collecting static files..."
python manage.py collectstatic --noinput

echo "[3/3] Starting Gunicorn (2 workers - Render 512MB limit)..."
exec gunicorn finproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
