from fastapi import APIRouter
from typing import List

from src.exceptions import BuildingNotFoundException, BuildingNotFoundHTTPException
from src.services.buildings import BuildingService
from src.api.dependencies import DBDep, ApiKeyDep
from src.schemas.building import Building, BuildingWithOrganizations

router = APIRouter(prefix="/buildings", tags=["Здания"])


@router.get("", summary="Список всех зданий")
async def get_buildings(
    db: DBDep, api_key: ApiKeyDep, skip: int = 0, limit: int = 100
) -> List[Building]:
    """Получить список всех зданий"""
    return await BuildingService(db).get_all()


@router.get("/{building_id}", summary="Информация о здании")
async def get_building(
    building_id: int, db: DBDep, api_key: ApiKeyDep
) -> BuildingWithOrganizations:
    """Получить информацию о здании по ID"""
    try:
        return await BuildingService(db).get_one_or_none_building(building_id)
    except BuildingNotFoundException:
        raise BuildingNotFoundHTTPException()
