#!/bin/sh

if [ "$DATABASE" = "postgres" ] 
then
  echo "Connecting to postgres database..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "Database is running"
fi

echo "Making migrations"
python manage.py makemigrations
echo "Applying migrations"
python manage.py migrate

# Loads the data
# - runs after migrations to ensure
#   - the database schema is up to date
#   - the required tables exist
python manage.py load_tweets

exec "$@"