web: bash -lc "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn plumix.wsgi:application --bind 0.0.0.0:$PORT"
