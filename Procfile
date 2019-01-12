web: gunicorn tcc.wsgi:application --timeout 30 --keep-alive 15 --log-file -
worker: python ./manage.py rqworker high
