#!/bin/sh

# wait for MySQL server to start
sleep 10

cd /app

su -m app -c "python manage.py migrate"
su -m app -c "python manage.py collectstatic --noinput"
su -m app -c "gunicorn sis_biblioteca.wsgi -w 2 -b 0.0.0.0:8000"