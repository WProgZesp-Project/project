#!/bin/sh

# Czekaj aż baza danych będzie dostępna (opcjonalnie)
# np. za pomocą wait-for-it.sh albo podobnego skryptu

echo "Uruchamianie migracji bazy danych..."
python manage.py migrate

echo "Zbieranie statycznych plików..."
python manage.py collectstatic --noinput

echo "Uruchamianie serwera..."
exec "$@"
