from geopy.distance import geodesic
from src.exceptions import (
    ActivityNotFoundException,
    NoOrganizationsByActivityException,
    NoOrganizationsInAreaException,
    NoOrganizationsInBuildingException,
    OrganizationNotFoundException,
)
from src.services.base import BaseService
from src.schemas.organization import OrganizationSearchResult


class OrganizationService(BaseService):
    async def get_filtered_building(self, building_id: int):
        organizations = await self.db.organizations.get_filtered_with_relations(
            building_id=building_id
        )
        if not organizations:
            raise NoOrganizationsInBuildingException()
        return organizations

    async def get_activity_id(self, activity_id: int):
        activity = await self.db.activities.get_one_or_none(id=activity_id)
        if not activity:
            raise ActivityNotFoundException()
        organizations = await self.db.organizations.get_by_activity_ids([activity_id])
        if not organizations:
            raise NoOrganizationsByActivityException()
        return organizations

    async def get_all_with_buildings(self, lat: float, lng: float, radius: float):
        all_orgs = await self.db.organizations.get_filtered_with_relations()
        result = []
        point = (lat, lng)
        for org in all_orgs:
            org_point = (org.building.latitude, org.building.longitude)
            distance = geodesic(point, org_point).meters

            if distance <= radius:
                result.append(
                    OrganizationSearchResult(
                        id=org.id,
                        name=org.name,
                        address=org.building.address,
                        phones=[p.phone for p in org.phones],
                        activities=[a.name for a in org.activities],
                        distance=distance,
                    )
                )
        if not result:
            raise NoOrganizationsInAreaException()
        return result

    async def get_one_or_none_rel(self, organization_id: int):
        organization = await self.db.organizations.get_one_with_relations(
            id=organization_id
        )
        if organization is None:
            raise OrganizationNotFoundException()
        return organization

    async def get_one_or_none_name(self, activity_name: str):
        root = await self.db.activities.get_one_or_none(name=activity_name)
        if not root:
            raise ActivityNotFoundException()
        # Получаем все дочерние ID (рекурсивно до 3 уровня)
        activity_ids = await self.db.activities.get_all_descendant_ids(root.id)
        activity_ids.append(root.id)

        # Получаем организации по этим видам деятельности
        organizations = await self.db.organizations.get_by_activity_ids(activity_ids)

        if not organizations:
            raise NoOrganizationsByActivityException()

        result = []
        for org in organizations:
            result.append(
                OrganizationSearchResult(
                    id=org.id,
                    name=org.name,
                    address=org.building.address,
                    phones=[p.phone for p in org.phones],
                    activities=[a.name for a in org.activities],
                )
            )

        return result

    async def get_filtered_name(self, name: str):
        # Получаем все организации со связями
        all_orgs = await self.db.organizations.get_filtered_with_relations()

        # Фильтруем по имени в Python
        result = []
        for org in all_orgs:
            if name.lower() in org.name.lower():
                result.append(
                    OrganizationSearchResult(
                        id=org.id,
                        name=org.name,
                        address=org.building.address,
                        phones=[p.phone for p in org.phones],
                        activities=[a.name for a in org.activities],
                    )
                )
        if not result:
            raise OrganizationNotFoundException()

        return result
