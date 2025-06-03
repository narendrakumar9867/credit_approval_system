# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apt-get update \
  && apt-get install -y gcc libpq-dev \
  && pip install --upgrade pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /myapp

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY backend/. ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]