from fastapi import HTTPException
from scripts.core.utils.mongo_utils.usage_log_utils import (
    log_usage,
    get_usage_logs,
    get_usage_summary
)
from scripts.core.model.usage_models import UsageLog, UsageSummary
from scripts.core.utils.celery_tasks import deduct_credits_task


class UsageHandler:

    @staticmethod
    def trigger_credit_deduction(user: dict, service: str, endpoint: str) -> dict:
        try:
            tenant_id = user["tenant_id"]

            # Trigger the celery task
            deduct_credits_task.delay(
                tenant_id=tenant_id,
                service=service,
                endpoint=endpoint
            )

            return {"message": "Credits deduction triggered"}
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to trigger credit deduction")

    @staticmethod
    def log_usage_entry(
        tenant_id: str, service: str, endpoint: str, credits_used: int
    ) -> dict:
        try:
            log_usage(tenant_id, service, endpoint, credits_used)
            return {"message": "Usage logged successfully"}
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to log usage")

    @staticmethod
    def get_my_usage_logs(user: dict) -> list[UsageLog]:
        try:
            tenant_id = user["tenant_id"]
            logs = get_usage_logs(tenant_id)
            return logs
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to retrieve usage logs")

    @staticmethod
    def get_my_usage_summary(user: dict) -> list[UsageSummary]:
        try:
            tenant_id = user["tenant_id"]
            summary = get_usage_summary(tenant_id)
            return summary
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to retrieve usage summary")
