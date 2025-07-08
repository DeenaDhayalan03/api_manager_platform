from fastapi import APIRouter, Depends
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.model.endpoint_credits_model import EndpointCredit
from scripts.core.handler.endpoint_credits_handler import EndpointCreditHandler
from scripts.core.utils.jwt_utils.jwt_handler import get_current_user

router = APIRouter()


@router.post(APIEndpoints.ADD_OR_UPDATE_ENDPOINT_CREDIT)
def add_or_update_credit(
    data: EndpointCredit,
    user: dict = Depends(get_current_user)
):
    if user["role"] != "admin":
        return {"error": "Only admins can modify endpoint credits"}
    return EndpointCreditHandler.add_only(data.model_dump())


@router.get(APIEndpoints.LIST_ENDPOINT_CREDITS)
def list_endpoint_credits(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        return {"error": "Only admins can view endpoint credits"}
    return EndpointCreditHandler.list_all()


@router.get(APIEndpoints.GET_ENDPOINT_CREDIT)
def get_credit(service: str, endpoint: str, user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        return {"error": "Only admins can view endpoint credits"}
    return EndpointCreditHandler.get(service, endpoint)


@router.delete(APIEndpoints.DELETE_ENDPOINT_CREDIT)
def delete_credit(service: str, endpoint: str, user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        return {"error": "Only admins can delete endpoint credits"}
    return EndpointCreditHandler.delete(service, endpoint)
