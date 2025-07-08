from pydantic import BaseModel
from datetime import datetime
from typing import List

class InvoiceLog(BaseModel):
    service: str
    endpoint: str
    credits_used: int
    timestamp: datetime

class Invoice(BaseModel):
    tenant_id: str
    total_credits_used: int
    log_count: int
    logs: List[InvoiceLog]
    generated_at: datetime
