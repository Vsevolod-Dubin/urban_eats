#!/bin/sh

# wait-for-postgres.sh
echo "⏳ Waiting for PostgreSQL to become available at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL is up — executing command"
