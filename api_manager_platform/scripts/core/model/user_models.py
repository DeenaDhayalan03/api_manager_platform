from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    tenant_id: str
    role: str
    service_name: str
    plan_name: str
    credits: int | None
    rate_limit: int | None
    rate_window: str | None

class UserInDB(UserBase):
    password: str
    created_at: datetime
    plan_expiry: datetime
