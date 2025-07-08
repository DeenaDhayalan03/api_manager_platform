from pydantic import BaseModel
from typing import Optional

class StatusResponse(BaseModel):
    success: bool
    message: str

class CreditsResponse(BaseModel):
    credits_remaining: Optional[int]
    rate_limit: Optional[int]
    rate_window: Optional[str]
