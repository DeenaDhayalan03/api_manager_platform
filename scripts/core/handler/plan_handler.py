from scripts.core.utils.mongo_utils.plan_utils import get_all_plans_from_db
from fastapi import HTTPException

class PlanHandler:

    @staticmethod
    def get_all_plans() -> list:
        try:
            plans = get_all_plans_from_db()
            if not plans:
                raise HTTPException(status_code=404, detail="No plans found")
            return plans
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
