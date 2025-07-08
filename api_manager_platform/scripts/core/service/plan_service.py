from fastapi import APIRouter
from scripts.core.handler.plan_handler import PlanHandler
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.model.plan_models import PlanResponse
from typing import List

router = APIRouter()


@router.get(APIEndpoints.LIST_PLANS, response_model=List[PlanResponse])
def list_available_plans():
    return PlanHandler.get_all_plans()
