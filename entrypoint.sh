#!/bin/sh

export PYTHONPATH=/app/pdfapp
cd /app/pdfapp

echo "Running migrations..."
python manage.py migrate

echo "Setting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn pdfapp.wsgi:application --bind 0.0.0.0:8000
