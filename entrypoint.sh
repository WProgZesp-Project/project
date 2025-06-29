#!/bin/sh

export PYTHONPATH=/app

echo "Running migrations..."
python /app/pdfapp/manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn pdfapp.wsgi:application --bind 0.0.0.0:8000
