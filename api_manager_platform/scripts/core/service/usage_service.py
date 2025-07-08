from fastapi import APIRouter, Depends
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.handler.usage_handler import UsageHandler
from scripts.core.utils.jwt_utils.jwt_handler import get_current_user

router = APIRouter()

@router.get(APIEndpoints.CREDITS_ME)
def get_my_usage_summary(user: dict = Depends(get_current_user)):
    return UsageHandler.get_my_usage_summary(user)
