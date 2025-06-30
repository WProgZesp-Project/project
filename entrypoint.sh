#!/bin/sh

export PYTHONPATH=/app/pdfapp
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-pdfapp.settings.staging}

echo "Using settings module: $DJANGO_SETTINGS_MODULE"

echo "Running migrations..."
python /app/manage.py migrate

echo "Collecting static files..."
python /app/manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn pdfapp.wsgi:application --bind 0.0.0.0:8000
