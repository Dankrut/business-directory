from pydantic import BaseModel, ConfigDict
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas.organization import Organization


class Building(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class BuildingWithOrganizations(Building):
    organizations: List["Organization"] = []  # Organization будет импортирован позже

    model_config = ConfigDict(from_attributes=True)
