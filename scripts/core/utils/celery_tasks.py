from scripts.core.utils.endpoint_credits_utils import get_endpoint_credit
from scripts.core.utils.mongo_utils.user_utils import update_user_credits, get_user_by_tenant_id
from scripts.core.utils.mongo_utils.usage_log_utils import log_usage
from scripts.core.utils.mongo_utils.notification_utils import insert_or_update_low_credit_notification
from scripts.core.utils.mqtt_utils.mqtt_publish import publish_low_credit_alert, publish_credit_success
from scripts.core.utils.celery_utils.task_wrappers import BaseTaskWithRetry, log_task_execution
from scripts.core.utils.mongo_utils.summary_utils import generate_scheduled_summary
from scripts.core.utils.celery_utils.celery_app import celery_app


@celery_app.task(base=BaseTaskWithRetry, name="deduct_credits_task")
@log_task_execution
def deduct_credits_task(tenant_id: str, service: str, endpoint: str):
    endpoint_credit = get_endpoint_credit(service, endpoint)
    if not endpoint_credit:
        return {"skip": True, "reason": "No endpoint credit", "tenant_id": tenant_id}

    credits_required = endpoint_credit["credits"]
    user = get_user_by_tenant_id(tenant_id)
    if not user:
        return {"skip": True, "reason": "User not found", "tenant_id": tenant_id}

    current_credits = user.get("credits", 0)
    if current_credits < credits_required:
        return {"skip": True, "reason": "Insufficient credits", "tenant_id": tenant_id}

    new_credits = current_credits - credits_required
    update_user_credits(tenant_id, new_credits)

    return {
        "tenant_id": tenant_id,
        "username": user.get("username"),
        "service": service,
        "endpoint": endpoint,
        "credits_used": credits_required,
        "remaining_credits": new_credits,
    }


@celery_app.task(base=BaseTaskWithRetry, name="log_usage_task")
@log_task_execution
def log_usage_task(data: dict):
    if data.get("skip"):
        return data
    log_usage(data["tenant_id"], data["service"], data["endpoint"], data["credits_used"])
    return data


@celery_app.task(base=BaseTaskWithRetry, name="send_mqtt_alert_task")
@log_task_execution
def send_mqtt_alert_task(data: dict):
    if data.get("skip"):
        return data

    tenant_id = data["tenant_id"]
    username = data.get("username", "unknown")
    remaining_credits = data["remaining_credits"]

    if remaining_credits <= 100:
        warning_msg = f"Low credit alert: only {remaining_credits} credits left."
        publish_low_credit_alert(tenant_id, remaining_credits, message=warning_msg)
        insert_or_update_low_credit_notification(tenant_id, username, warning_msg)

    publish_credit_success(tenant_id, data["credits_used"])
    return data


@celery_app.task(base=BaseTaskWithRetry, name="scripts.core.utils.celery_tasks.generate_scheduled_summary_task")
@log_task_execution
def generate_scheduled_summary_task():
    print("[generate_scheduled_summary_task] Triggered by Celery Beat")
    generate_scheduled_summary()
