from scripts.core.utils.mongo_utils.db_connection import db  # sync DB
from scripts.constants.app_configuration import settings


def get_plan_by_name(name: str) -> dict | None:
    return db[settings.PLANS_COLLECTION].find_one({"name": name})


def get_all_plans_from_db() -> list:
    return list(db[settings.PLANS_COLLECTION].find({}))
