from scripts.core.utils.mongo_utils.db_connection import db
from scripts.constants.app_configuration import settings
from datetime import datetime

NOTIFICATIONS_COLLECTION = settings.NOTIFICATIONS_COLLECTION

def insert_or_update_low_credit_notification(tenant_id: str, username: str, message: str):

    db[NOTIFICATIONS_COLLECTION].update_one(
        {
            "tenant_id": tenant_id,
            "username": username,
            "type": "warning",
            "read": False
        },
        {
            "$set": {
                "message": message,
                "timestamp": datetime.utcnow()
            }
        },
        upsert=True
    )


def update_low_credit_notification_to_insufficient(tenant_id: str, username: str, required: int, available: int):

    new_message = (
        f"Insufficient credits to access endpoint. Required: {required}, Available: {available}."
    )

    db[NOTIFICATIONS_COLLECTION].update_one(
        {
            "tenant_id": tenant_id,
            "username": username,
            "type": "warning",
            "read": False
        },
        {
            "$set": {
                "message": new_message,
                "timestamp": datetime.utcnow()
            }
        },
        upsert=True
    )
