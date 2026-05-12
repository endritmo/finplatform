#!/bin/sh
set -e

echo "========================================"
echo " FinPlatform Backend — Starting up"
echo "========================================"

echo "[1/5] Running database migrations..."
python manage.py migrate --noinput

echo "[2/5] Collecting static files..."
python manage.py collectstatic --noinput

echo "[3/5] Creating superuser if not exists..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SUPERUSER_USERNAME'],
        os.environ['DJANGO_SUPERUSER_EMAIL'],
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

echo "[4/5] Seeding forum categories..."
python manage.py shell -c "
from forum.models import Category
Category.objects.get_or_create(name='Bitcoin', slug='bitcoin')
Category.objects.get_or_create(name='Ethereum', slug='ethereum')
Category.objects.get_or_create(name='Forex', slug='forex')
Category.objects.get_or_create(name='Stocks', slug='stocks')
Category.objects.get_or_create(name='Commodities', slug='commodities')
print('Categories seeded.')
"

echo "[5/5] Starting Gunicorn..."
exec gunicorn finproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -