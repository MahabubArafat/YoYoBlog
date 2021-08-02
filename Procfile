web: flask db upgrade; gunicorn microblog:app
worker: rq worker -u $REDIS_URL microblog-tasks