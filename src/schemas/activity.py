from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas.organization import Organization


class Activity(BaseModel):
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ActivityWithChildren(Activity):
    children: List["ActivityWithChildren"] = []

    model_config = ConfigDict(from_attributes=True)


class ActivityWithOrganizations(Activity):
    organizations: List["Organization"] = []

    model_config = ConfigDict(from_attributes=True)
