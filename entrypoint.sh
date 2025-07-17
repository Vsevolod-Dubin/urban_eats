#!/bin/sh

echo "⏳ Waiting for the database to become available..."
export DB_HOST=db
export DB_PORT=5432
./wait-for-postgres.sh

echo "📦 Applying database migrations..."
python urban_eats/manage.py migrate

echo "🔍 Checking if initial data should be loaded..."
python urban_eats/manage.py shell -c "
from menu.models import Dish;
import sys;
exit(0) if Dish.objects.exists() else exit(1)
"

if [ $? -ne 0 ]; then
  echo "📂 Loading initial data from fixtures..."
  python urban_eats/manage.py loaddata fixtures
else
  echo "✅ Data already exists, skipping fixtures."
fi

echo "🧱 Collecting static files..."
python urban_eats/manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
gunicorn urban_eats.wsgi:application --bind 0.0.0.0:8000

