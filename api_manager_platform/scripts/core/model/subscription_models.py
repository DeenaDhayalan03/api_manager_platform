from pydantic import BaseModel
from datetime import datetime

class Subscription(BaseModel):
    tenant_id: str
    plan_name: str
    service_name: str
    start_date: datetime
    end_date: datetime
