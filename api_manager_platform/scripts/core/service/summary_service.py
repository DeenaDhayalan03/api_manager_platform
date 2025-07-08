from fastapi import APIRouter, Depends
from scripts.core.utils.jwt_utils.jwt_handler import get_current_user
from scripts.core.handler.summary_handler import get_usage_summary_handler
from scripts.constants.api_endpoints import APIEndpoints

router = APIRouter()

@router.get(APIEndpoints.TRIGGER_INVOICE)
def trigger_invoice_summary(current_user: dict = Depends(get_current_user)):
    return get_usage_summary_handler(current_user)