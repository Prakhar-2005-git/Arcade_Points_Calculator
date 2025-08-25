#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Make database migrations
python manage.py makemigrations

# Apply database migrations
python manage.py migrate
