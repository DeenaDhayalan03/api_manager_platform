from scripts.core.utils.mongo_utils.db_connection import db
from scripts.constants.app_configuration import settings


def add_endpoint_credit(service: str, endpoint: str, credits: int):
    existing = db[settings.ENDPOINT_CREDITS_COLLECTION].find_one({
        "service": service,
        "endpoint": endpoint
    })

    if existing:
        raise ValueError("Credit entry for this service and endpoint already exists")

    return db[settings.ENDPOINT_CREDITS_COLLECTION].insert_one({
        "service": service,
        "endpoint": endpoint,
        "credits": credits
    })


def get_all_endpoint_credits():
    return list(db[settings.ENDPOINT_CREDITS_COLLECTION].find())


def get_endpoint_credit(service: str, endpoint: str):
    return db[settings.ENDPOINT_CREDITS_COLLECTION].find_one(
        {"service": service, "endpoint": endpoint}
    )


def delete_endpoint_credit(service: str, endpoint: str):
    return db[settings.ENDPOINT_CREDITS_COLLECTION].delete_one(
        {"service": service, "endpoint": endpoint}
    )
