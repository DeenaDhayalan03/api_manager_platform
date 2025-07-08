from scripts.core.utils.mongo_utils.db_connection import db  # sync DB
from scripts.constants.app_configuration import settings


def register_service_in_db(service_data: dict) -> dict:
    db[settings.SERVICES_COLLECTION].insert_one(service_data)
    return service_data


def get_all_services_from_db() -> list:
    return list(db[settings.SERVICES_COLLECTION].find())


def get_service_by_name(service_name: str) -> dict | None:
    return db[settings.SERVICES_COLLECTION].find_one({"name": service_name})
