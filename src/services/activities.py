from src.exceptions import ActivityNotFoundException
from src.schemas.activity import ActivityWithChildren
from src.services.base import BaseService


class ActivityService(BaseService):
    async def get_all_activities(self):
        return await self.db.activities.get_all()

    async def get_activity_tree(self):
        """Получить дерево видов деятельности"""
        # Получаем все корневые элементы (level=1)
        roots = await self.db.activities.get_filtered(level=1)

        # Рекурсивно строим дерево
        result = []
        for root in roots:
            tree_item = await self._build_tree(root)
            result.append(tree_item)

        return result

    async def _build_tree(self, activity):
        """Рекурсивно строит дерево для одного узла"""
        children = await self.db.activities.get_filtered(parent_id=activity.id)

        child_trees = []
        for child in children:
            child_tree = await self._build_tree(child)
            child_trees.append(child_tree)

        return ActivityWithChildren(
            id=activity.id,
            name=activity.name,
            level=activity.level,
            parent_id=activity.parent_id,
            children=child_trees,
        )

    async def get_activity_by_id(self, activity_id: int):
        """Получить вид деятельности по ID"""
        activity = await self.db.activities.get_one_or_none(id=activity_id)
        if activity is None:
            raise ActivityNotFoundException()
        return activity
