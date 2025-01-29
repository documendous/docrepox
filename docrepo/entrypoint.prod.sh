#!/bin/sh

# May be necessary to use sleep 10 when using Elastic search
# sleep 10

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear

# Uncomment for cache-busting (this is a hack until we can figure
# out how to serve STATIC_ROOT with nginx)
cp -rf /tmp/staticfiles/* /home/docrepo/web/staticfiles/.

# Uncomment for diagnostics
# python manage.py diffsettings --all

# Uncomment to use Elastic search indexing
# python manage.py search_index --rebuild -f

exec "$@"
