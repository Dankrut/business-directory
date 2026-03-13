from src.exceptions import BuildingNotFoundException
from src.services.base import BaseService


class BuildingService(BaseService):
    async def get_all(self):
        return await self.db.buildings.get_all()

    async def get_one_or_none_building(self, building_id: int):
        building = await self.db.buildings.get_one_or_none(id=building_id)
        if building is None:
            raise BuildingNotFoundException()
        return building
