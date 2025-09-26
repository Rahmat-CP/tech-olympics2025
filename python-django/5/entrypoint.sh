#!/bin/bash

python manage.py migrate
python manage.py flush --noinput
python manage.py collectstatic --noinput --clear

celery -A core worker -l info &  
celery -A core beat -l info &

exec "$@"
