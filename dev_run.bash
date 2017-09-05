#!/bin/bash
source tmp/venv/bin/activate
export DJANGO_SETTINGS_MODULE="group_builder.settings.dev"
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver
