from fastapi import APIRouter, Depends, HTTPException
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.handler.service_handler import ServiceHandler
from scripts.core.model.service_models import Service
from scripts.core.utils.jwt_utils.jwt_handler import get_current_user

router = APIRouter()


@router.post(APIEndpoints.REGISTER_SERVICE)
def register_service(
    data: Service,
    user: dict = Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can register services")
    return ServiceHandler.register_service(data.model_dump())


@router.get(APIEndpoints.LIST_SERVICES)
def list_services():
    return ServiceHandler.list_services()


@router.get(APIEndpoints.SERVICE_DETAILS)
def get_service_details(service_name: str):
    return ServiceHandler.get_service_details(service_name)
