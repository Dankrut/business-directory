from fastapi import APIRouter
from typing import List

from src.exceptions import ActivityNotFoundException, ActivityNotFoundHTTPException
from src.services.activities import ActivityService
from src.api.dependencies import DBDep, ApiKeyDep
from src.schemas.activity import Activity, ActivityWithChildren

router = APIRouter(prefix="/activities", tags=["Виды деятельности"])


@router.get("", summary="Список всех видов деятельности")
async def get_activities(db: DBDep, api_key: ApiKeyDep) -> List[Activity]:
    """Получить список всех видов деятельности"""
    return await ActivityService(db).get_all_activities()


@router.get("/tree", summary="Дерево видов деятельности")
async def get_activity_tree(
    db: DBDep, api_key: ApiKeyDep
) -> List[ActivityWithChildren]:
    """Получить дерево видов деятельности (с вложенными детьми до 3 уровня)"""
    return await ActivityService(db).get_activity_tree()


@router.get("/{activity_id}", summary="Информация о виде деятельности")
async def get_activity(activity_id: int, db: DBDep, api_key: ApiKeyDep) -> Activity:
    """Получить информацию о виде деятельности по ID"""
    try:
        return await ActivityService(db).get_activity_by_id(activity_id)
    except ActivityNotFoundException:
        raise ActivityNotFoundHTTPException()
