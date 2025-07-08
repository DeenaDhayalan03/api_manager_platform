from scripts.core.utils.mongo_utils.db_connection import db
from scripts.constants.app_configuration import settings


def get_user_by_username(username: str):
    return db[settings.USERS_COLLECTION].find_one({"username": username})


def create_user(data: dict) -> dict:
    db[settings.USERS_COLLECTION].insert_one(data)
    return data


def update_user_credits(tenant_id: str, new_credits: int):
    return db[settings.USERS_COLLECTION].update_one(
        {"tenant_id": tenant_id},
        {"$set": {"credits": new_credits}}
    )


def get_user_by_tenant_id(tenant_id: str):
    return db[settings.USERS_COLLECTION].find_one({"tenant_id": tenant_id})
