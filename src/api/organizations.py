from fastapi import APIRouter, Query
from typing import List

from src.services.organizations import OrganizationService
from src.api.dependencies import DBDep, ApiKeyDep
from src.schemas.organization import Organization, OrganizationSearchResult
from src.exceptions import (
    OrganizationNotFoundException,
    ActivityNotFoundException,
    NoOrganizationsInAreaException,
    NoOrganizationsInBuildingException,
    NoOrganizationsByActivityException,
    OrganizationNotFoundHTTPException,
    ActivityNotFoundHTTPException,
    NoOrganizationsInAreaHTTPException,
    NoOrganizationsInBuildingHTTPException,
    NoOrganizationsByActivityHTTPException,
)

router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.get("/building/{building_id}", summary="Организации в здании")
async def get_organizations_by_building(
    building_id: int, db: DBDep, api_key: ApiKeyDep
) -> List[Organization]:
    """Получить все организации в конкретном здании"""
    try:
        return await OrganizationService(db).get_filtered_building(building_id)
    except NoOrganizationsInBuildingException:
        raise NoOrganizationsInBuildingHTTPException()


@router.get("/activity/{activity_id}", summary="Организации по виду деятельности")
async def get_organizations_by_activity(
    activity_id: int, db: DBDep, api_key: ApiKeyDep
) -> List[Organization]:
    """Получить все организации с указанным видом деятельности"""
    try:
        return await OrganizationService(db).get_activity_id(activity_id)
    except ActivityNotFoundException:
        raise ActivityNotFoundHTTPException()
    except NoOrganizationsByActivityException:
        raise NoOrganizationsByActivityHTTPException()


@router.get("/nearby", summary="Организации рядом")
async def get_organizations_nearby(
    db: DBDep,
    api_key: ApiKeyDep,
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: float = Query(..., gt=0, le=50000, description="Радиус в метрах"),
) -> List[OrganizationSearchResult]:
    """Найти организации в заданном радиусе от точки"""
    try:
        return await OrganizationService(db).get_all_with_buildings(lat, lng, radius)
    except NoOrganizationsInAreaException:
        raise NoOrganizationsInAreaHTTPException()


# 4. Информация об организации по ID
@router.get("/{organization_id}", summary="Детальная информация об организации")
async def get_organization_by_id(
    organization_id: int, db: DBDep, api_key: ApiKeyDep
) -> Organization:
    """Получить полную информацию об организации по ID"""
    try:
        return await OrganizationService(db).get_one_or_none_rel(organization_id)
    except OrganizationNotFoundException:
        raise OrganizationNotFoundHTTPException()


# 5. Поиск по дереву деятельности
@router.get(
    "/search/activity-tree/{activity_name}", summary="Поиск по дереву деятельности"
)
async def search_by_activity_tree(
    activity_name: str, db: DBDep, api_key: ApiKeyDep
) -> List[OrganizationSearchResult]:
    """Найти организации по виду деятельности и всем его подкатегориям"""
    try:
        return await OrganizationService(db).get_one_or_none_name(activity_name)
    except ActivityNotFoundException:
        raise ActivityNotFoundHTTPException()
    except NoOrganizationsByActivityException:
        raise NoOrganizationsByActivityHTTPException()


# 6. Поиск организации по названию
@router.get("/search/name", summary="Поиск организации по названию")
async def search_organizations_by_name(
    db: DBDep,
    api_key: ApiKeyDep,
    name: str = Query(..., min_length=1),
) -> List[OrganizationSearchResult]:
    """Найти организации по части названия"""
    try:
        return await OrganizationService(db).get_filtered_name(name)
    except OrganizationNotFoundException:
        raise OrganizationNotFoundHTTPException()
