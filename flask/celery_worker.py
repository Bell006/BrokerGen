
from app.tasks import celery_app


# celery -A celery_worker.celery_app worker --loglevel=info