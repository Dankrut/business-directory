from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from src.schemas.phone import Phone
from src.schemas.activity import Activity
from src.schemas.building import Building


class Organization(BaseModel):
    id: int
    name: str
    building: Building
    phones: List[Phone]
    activities: List[Activity]

    model_config = ConfigDict(from_attributes=True)


# Для поиска - краткая информация
class OrganizationSearchResult(BaseModel):
    id: int
    name: str
    address: str
    phones: List[str]
    activities: List[str]
    distance: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
