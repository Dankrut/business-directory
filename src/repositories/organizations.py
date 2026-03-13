from typing import List, Optional
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.schemas.organization import Organization
from src.models.organization import OrganizationOrm
from src.models.activity import ActivityOrm  # Добавить импорт
from src.repositories.base import BaseRepository


class OrganizationsRepository(BaseRepository):
    model = OrganizationOrm
    schema = Organization

    async def get_filtered_with_relations(self, **filter_by):
        """Получить организации со всеми связанными данными"""
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.phones),
                selectinload(self.model.activities),
            )
        )
        result = await self.session.execute(query)
        organizations = result.unique().scalars().all()
        # Добавить from_attributes=True
        return [
            self.schema.model_validate(org, from_attributes=True)
            for org in organizations
        ]

    async def get_one_with_relations(self, **filter_by) -> Optional[Organization]:
        """Получить одну организацию со всеми связями (возвращает None если не найдена)"""
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.phones),
                selectinload(self.model.activities),
            )
        )
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def get_by_activity_ids(self, activity_ids: List[int]) -> List[Organization]:
        """Получить организации по списку ID деятельности"""
        if not activity_ids:
            return []

        query = (
            select(self.model)
            .join(self.model.activities)
            .where(ActivityOrm.id.in_(activity_ids))
            .options(
                selectinload(self.model.building),
                selectinload(self.model.phones),
                selectinload(self.model.activities),
            )
            .distinct()
        )
        result = await self.session.execute(query)
        organizations = result.unique().scalars().all()
        return [
            self.schema.model_validate(org, from_attributes=True)
            for org in organizations
        ]
