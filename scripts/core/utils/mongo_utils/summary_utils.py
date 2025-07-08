from datetime import datetime, timedelta
from scripts.constants.app_configuration import settings
from scripts.core.utils.mongo_utils.db_connection import db


def generate_scheduled_summary():

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=10)

    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time, "$lte": now}}},
        {"$group": {
            "_id": {
                "tenant_id": "$tenant_id",
                "username": "$username",
                "service": "$service",
                "endpoint": "$endpoint"
            },
            "total_calls": {"$sum": 1},
            "total_credits_used": {"$sum": "$credits_used"}
        }},
        {"$addFields": {"generated_at": now}}
    ]

    results = db[settings.USAGE_LOGS_COLLECTION].aggregate(pipeline)

    for doc in results:
        doc_id = doc["_id"]
        doc["generated_at"] = now

        db[settings.SCHEDULED_SUMMARY_COLLECTION].replace_one(
            {"_id": doc_id},
            doc,
            upsert=True
        )


def generate_usage_summary(tenant_id: str):
    """
    On-demand summary generation for invoices. Aggregates usage logs per service and endpoint for a tenant.
    """
    now = datetime.utcnow()

    pipeline = [
        {"$match": {"tenant_id": tenant_id}},
        {"$group": {
            "_id": {
                "service": "$service",
                "endpoint": "$endpoint"
            },
            "total_calls": {"$sum": 1},
            "total_credits_used": {"$sum": "$credits_used"}
        }},
        {"$addFields": {
            "tenant_id": tenant_id,
            "generated_at": now
        }}
    ]

    results = db[settings.USAGE_LOGS_COLLECTION].aggregate(pipeline)

    summary_docs = []
    for doc in results:
        summary = {
            "_id": {
                "tenant_id": tenant_id,
                "service": doc["_id"]["service"],
                "endpoint": doc["_id"]["endpoint"]
            },
            "total_calls": doc["total_calls"],
            "total_credits_used": doc["total_credits_used"],
            "generated_at": now
        }
        summary_docs.append(summary)
        db[settings.USAGE_SUMMARY_COLLECTION].replace_one(
            {"_id": summary["_id"]},
            summary,
            upsert=True
        )

    return summary_docs
