from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
import requests
import asyncio

from scripts.core.utils.jwt_utils.jwt_handler import get_current_user
from scripts.core.utils.mongo_utils.service_utils import get_service_by_name
from scripts.core.utils.endpoint_credits_utils import get_endpoint_credit
from scripts.core.utils.mongo_utils.usage_log_utils import log_usage
from scripts.core.utils.mongo_utils.user_utils import get_user_by_tenant_id
from scripts.core.utils.mongo_utils.notification_utils import (
    insert_or_update_low_credit_notification,
    update_low_credit_notification_to_insufficient
)
from scripts.core.utils.mqtt_utils.mqtt_publish import publish_low_credit_alert
from celery import chain
from scripts.core.utils.celery_tasks import (
    deduct_credits_task,
    log_usage_task,
    send_mqtt_alert_task
)

router = APIRouter()

@router.api_route("/api/proxy/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(service: str, path: str, request: Request, user: dict = Depends(get_current_user)):
    tenant_id = user["tenant_id"]

    service_doc = get_service_by_name(service)
    if not service_doc:
        raise HTTPException(status_code=404, detail="Service not registered")

    base_url = service_doc["base_url"].rstrip("/")
    full_url = f"{base_url}/{path}"

    endpoint_credit = get_endpoint_credit(service, f"/{path}")
    if not endpoint_credit:
        raise HTTPException(status_code=404, detail="Endpoint credit not defined")

    required_credits = endpoint_credit["credits"]

    user_doc = get_user_by_tenant_id(tenant_id)
    current_credits = user_doc.get("credits", 0)
    username = user_doc.get("username")

    if current_credits <= 100 and current_credits >= required_credits:
        warning_msg = f"Low credit alert: only {current_credits} credits left."
        publish_low_credit_alert(tenant_id, current_credits, message=warning_msg)
        insert_or_update_low_credit_notification(tenant_id, username, warning_msg)

    if current_credits < required_credits:
        block_msg = f"Insufficient credits: Required {required_credits}, but only {current_credits} available."
        publish_low_credit_alert(tenant_id, current_credits, message=block_msg)
        update_low_credit_notification_to_insufficient(tenant_id, username, required=required_credits, available=current_credits)
        raise HTTPException(status_code=402, detail=block_msg)

    chain(
        deduct_credits_task.s(tenant_id, service, f"/{path}"),
        log_usage_task.s(),
        send_mqtt_alert_task.s()
    ).delay()

    try:
        body = asyncio.run(request.body())
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read request body")

    headers = dict(request.headers)
    try:
        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=body
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Request to target failed: {str(e)}")

    # 7. Log usage
    log_usage(tenant_id, service, f"/{path}", required_credits)

    try:
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception:
        return JSONResponse(
            status_code=response.status_code,
            content={"detail": "Non-JSON response from proxied API"},
        )
