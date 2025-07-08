from pydantic import BaseModel

class Service(BaseModel):
    name: str
    base_url: str
    description: str
