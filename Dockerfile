FROM python:3.12-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base \
    python3-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python pdfapp/manage.py migrate --noinput
RUN python pdfapp/manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "pdfapp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]