from celery import Task
import logging

logger = logging.getLogger(__name__)

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 5}
    retry_backoff = True
    retry_jitter = True
    acks_late = True


def log_task_execution(func):

    def wrapper(*args, **kwargs):
        logger.info(f"Starting task: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Finished task: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in task {func.__name__}: {str(e)}")
            raise
    return wrapper