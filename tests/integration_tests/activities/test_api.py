from httpx import AsyncClient


async def test_get_activities(ac: AsyncClient):
    """Тест получения всех видов деятельности"""
    response = await ac.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_activity_tree(ac: AsyncClient):
    """Тест получения дерева деятельности"""
    response = await ac.get("/activities/tree")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_activity_by_id(ac: AsyncClient):
    """Тест получения деятельности по ID"""
    response = await ac.get("/activities/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


async def test_get_activity_not_found(ac: AsyncClient):
    """Тест получения несуществующей деятельности"""
    response = await ac.get("/activities/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Вид деятельности не найден"
