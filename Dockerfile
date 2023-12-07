FROM python:3.8-alpine

COPY . /app
WORKDIR /app

ARG APP_ENV=Production

RUN pip install -r requirments.txt
CMD gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app