web: gunicorn --pythonpath src srvup.wsgi
worker: ~ $ celery worker --workdir=src --app=srvup.celery:app --loglevel=INFO