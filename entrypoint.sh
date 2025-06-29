#!/bin/sh

echo "Running migrations..."
python pdfapp/manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn pdfapp.wsgi:application --bind 0.0.0.0:8000
