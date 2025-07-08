from scripts.core.utils.mongo_utils.db_connection import db
from datetime import datetime
from scripts.constants.app_configuration import settings


def log_usage(tenant_id: str, service: str, endpoint: str, credits_used: int):
    log = {
        "tenant_id": tenant_id,
        "service": service,
        "endpoint": endpoint,
        "credits_used": credits_used,
        "timestamp": datetime.utcnow()
    }
    db[settings.USAGE_LOGS_COLLECTION].insert_one(log)


def get_usage_logs(tenant_id: str, filters: dict = {}):
    query = {"tenant_id": tenant_id}
    query.update(filters)
    return list(db[settings.USAGE_LOGS_COLLECTION].find(query))


def get_usage_summary(tenant_id: str):
    pipeline = [
        {"$match": {"tenant_id": tenant_id}},
        {"$group": {
            "_id": "$endpoint",
            "total_calls": {"$sum": 1},
            "total_credits": {"$sum": "$credits_used"}
        }}
    ]
    return list(db[settings.USAGE_LOGS_COLLECTION].aggregate(pipeline))
