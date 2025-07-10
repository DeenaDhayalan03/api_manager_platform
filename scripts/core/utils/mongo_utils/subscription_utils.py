from scripts.core.utils.mongo_utils.db_connection import db
from datetime import datetime, timedelta
from scripts.constants.app_configuration import settings


def create_subscription(tenant_id: str, plan_name: str, service_name: str, duration_days: int):
    sub_doc = {
        "tenant_id": tenant_id,
        "plan_name": plan_name,
        "service_name": service_name,
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(days=duration_days)
    }
    db[settings.SUBSCRIPTIONS_COLLECTION].insert_one(sub_doc)


def get_active_subscription(tenant_id: str):
    now = datetime.utcnow()
    return db[settings.SUBSCRIPTIONS_COLLECTION].find_one({
        "tenant_id": tenant_id,
        "start_date": {"$lte": now},
        "end_date": {"$gte": now}
    })
