from fastapi import HTTPException
from scripts.core.utils.mongo_utils.service_utils import (
    register_service_in_db,
    get_all_services_from_db,
    get_service_by_name
)
from scripts.core.utils.mongo_utils.mongo_utils import serialize_mongo_document


class ServiceHandler:

    @staticmethod
    def register_service(data: dict) -> dict:
        existing = get_service_by_name(data["name"])
        if existing:
            raise HTTPException(status_code=400, detail="Service already exists")

        service = register_service_in_db(data)
        return serialize_mongo_document(service)

    @staticmethod
    def list_services() -> list:
        services = get_all_services_from_db()
        if not services:
            raise HTTPException(status_code=404, detail="No services found")
        return [serialize_mongo_document(service) for service in services]

    @staticmethod
    def get_service_details(service_name: str) -> dict:
        service = get_service_by_name(service_name)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return serialize_mongo_document(service)
