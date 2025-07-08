from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "generate-scheduled-summary": {
        "task": "scripts.core.utils.celery_tasks.generate_scheduled_summary_task",
        "schedule": crontab(minute="*/5"),
        "args": [],
    }
}
