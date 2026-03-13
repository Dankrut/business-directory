from pydantic import BaseModel, ConfigDict


class Phone(BaseModel):
    id: int
    phone: str
    organization_id: int

    model_config = ConfigDict(from_attributes=True)
