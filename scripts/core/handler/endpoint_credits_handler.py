from fastapi import HTTPException
from scripts.core.utils.endpoint_credits_utils import (
    add_endpoint_credit,
    get_all_endpoint_credits,
    get_endpoint_credit,
    delete_endpoint_credit
)
from scripts.core.utils.mongo_utils.mongo_utils import serialize_mongo_document


class EndpointCreditHandler:

    @staticmethod
    def add_only(data: dict) -> dict:
        try:
            add_endpoint_credit(data["service"], data["endpoint"], data["credits"])
            return {"message": "Endpoint credit added successfully"}
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update endpoint credit: {str(e)}")

    @staticmethod
    def list_all() -> list:
        try:
            raw_records = get_all_endpoint_credits()
            return [serialize_mongo_document(record) for record in raw_records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch endpoint credits: {str(e)}")

    @staticmethod
    def get(service: str, endpoint: str) -> dict:
        try:
            credit = get_endpoint_credit(service, endpoint)
            if not credit:
                raise HTTPException(status_code=404, detail="Endpoint credit not found")
            return serialize_mongo_document(credit)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch endpoint credit: {str(e)}")

    @staticmethod
    def delete(service: str, endpoint: str) -> dict:
        try:
            result = delete_endpoint_credit(service, endpoint)
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Endpoint credit not found")
            return {"message": "Endpoint credit deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete endpoint credit: {str(e)}")
