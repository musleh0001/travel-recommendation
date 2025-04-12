#!/bin/sh

set -e

# Check if virtualenv is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is not active."
    exit 1
fi

echo "🚀 Applying migrations..."
python manage.py migrate --noinput


echo "🔥 Starting server..."
python manage.py runserver