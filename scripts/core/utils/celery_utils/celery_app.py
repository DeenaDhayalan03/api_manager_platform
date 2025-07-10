from celery import Celery
from scripts.constants.app_configuration import settings
from scripts.core.utils.celery_beat_utils.scheduler_config import CELERY_BEAT_SCHEDULE

celery_app = Celery(
    "api_management_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,
    worker_autoscale=settings.CELERY_WORKER_AUTOSCALE,
    task_acks_late=True,
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule=CELERY_BEAT_SCHEDULE
)
