from pydantic import BaseModel
from datetime import datetime

class UsageLog(BaseModel):
    tenant_id: str
    service: str
    endpoint: str
    credits_used: int
    timestamp: datetime

class UsageSummary(BaseModel):
    endpoint: str
    total_calls: int
    total_credits: int
