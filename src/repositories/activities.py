from typing import List

from src.schemas.activity import Activity
from src.models.activity import ActivityOrm
from src.repositories.base import BaseRepository


class ActivitiesRepository(BaseRepository):
    model = ActivityOrm
    schema = Activity

    async def get_all_descendant_ids(self, activity_id: int) -> List[int]:
        """Получить все ID дочерних видов деятельности (рекурсивно до 3 уровня)"""
        descendant_ids = []

        children = await self.get_filtered(parent_id=activity_id)
        for child in children:
            descendant_ids.append(child.id)

            grandchildren = await self.get_filtered(parent_id=child.id)
            for grandchild in grandchildren:
                descendant_ids.append(grandchild.id)

        return descendant_ids
