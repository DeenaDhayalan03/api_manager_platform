from pydantic import BaseModel

class Plan(BaseModel):
    name: str
    description: str
    credits: int | None
    duration_days: int

class PlanResponse(Plan):
    pass
