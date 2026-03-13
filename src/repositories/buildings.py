from src.schemas.building import Building
from src.models.building import BuildingOrm
from src.repositories.base import BaseRepository


class BuildingsRepository(BaseRepository):
    model = BuildingOrm
    schema = Building
