from pydantic import BaseModel

class EndpointCredit(BaseModel):
    service: str
    endpoint: str
    credits: int